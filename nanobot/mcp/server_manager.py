"""MCP server manager for managing multiple MCP server connections."""

from typing import Any

from loguru import logger

from nanobot.config.schema import MCPConfig
from nanobot.mcp.client import MCPClient
from nanobot.mcp.types import MCPToolInfo


class MCPServerManager:
    """
    Manages MCP server processes and connections.
    
    Responsible for:
    - Starting all configured servers
    - Discovering tools from each server
    - Routing tool calls to the correct server
    - Graceful shutdown of all servers
    """
    
    def __init__(self, config: MCPConfig):
        """
        Initialize the server manager.
        
        Args:
            config: MCP configuration with server definitions.
        """
        self.config = config
        self._clients: dict[str, MCPClient] = {}
        self._tools: dict[str, MCPToolInfo] = {}  # Keyed by "server_name:tool_name"
    
    async def start_all(self) -> None:
        """
        Start all configured MCP servers.
        
        Connects to each server and discovers its tools.
        """
        if not self.config.enabled:
            logger.debug("MCP is disabled, skipping server startup")
            return
        
        for name, server_config in self.config.servers.items():
            client = MCPClient(name, server_config)
            try:
                await client.connect()
                self._clients[name] = client
                
                # Discover tools from this server
                tools = await client.list_tools()
                for tool in tools:
                    key = f"{name}:{tool.name}"
                    self._tools[key] = MCPToolInfo(
                        server_name=name,
                        name=tool.name,
                        description=tool.description or "",
                        input_schema=tool.inputSchema if tool.inputSchema else {"type": "object", "properties": {}},
                    )
                
                logger.info(f"MCP server '{name}' started with {len(tools)} tools")
                
            except Exception as e:
                logger.error(f"Failed to start MCP server '{name}': {e}")
                # Ensure the failed client is fully cleaned up
                await client.close()
                # Continue with other servers even if one fails
    
    def get_all_tools(self) -> list[MCPToolInfo]:
        """
        Get all discovered tools from all servers.
        
        Returns:
            List of MCPToolInfo objects.
        """
        return list(self._tools.values())
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        Call a tool on a specific server.
        
        Args:
            server_name: Name of the server.
            tool_name: Name of the tool.
            arguments: Tool arguments.
        
        Returns:
            Tool result as a string.
        """
        client = self._clients.get(server_name)
        if not client:
            return f"Error: MCP server '{server_name}' not found or not connected"
        
        try:
            return await client.call_tool(tool_name, arguments)
        except Exception as e:
            logger.error(f"Error calling MCP tool '{server_name}:{tool_name}': {e}")
            return f"Error: {str(e)}"
    
    async def shutdown(self) -> None:
        """Shutdown all connected MCP servers."""
        for name, client in self._clients.items():
            try:
                await client.close()
                logger.debug(f"MCP server '{name}' shut down")
            except Exception as e:
                logger.error(f"Error shutting down MCP server '{name}': {e}")
        
        self._clients.clear()
        self._tools.clear()
        logger.info("All MCP servers shut down")
    
    @property
    def server_count(self) -> int:
        """Return the number of connected servers."""
        return len(self._clients)
    
    @property
    def tool_count(self) -> int:
        """Return the total number of discovered tools."""
        return len(self._tools)
