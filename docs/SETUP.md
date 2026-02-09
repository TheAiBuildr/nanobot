# Setting Up and Interacting with nanobot Agent

## 1. Installation

**Option A: From PyPI (stable)**
```bash
pip install nanobot-ai
```

**Option B: From source (latest features)**
```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**Option C: Using uv (fast)**
```bash
uv tool install nanobot-ai
```

---

## 2. Initialize Configuration

Run the onboard command to create the config and workspace:

```bash
nanobot onboard
```

This creates:
- Config file at `~/.nanobot/config.json`
- Workspace at `~/.nanobot/workspace/` with template files:
  - `AGENTS.md` - Agent instructions and guidelines
  - `SOUL.md` - Personality and values
  - `USER.md` - User preferences
  - `memory/MEMORY.md` - Long-term memory storage

---

## 3. Configure API Key

Edit `~/.nanobot/config.json` with your LLM provider:

### OpenRouter (recommended for global users)
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

### DeepSeek
```json
{
  "providers": {
    "deepseek": {
      "apiKey": "sk-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "deepseek-chat"
    }
  }
}
```

### Local vLLM
```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

---

## 4. Interacting with the Agent

### Single Message Mode
```bash
nanobot agent -m "What is 2+2?"
nanobot agent -m "List files in my home directory"
nanobot agent -m "Search the web for latest AI news"
```

### Interactive Chat Mode
```bash
nanobot agent
```
- Type your messages and press Enter
- Exit with `exit`, `quit`, `/exit`, `/quit`, `:q`, or `Ctrl+D`
- History is saved and restored between sessions

### CLI Options
```bash
nanobot agent -m "message" --no-markdown   # Plain text output
nanobot agent -m "message" --logs          # Show runtime logs
nanobot agent -s "session-name"            # Use specific session
```

---

## 5. Agent Tools

The agent has access to these built-in tools:

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create or overwrite files |
| `edit_file` | Make targeted edits to files |
| `list_dir` | List directory contents |
| `exec` | Execute shell commands |
| `web_search` | Search the web (requires Brave API key) |
| `web_fetch` | Fetch and parse web pages |
| `message` | Send messages to chat channels |
| `spawn` | Create background subagents |
| `cron` | Schedule recurring tasks |

---

## 6. Customizing the Agent

### Agent Instructions (`~/.nanobot/workspace/AGENTS.md`)
```markdown
# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Guidelines
- Always explain what you're doing before taking actions
- Ask for clarification when the request is ambiguous
- Use tools to help accomplish tasks
- Remember important information in your memory files
```

### Memory (`~/.nanobot/workspace/memory/MEMORY.md`)
The agent can read and write to this file to persist information across sessions.

---

## 7. Chat App Integrations

To use nanobot through Telegram, Discord, WhatsApp, etc., configure channels and run the gateway:

**Example Telegram config:**
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

**Start the gateway:**
```bash
nanobot gateway
```

---

## 8. Scheduled Tasks (Cron)

```bash
# Add a daily morning greeting
nanobot cron add --name "morning" --message "Good morning! What's on my schedule?" --cron "0 9 * * *"

# Add an hourly check
nanobot cron add --name "hourly" --message "Check status" --every 3600

# List jobs
nanobot cron list

# Remove a job
nanobot cron remove <job_id>
```

---

## 9. Composio Integration (800+ External Tools)

nanobot can connect to [Composio](https://composio.dev) to access 800+ tools across popular apps (GitHub, Gmail, Slack, etc.) with managed authentication.

### Install

```bash
pip install "nanobot-ai[mcp,composio]"
```

### Configure

Add the `composio` section to `~/.nanobot/config.json`:

```json
{
  "composio": {
    "enabled": true,
    "apiKey": "YOUR_COMPOSIO_API_KEY",
    "userId": "default"
  }
}
```

| Field | Description |
|-------|-------------|
| `enabled` | Set to `true` to activate Composio tools |
| `apiKey` | Your Composio API key (get one at [app.composio.dev](https://app.composio.dev)) |
| `userId` | Composio user ID for connected accounts (default: `"default"`) |

### Usage

Composio uses a **Tool Router** that exposes tools through an MCP endpoint. When enabled, nanobot creates a Tool Router session and connects to it using the built-in MCP client. Tools are discovered automatically and appear alongside built-in tools, prefixed with `mcp__composio_`.

Connected account authentication (OAuth, API keys) is managed through the [Composio dashboard](https://app.composio.dev).

---

## 10. Security Options

For production, enable workspace restriction:

```json
{
  "tools": {
    "restrictToWorkspace": true
  }
}
```

This sandboxes all file and shell operations to the workspace directory.

---

## 11. Check Status

```bash
nanobot status           # Show config and provider status
nanobot channels status  # Show channel configurations
```

---

## Troubleshooting

### Cannot connect to API (SSL errors)

If you see errors like:
```
Cannot connect to host api.openrouter.ai:443 ssl:default
```

**Possible causes and solutions:**

1. **Network/Firewall** - Check if your network blocks outbound HTTPS
   ```bash
   curl -I https://api.openrouter.ai
   ```

2. **Proxy required** - Set proxy environment variables:
   ```bash
   export HTTPS_PROXY=http://your-proxy:port
   export HTTP_PROXY=http://your-proxy:port
   ```

3. **Running in Docker** - Ensure container has network access:
   ```bash
   docker run --network host ...
   ```

4. **Try a different provider** - Use DeepSeek or a local model instead

### Invalid API Key

```bash
nanobot status  # Check if API key is configured
```

Ensure your key is valid and has credits available.

---

## Architecture Summary

```
User Message
    ↓
AgentLoop (receives message)
    ↓
ContextBuilder (builds system prompt from AGENTS.md, SOUL.md, memory, skills)
    ↓
LLM Provider (calls Claude, GPT, DeepSeek, etc.)
    ↓
Tool Execution (if LLM requests tools)
    ↓
Response → User
```

The agent maintains session history, can use tools autonomously, and remembers context in the `memory/MEMORY.md` file for long-term persistence.
