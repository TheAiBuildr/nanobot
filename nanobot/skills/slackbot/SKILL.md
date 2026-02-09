---
name: slackbot
description: "Slack messaging and workspace management via Composio. Use when the user needs to (1) send messages to Slack channels or users, (2) search for channels or users, (3) read conversation history, (4) manage channels (create, archive, invite), (5) add reactions, (6) set reminders, or (7) manage files in Slack."
---

# Slackbot

Send messages, manage channels, and interact with Slack workspaces.

## Quick Start

When the user says:
- "Send a message to #general"
- "Find the #engineering channel"
- "What's the latest in #updates?"
- "Create a new Slack channel"
- "Set a Slack reminder"

## Core Operations

### Send a Message

```
mcp__composio_SLACKBOT_SEND_MESSAGE(
    channel="C01ABCDEF",
    text="Hello from nanobot!"
)
```

Requires a channel ID. Use `SLACKBOT_FIND_CHANNELS` first to resolve channel names to IDs.

### Find Channels

```
mcp__composio_SLACKBOT_FIND_CHANNELS(
    query="engineering"
)
```

Search by name, topic, purpose, or description.

### Find Users

```
mcp__composio_SLACKBOT_FIND_USERS(
    query="john@example.com"
)
```

Search by email, name, or display name.

### Read Conversation History

```
mcp__composio_SLACKBOT_FETCH_CONVERSATION_HISTORY(
    channel="C01ABCDEF"
)
```

Retrieves recent messages from a channel, DM, or group.

### Read Thread Replies

```
mcp__composio_SLACKBOT_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION(
    channel="C01ABCDEF",
    ts="1234567890.123456"
)
```

### Add Reaction

```
mcp__composio_SLACKBOT_ADD_REACTION_TO_AN_ITEM(
    channel="C01ABCDEF",
    timestamp="1234567890.123456",
    name="thumbsup"
)
```

### Create Channel

```
mcp__composio_SLACKBOT_CREATE_CHANNEL(
    name="project-alpha",
    is_private=false
)
```

### Invite Users to Channel

```
mcp__composio_SLACKBOT_INVITE_USERS_TO_A_CHANNEL(
    channel="C01ABCDEF",
    users="U01ABCDEF,U02GHIJKL"
)
```

### Set a Reminder

```
mcp__composio_SLACKBOT_CREATE_A_REMINDER(
    text="Review PR #42",
    time="in 2 hours"
)
```

Accepts Unix timestamps, relative time ("in 30 minutes"), or natural language.

## Other Useful Tools

- `SLACKBOT_DELETES_A_MESSAGE_FROM_A_CHAT` -- delete a message
- `SLACKBOT_ARCHIVE_A_CONVERSATION` -- archive a channel
- `SLACKBOT_CLOSE_DM_OR_MULTI_PERSON_DM` -- close a DM
- `SLACKBOT_FETCH_ITEM_REACTIONS` -- get reactions on a message
- `SLACKBOT_GET_USER_PRESENCE_INFO` -- check if a user is online
- `SLACKBOT_FIND_USER_BY_EMAIL_ADDRESS` -- look up user by email
- `SLACKBOT_CREATE_A_USER_GROUP` -- create a user group
- `SLACKBOT_ADD_A_STAR_TO_AN_ITEM` -- star a message or file
- `SLACKBOT_DELETE_A_SCHEDULED_MESSAGE_IN_A_CHAT` -- cancel a scheduled message

## Workflow Patterns

### Send to Channel by Name
1. `SLACKBOT_FIND_CHANNELS` with the channel name
2. Extract the channel ID from the result
3. `SLACKBOT_SEND_MESSAGE` with the channel ID and message

### Summarize Recent Activity
1. `SLACKBOT_FIND_CHANNELS` to get channel ID
2. `SLACKBOT_FETCH_CONVERSATION_HISTORY` to get recent messages
3. Summarize the conversation for the user

## Error Handling

| Error | Solution |
|-------|----------|
| Channel not found | Use `SLACKBOT_FIND_CHANNELS` to search by name |
| Not in channel | Use `SLACKBOT_INVITE_USERS_TO_A_CHANNEL` to join |
| Message not found | Verify timestamp format (e.g., `1234567890.123456`) |
| Auth error | Re-authenticate via `COMPOSIO_MANAGE_CONNECTIONS` |
