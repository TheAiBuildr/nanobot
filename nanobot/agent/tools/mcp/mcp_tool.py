"""MCP tool wrapper for integrating MCP tools into nanobot."""

from typing import Any

from nanobot.agent.tools.base import Tool
from nanobot.mcp.types import MCPToolInfo


class MCPToolWrapper(Tool):
    """
    Wraps an MCP tool for use in nanobot.
    
    This class bridges the MCP tool protocol to nanobot's Tool interface,
    allowing MCP tools to be registered and called like native tools.
    """
    
    def __init__(self, tool_info: MCPToolInfo, manager: "MCPServerManager"):
        """
        Initialize the wrapper.
        
        Args:
            tool_info: Information about the MCP tool.
            manager: The server manager that handles tool execution.
        """
        self._info = tool_info
        self._manager = manager
    
    @property
    def name(self) -> str:
        """Tool name with mcp__ prefix and server name."""
        # Use double underscore to separate prefix from server name
        return f"mcp__{self._info.server_name}_{self._info.name}"
    
    @property
    def description(self) -> str:
        """Tool description with server indicator."""
        return f"[MCP:{self._info.server_name}] {self._info.description}"
    
    @property
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for tool parameters."""
        return self._info.input_schema
    
    async def execute(self, **kwargs: Any) -> str:
        """
        Execute the MCP tool.
        
        Args:
            **kwargs: Tool arguments.
        
        Returns:
            Tool result as a string.
        """
        return await self._manager.call_tool(
            self._info.server_name,
            self._info.name,
            kwargs,
        )
