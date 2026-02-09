Add MCP Support to Nanobot

Architecture

MCP servers are external processes that expose tools over stdio or HTTP. Nanobot will launch/connect to these servers, discover their tools, and wrap each one as a native Tool instance so the agent can call them seamlessly.

flowchart LR
    Config["config.json\n(mcp section)"] --> SM[MCPServerManager]
    SM --> C1[MCPClient\nstdio]
    SM --> C2[MCPClient\nstreamable-http]
    C1 --> S1["MCP Server\n(e.g. filesystem)"]
    C2 --> S2["MCP Server\n(e.g. remote)"]
    SM --> TW[MCPToolWrapper\nper discovered tool]
    TW --> TR[ToolRegistry]
    TR --> AL[AgentLoop]

Key Design Decisions





Use the official mcp SDK (ClientSession, stdio_client, streamable_http_client) -- no custom protocol handling



**MCPServerManager** owns the full lifecycle: start servers, create sessions, discover tools, shut down cleanly



**One MCPToolWrapper** per MCP tool, implementing the existing Tool ABC. Tool names are prefixed mcp__{server}_{tool} (double underscore separates the mcp prefix from server name)



Async initialization -- MCP servers must be started before the agent loop processes messages, so AgentLoop gains an async start_mcp() method called before run()



Transport support: stdio (subprocess) and streamable-http (remote HTTP). The SSE transport is deprecated upstream



Environment variable expansion in server env config (e.g. "${GITHUB_TOKEN}" resolves from the host environment)



Optional dependency -- mcp is added under [project.optional-dependencies] and the feature degrades gracefully if not installed

Files to Change

1. Config Schema -- nanobot/config/schema.py

Fix the existing stubs. Move MCPServerConfig and MCPConfig out of the Config class (they are currently incorrectly nested inside it) and place them as top-level models alongside the other config classes. Add the mcp field to Config.

class MCPServerConfig(BaseModel):
    """Single MCP server configuration."""
    command: str = ""           # For stdio: "npx", "uvx", "python", etc.
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    transport: str = "stdio"    # "stdio" or "streamable-http"
    url: str | None = None      # For streamable-http transport

class MCPConfig(BaseModel):
    """MCP configuration."""
    enabled: bool = False
    servers: dict[str, MCPServerConfig] = Field(default_factory=dict)

2. MCP Client -- nanobot/mcp/client.py

Thin wrapper around the SDK's ClientSession. Handles both transport types and provides a unified interface for listing tools and calling tools.

Key methods:





async connect() -- establish session via stdio or streamable-http



async list_tools() -- return list of mcp.types.Tool



async call_tool(name, arguments) -- call tool and return text result



async close() -- clean shutdown

Uses contextlib.AsyncExitStack internally to manage the nested async context managers (stdio_client / streamable_http_client -> ClientSession).

3. MCP Server Manager -- nanobot/mcp/server_manager.py

Manages multiple MCPClient instances keyed by server name. Responsible for:





Starting all configured servers



Discovering tools from each server



Routing call_tool requests to the correct server



Graceful shutdown of all servers

class MCPServerManager:
    def __init__(self, config: MCPConfig): ...
    async def start_all(self) -> None: ...
    async def get_all_tools(self) -> list[tuple[str, Tool]]: ...  # (server_name, mcp_tool)
    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> str: ...
    async def shutdown(self) -> None: ...

4. MCP Types -- nanobot/mcp/types.py

Simple dataclass for internal use (wrapping discovered tool metadata):

@dataclass
class MCPToolInfo:
    server_name: str
    name: str
    description: str
    input_schema: dict

5. MCP Tool Wrapper -- nanobot/agent/tools/mcp/mcp_tool.py

Implements the Tool ABC, bridging an MCP tool into the nanobot tool system:

class MCPToolWrapper(Tool):
    def __init__(self, tool_info: MCPToolInfo, manager: MCPServerManager):
        self._info = tool_info
        self._manager = manager

    @property
    def name(self) -> str:
        return f"mcp__{self._info.server_name}_{self._info.name}"

    @property
    def description(self) -> str:
        return f"[MCP:{self._info.server_name}] {self._info.description}"

    @property
    def parameters(self) -> dict:
        return self._info.input_schema

    async def execute(self, **kwargs) -> str:
        return await self._manager.call_tool(
            self._info.server_name, self._info.name, kwargs
        )

6. Agent Loop Integration -- nanobot/agent/loop.py





Add mcp_config parameter to AgentLoop.__init__() (optional, defaults to None)



Add async def start_mcp(self) method that starts the MCP server manager and registers all discovered tools



Add async def stop_mcp(self) for cleanup



Store self._mcp_manager on the instance

7. CLI Wiring -- nanobot/cli/commands.py





In gateway(): pass config.mcp to AgentLoop, call await agent.start_mcp() before the main asyncio.gather()



In agent(): same pattern -- call await agent_loop.start_mcp() before processing

8. Module Init Files





nanobot/mcp/init.py -- export MCPServerManager, MCPClient



nanobot/agent/tools/mcp/init.py -- export MCPToolWrapper

9. Dependencies -- pyproject.toml

Add optional dependency group:

[project.optional-dependencies]
mcp = ["mcp>=1.9.0"]

Example Config (config.json)

{
  "mcp": {
    "enabled": true,
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/tylerhunt/workspace"]
      },
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
      },
      "remote": {
        "transport": "streamable-http",
        "url": "http://my-server:8000/mcp"
      }
    }
  }
}

Graceful Degradation

If mcp package is not installed and mcp.enabled is True, log a warning and skip MCP initialization rather than crashing. This is handled via a try/import guard in start_mcp().