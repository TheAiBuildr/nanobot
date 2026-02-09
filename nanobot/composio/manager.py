"""Composio manager for creating Tool Router sessions with MCP endpoints."""

import asyncio
from dataclasses import dataclass, field
from typing import Any

from loguru import logger

from nanobot.config.schema import ComposioConfig


@dataclass
class ComposioSession:
    """Holds the MCP endpoint info from a Composio Tool Router session."""
    mcp_url: str = ""
    mcp_headers: dict[str, str] = field(default_factory=dict)


class ComposioManager:
    """
    Manages the Composio Tool Router session.

    Responsible for:
    - Initializing the Composio SDK client
    - Creating a Tool Router session
    - Exposing the MCP URL and headers for use with nanobot's MCP client
    - Graceful shutdown
    """

    def __init__(self, config: ComposioConfig):
        self.config = config
        self._client: Any = None  # composio.Composio instance (lazy)
        self._session: ComposioSession | None = None

    async def start(self) -> ComposioSession | None:
        """
        Initialize the Composio client and create a Tool Router session.

        Returns the session info (MCP URL + headers) or None on failure.
        Runs synchronous SDK calls in a background thread.
        """
        if not self.config.enabled:
            logger.debug("Composio is disabled, skipping startup")
            return None

        try:
            from composio import Composio  # noqa: F811
        except ImportError:
            logger.warning(
                "Composio is enabled but the 'composio' package is not installed. "
                "Install it with: pip install \"nanobot-ai[composio]\""
            )
            return None

        if not self.config.api_key:
            logger.warning("Composio is enabled but no api_key is configured")
            return None

        # Create session in a thread (SDK is sync)
        self._session = await asyncio.to_thread(self._create_session, Composio)
        return self._session

    def _create_session(self, composio_cls: type) -> ComposioSession | None:
        """
        Synchronous helper: create Composio client and Tool Router session.

        Called inside asyncio.to_thread().
        """
        try:
            self._client = composio_cls(api_key=self.config.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Composio client: {e}")
            return None

        try:
            session = self._client.create(user_id=self.config.user_id)
            mcp_url = session.mcp.url
            mcp_headers = dict(session.mcp.headers) if session.mcp.headers else {}

            logger.info(f"Composio: Tool Router session created (MCP URL: {mcp_url})")
            return ComposioSession(mcp_url=mcp_url, mcp_headers=mcp_headers)
        except Exception as e:
            logger.error(f"Failed to create Composio Tool Router session: {e}")
            return None

    async def shutdown(self) -> None:
        """Clean up the Composio client and session."""
        self._client = None
        self._session = None
        logger.debug("Composio manager shut down")
