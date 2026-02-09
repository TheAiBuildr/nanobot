---
name: composio
description: "Use Composio Tool Router to access 800+ external tools (Gmail, Slack, GitHub, etc.) with managed authentication and a remote code interpreter."
metadata: {"nanobot":{"always":true}}
---

# Composio Tool Router

You have access to Composio's Tool Router, which provides external tools for interacting with third-party apps and services. All Composio tools are prefixed with `mcp__composio_`.

## Key Meta-Tools

These are your primary tools for working with Composio. Use them in this order:

### 1. COMPOSIO_SEARCH_TOOLS
Search for tools by natural language description. **Always use this first** when the user asks you to do something with an external app.

```
mcp__composio_COMPOSIO_SEARCH_TOOLS
  query: "send an email using gmail"
```

This returns tool slugs, descriptions, and parameter schemas you need to execute them.

### 2. COMPOSIO_MANAGE_CONNECTIONS
Connect or check the status of an app. Use this when:
- A tool execution fails due to missing authentication
- The user explicitly asks to connect an app
- You need to check which apps are connected

```
mcp__composio_COMPOSIO_MANAGE_CONNECTIONS
  action: "check_connection"
  app: "gmail"
```

When connecting a new app, this returns an authorization link for the user to click.

### 3. COMPOSIO_MULTI_EXECUTE_TOOL
Execute one or more discovered tools. After finding a tool with COMPOSIO_SEARCH_TOOLS, use this to run it.

### 4. COMPOSIO_GET_TOOL_SCHEMAS
Retrieve full input parameter schemas for specific tool slugs. Use when COMPOSIO_SEARCH_TOOLS does not provide complete parameter details. **Never guess or invent parameters** -- always get the schema first.

## Code Interpreter

### COMPOSIO_REMOTE_WORKBENCH
Run Python code in a persistent remote sandbox. Good for:
- Data analysis and transformation
- Processing outputs from other tools
- Working with files (CSV, JSON, images)
- Bulk automation loops

### COMPOSIO_REMOTE_BASH_TOOL
Run shell commands in the same remote sandbox. Good for:
- Quick file operations (jq, grep, sed)
- Installing packages for the workbench
- Downloading/uploading files

## Workflow

When a user asks you to interact with an external service:

1. **Search** for the right tool: `COMPOSIO_SEARCH_TOOLS`
2. **Check connection**: If unsure, use `COMPOSIO_MANAGE_CONNECTIONS` to verify the app is connected
3. **Get schema** if needed: `COMPOSIO_GET_TOOL_SCHEMAS` for full parameter details
4. **Execute**: Use the discovered tool or `COMPOSIO_MULTI_EXECUTE_TOOL`

If execution fails with an auth error, guide the user through connecting the app via `COMPOSIO_MANAGE_CONNECTIONS`.

## Tips

- Tool slugs follow the pattern `APPNAME_ACTION` (e.g. `GMAIL_SEND_EMAIL`, `SLACK_SEND_MESSAGE`)
- Connected apps persist across sessions -- you don't need to reconnect each time
- For complex multi-step workflows, use `COMPOSIO_REMOTE_WORKBENCH` to orchestrate
- When listing available tools for the user, use `COMPOSIO_SEARCH_TOOLS` with a broad query
