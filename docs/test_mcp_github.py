"""Quick test of the GitHub MCP server connection."""
import asyncio
import json
from nanobot.config.loader import load_config
from nanobot.mcp import MCPServerManager

async def test():
    # Load config from the real config file
    config = load_config()
    mcp_config = config.mcp
    
    if not mcp_config.enabled:
        print("MCP is not enabled in config!")
        return
    
    # Only test the github server
    from nanobot.config.schema import MCPConfig
    github_only = MCPConfig(
        enabled=True,
        servers={"github": mcp_config.servers["github"]}
    )
    
    manager = MCPServerManager(github_only)
    print("Starting GitHub MCP server...")
    await manager.start_all()
    
    tools = manager.get_all_tools()
    print(f"\n✅ Connected! Found {len(tools)} GitHub tools:\n")
    for t in sorted(tools, key=lambda x: x.name):
        desc = t.description[:80] if t.description else "(no description)"
        print(f"  • {t.name}: {desc}")
    
    # Quick test: list repos for the authenticated user
    print("\n--- Testing: list user repos ---")
    result = await manager.call_tool("github", "list_commits", {
        "owner": "txhunter",
        "repo": "nanobot",
        "perPage": 3,
    })
    print(result[:1000])
    
    await manager.shutdown()
    print("\n✅ GitHub MCP test complete!")

if __name__ == "__main__":
    asyncio.run(test())
