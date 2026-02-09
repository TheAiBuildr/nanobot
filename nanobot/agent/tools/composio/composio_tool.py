"""Composio tool wrapper for integrating Composio tools into nanobot."""

from typing import Any

from nanobot.agent.tools.base import Tool
from nanobot.composio.types import ComposioToolInfo


class ComposioToolWrapper(Tool):
    """
    Wraps a Composio tool for use in nanobot.

    This class bridges Composio's tool schema to nanobot's Tool interface,
    allowing Composio tools to be registered and called like native tools.
    """

    def __init__(self, tool_info: ComposioToolInfo, manager: "ComposioManager"):
        """
        Initialize the wrapper.

        Args:
            tool_info: Information about the Composio tool.
            manager: The ComposioManager that handles tool execution.
        """
        self._info = tool_info
        self._manager = manager

    @property
    def name(self) -> str:
        """Tool name with composio__ prefix."""
        return f"composio__{self._info.slug}"

    @property
    def description(self) -> str:
        """Tool description with Composio indicator."""
        return f"[Composio] {self._info.description}"

    @property
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for tool parameters."""
        schema = self._info.input_schema
        # Ensure the schema has a valid top-level type
        if "type" not in schema:
            schema = {**schema, "type": "object"}
        if "properties" not in schema:
            schema = {**schema, "properties": {}}
        return schema

    async def execute(self, **kwargs: Any) -> str:
        """
        Execute the Composio tool.

        Args:
            **kwargs: Tool arguments.

        Returns:
            Tool result as a string.
        """
        return await self._manager.execute(self._info.slug, kwargs)
