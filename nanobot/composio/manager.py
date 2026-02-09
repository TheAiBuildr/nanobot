"""Composio manager for discovering and executing Composio tools."""

import asyncio
import json
from typing import Any

from loguru import logger

from nanobot.config.schema import ComposioConfig
from nanobot.composio.types import ComposioToolInfo


class ComposioManager:
    """
    Manages the Composio SDK connection, tool discovery, and execution.

    Responsible for:
    - Initializing the Composio SDK client
    - Discovering tools from configured toolkits
    - Executing tool calls (sync SDK wrapped in asyncio.to_thread)
    - Graceful shutdown
    """

    def __init__(self, config: ComposioConfig):
        self.config = config
        self._client: Any = None  # composio.Composio instance (lazy)
        self._tools: list[ComposioToolInfo] = []

    async def start(self) -> None:
        """
        Initialize the Composio client and discover tools from configured toolkits.

        Runs synchronous SDK calls in a background thread to avoid blocking
        the event loop.
        """
        if not self.config.enabled:
            logger.debug("Composio is disabled, skipping startup")
            return

        try:
            from composio import Composio  # noqa: F811
        except ImportError:
            logger.warning(
                "Composio is enabled but the 'composio' package is not installed. "
                "Install it with: pip install \"nanobot-ai[composio]\""
            )
            return

        if not self.config.api_key:
            logger.warning("Composio is enabled but no api_key is configured")
            return

        if not self.config.toolkits:
            logger.warning(
                "Composio is enabled but no toolkits are configured. "
                "Add toolkits to composio.toolkits in config.json "
                "(e.g. [\"GITHUB\", \"GMAIL\"])"
            )
            return

        # Initialize client and discover tools in a thread (SDK is sync)
        self._tools = await asyncio.to_thread(self._discover_tools, Composio)

        if self._tools:
            logger.info(
                f"Composio: {len(self._tools)} tools discovered from "
                f"{len(self.config.toolkits)} toolkit(s)"
            )
        else:
            logger.warning("Composio: no tools discovered")

    def _discover_tools(self, composio_cls: type) -> list[ComposioToolInfo]:
        """
        Synchronous helper: create client and discover tools.

        Called inside asyncio.to_thread().
        """
        try:
            self._client = composio_cls(api_key=self.config.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Composio client: {e}")
            return []

        discovered: list[ComposioToolInfo] = []

        for toolkit_slug in self.config.toolkits:
            try:
                raw_tools = self._client.tools.get(
                    user_id=self.config.user_id,
                    toolkits=[toolkit_slug],
                )
                for tool in raw_tools:
                    # The SDK returns tool objects with function/name/description/parameters
                    # attributes.  Normalize into our internal dataclass.
                    info = self._parse_tool(tool, toolkit_slug)
                    if info:
                        discovered.append(info)
            except Exception as e:
                logger.error(f"Composio: failed to list tools for toolkit '{toolkit_slug}': {e}")

        return discovered

    # ------------------------------------------------------------------
    # Tool parsing helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_tool(tool: Any, toolkit_slug: str) -> ComposioToolInfo | None:
        """
        Parse a Composio SDK tool object into a ComposioToolInfo.

        The SDK may return different shapes depending on the provider used.
        We try multiple access patterns for resilience.
        """
        try:
            # Attempt dict-like access (raw dict from REST / provider.tools.get)
            if isinstance(tool, dict):
                func = tool.get("function", tool)
                slug = func.get("name") or func.get("slug") or ""
                name = func.get("name") or slug
                desc = func.get("description") or ""
                params = func.get("parameters") or func.get("input_schema") or {
                    "type": "object",
                    "properties": {},
                }
                return ComposioToolInfo(slug=slug, name=name, description=desc, input_schema=params)

            # Attempt attribute access (Pydantic model / SDK object)
            func = getattr(tool, "function", tool)
            slug = getattr(func, "name", None) or getattr(func, "slug", "") or ""
            name = getattr(func, "name", slug) or slug
            desc = getattr(func, "description", "") or ""
            params = getattr(func, "parameters", None) or getattr(func, "input_schema", None)
            if params is None:
                params = {"type": "object", "properties": {}}
            elif hasattr(params, "model_dump"):
                params = params.model_dump()
            elif hasattr(params, "dict"):
                params = params.dict()

            if not slug:
                return None

            return ComposioToolInfo(slug=slug, name=name, description=desc, input_schema=params)
        except Exception as e:
            logger.debug(f"Composio: could not parse tool from toolkit '{toolkit_slug}': {e}")
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_all_tools(self) -> list[ComposioToolInfo]:
        """Return all discovered tools."""
        return list(self._tools)

    async def execute(self, slug: str, arguments: dict[str, Any]) -> str:
        """
        Execute a Composio tool by slug.

        The synchronous SDK call is run in a thread.

        Args:
            slug: Tool slug (e.g. "GITHUB_CREATE_ISSUE").
            arguments: Tool arguments dict.

        Returns:
            Serialized result string.
        """
        if not self._client:
            return "Error: Composio client not initialized"

        try:
            result = await asyncio.to_thread(
                self._execute_sync,
                slug,
                arguments,
            )
            # Serialize result to a readable string
            if isinstance(result, str):
                return result
            if isinstance(result, dict):
                return json.dumps(result, ensure_ascii=False, default=str)
            return str(result)
        except Exception as e:
            logger.error(f"Composio: error executing tool '{slug}': {e}")
            return f"Error executing Composio tool '{slug}': {e}"

    def _execute_sync(self, slug: str, arguments: dict[str, Any]) -> Any:
        """Synchronous execute wrapper called inside to_thread."""
        return self._client.tools.execute(
            slug,
            user_id=self.config.user_id,
            arguments=arguments,
        )

    async def shutdown(self) -> None:
        """Clean up the Composio client."""
        self._client = None
        self._tools.clear()
        logger.debug("Composio manager shut down")

    @property
    def tool_count(self) -> int:
        """Return the total number of discovered tools."""
        return len(self._tools)
