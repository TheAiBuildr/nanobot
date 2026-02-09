---
name: quick-reply
description: "Send progress updates to the user during long-running tasks so they know you're still working."
metadata: {"nanobot":{"always":true}}
---

# Quick Reply: Progress Updates

When you're about to start a task that involves **multiple steps** or may take a while, send a brief progress message to the user so they know you're working on it. Use the `message` tool for this.

## When to Send Progress Updates

- **Multi-step tool chains**: You plan to call 3+ tools in sequence (e.g., search the web, fetch pages, then summarize).
- **Spawning subagents**: Before calling `spawn`, let the user know what's about to happen.
- **Complex research**: Multiple web searches or file reads to gather information.
- **Large file operations**: Scanning directories, processing many files.

## When NOT to Send Progress Updates

- **Quick responses**: If you can answer directly without tools, just respond.
- **Single tool calls**: One file read or one search does not need a progress update.
- **Follow-up questions**: If you're asking the user a question, no progress needed.

## How to Send

Use the `message` tool with a short, natural status update (1 line):

```
message(content="Searching for information on that topic...")
```

Then continue with your actual work. When transitioning between major phases, you may send another update:

```
message(content="Found some good sources. Compiling a summary now...")
```

## Guidelines

1. **Be brief** -- one short sentence per update. Do not send walls of text as progress.
2. **Be specific** -- "Searching for React performance tips..." is better than "Working on it...".
3. **Don't overdo it** -- 1-2 progress messages per task is plenty. More feels spammy.
4. **Front-load** -- send the first update early, before starting the slow work.
5. **Skip for CLI** -- progress updates are most useful on chat channels (Slack, Telegram, etc.) where there's latency between messages. In CLI/interactive mode the user can see tool output in real time.
