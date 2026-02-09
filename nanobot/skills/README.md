# nanobot Skills

This directory contains built-in skills that extend nanobot's capabilities.

## Skill Format

Each skill is a directory containing a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Markdown instructions for the agent

## Attribution

These skills are adapted from [OpenClaw](https://github.com/openclaw/openclaw)'s skill system.
The skill format and metadata structure follow OpenClaw's conventions to maintain compatibility.

## Available Skills

| Skill | Description |
|-------|-------------|
| `github` | Interact with GitHub using the `gh` CLI |
| `weather` | Get weather info using wttr.in and Open-Meteo |
| `summarize` | Summarize URLs, files, and YouTube videos |
| `tmux` | Remote-control tmux sessions |
| `skill-creator` | Create new skills |
| `composio` | Use Composio Tool Router for 800+ external tools (Gmail, Slack, GitHub, etc.) |
| `browserless` | Web scraping, screenshots, PDF generation, and browser automation via Browserless |
| `google-calendar` | Google Calendar event management (create, list, find free slots) |
| `google-docs` | Google Docs document creation and editing (text, markdown, tables) |
| `google-drive` | Google Drive file management (upload, download, share, organize) |
| `google-sheets` | Google Sheets spreadsheet operations (read, write, query, chart) |
| `google-tasks` | Google Tasks to-do list management (create, update, organize) |
| `slackbot` | Slack messaging, channel management, and workspace interactions |