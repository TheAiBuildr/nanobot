"""MCP client wrapper for connecting to MCP servers."""

import os
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from loguru import logger

from nanobot.config.schema import MCPServerConfig


class MCPClient:
    """
    Client for connecting to an MCP server.
    
    Handles both stdio (subprocess) and streamable-http transports.
    Uses AsyncExitStack to manage the nested async context managers.
    """
    
    def __init__(self, name: str, config: MCPServerConfig):
        """
        Initialize an MCP client.
        
        Args:
            name: Server name (for logging).
            config: Server configuration.
        """
        self.name = name
        self.config = config
        self._stack: AsyncExitStack | None = None
        self._session: "ClientSession | None" = None
    
    async def connect(self) -> None:
        """
        Establish connection to the MCP server.
        
        Raises:
            ImportError: If the mcp package is not installed.
            Exception: If connection fails.
        """
        from mcp import ClientSession
        
        self._stack = AsyncExitStack()
        
        try:
            if self.config.transport == "streamable-http":
                await self._connect_http()
            else:
                await self._connect_stdio()
        except Exception:
            # Clean up the AsyncExitStack on failure to avoid dangling
            # anyio task groups that crash when garbage collected.
            await self._safe_close()
            raise
        
        logger.info(f"MCP client '{self.name}' connected via {self.config.transport}")
    
    async def _connect_stdio(self) -> None:
        """Connect via stdio transport (subprocess)."""
        from mcp import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
        
        # Expand environment variables in the env config
        env = self._expand_env(self.config.env)
        
        # Ensure any directory paths in args exist
        self._ensure_arg_dirs()
        
        server_params = StdioServerParameters(
            command=self.config.command,
            args=self.config.args,
            env=env if env else None,
        )
        
        read, write = await self._stack.enter_async_context(
            stdio_client(server_params)
        )
        self._session = await self._stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._session.initialize()
    
    async def _connect_http(self) -> None:
        """Connect via streamable HTTP transport."""
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
        
        if not self.config.url:
            raise ValueError(f"MCP server '{self.name}' uses streamable-http but no URL configured")
        
        kwargs: dict[str, Any] = {}
        if self.config.headers:
            kwargs["headers"] = self.config.headers
        
        read, write, _ = await self._stack.enter_async_context(
            streamable_http_client(self.config.url, **kwargs)
        )
        self._session = await self._stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._session.initialize()
    
    def _expand_env(self, env: dict[str, str]) -> dict[str, str]:
        """Expand ${VAR} references in environment values from host environment."""
        result = {}
        for key, value in env.items():
            if value.startswith("${") and value.endswith("}"):
                var_name = value[2:-1]
                result[key] = os.environ.get(var_name, "")
            else:
                result[key] = value
        return result
    
    def _ensure_arg_dirs(self) -> None:
        """Create any directory paths found in server args (e.g. filesystem server roots)."""
        for arg in self.config.args:
            # Skip flags and package names
            if arg.startswith("-") or arg.startswith("@") or ":" in arg:
                continue
            p = Path(arg).expanduser()
            if p.is_absolute() or (not p.is_file() and "/" in arg):
                p.mkdir(parents=True, exist_ok=True)
    
    async def list_tools(self) -> list["Tool"]:
        """
        List available tools from this server.
        
        Returns:
            List of MCP Tool objects.
        """
        if not self._session:
            raise RuntimeError(f"MCP client '{self.name}' not connected")
        
        result = await self._session.list_tools()
        return list(result.tools)
    
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """
        Call a tool on this server.
        
        Args:
            name: Tool name.
            arguments: Tool arguments.
        
        Returns:
            Tool result as a string.
        """
        from mcp import types
        
        if not self._session:
            raise RuntimeError(f"MCP client '{self.name}' not connected")
        
        result = await self._session.call_tool(name, arguments=arguments)
        
        # Check for errors
        if result.isError:
            error_text = ""
            for content in result.content:
                if isinstance(content, types.TextContent):
                    error_text += content.text
            return f"Error: {error_text}" if error_text else "Error: Unknown error"
        
        # Extract text content from the result
        text_parts = []
        for content in result.content:
            if isinstance(content, types.TextContent):
                text_parts.append(content.text)
            elif isinstance(content, types.ImageContent):
                text_parts.append(f"[Image: {content.mimeType}]")
            elif isinstance(content, types.EmbeddedResource):
                text_parts.append(f"[Resource: {content.resource.uri}]")
        
        return "\n".join(text_parts) if text_parts else "(no output)"
    
    async def _safe_close(self) -> None:
        """Close the stack, suppressing errors from partially-initialized contexts."""
        if self._stack:
            try:
                await self._stack.aclose()
            except BaseException as e:
                # Must catch BaseException: CancelledError is not a subclass of
                # Exception in Python 3.9+ and anyio raises it during cleanup.
                logger.debug(f"MCP client '{self.name}' cleanup error (ignored): {e}")
            finally:
                self._stack = None
                self._session = None
    
    async def close(self) -> None:
        """Close the connection and clean up resources."""
        await self._safe_close()
        logger.debug(f"MCP client '{self.name}' closed")
