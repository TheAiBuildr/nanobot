---
name: google-calendar
description: "Google Calendar event management via Composio. Use when the user needs to (1) create, update, or delete calendar events, (2) list upcoming events or check schedule, (3) find free time slots, (4) manage multiple calendars, (5) quick-add events from natural language, or (6) check availability for meetings."
---

# Google Calendar

Create, manage, and query events on Google Calendar.

## Quick Start

When the user says:
- "Schedule a meeting for [time]"
- "What's on my calendar today?"
- "Find a free slot this week"
- "Add an event for [description]"
- "Cancel my [event]"

## Core Operations

### Create Event

```
mcp__composio_GOOGLECALENDAR_CREATE_EVENT(
    calendar_id="primary",
    summary="Team Standup",
    start="2026-02-10T09:00:00Z",
    end="2026-02-10T09:30:00Z",
    description="Daily sync",
    attendees=["alice@example.com"]
)
```

Requires RFC3339 UTC timestamps. End must be after start. Use `primary` for the user's main calendar.

### Quick Add (Natural Language)

```
mcp__composio_GOOGLECALENDAR_QUICK_ADD(
    calendar_id="primary",
    text="Lunch with Bob at noon tomorrow"
)
```

Parses natural language to create an event. Great for quick scheduling.

### List Events

```
mcp__composio_GOOGLECALENDAR_EVENTS_LIST(
    calendar_id="primary",
    time_min="2026-02-09T00:00:00Z",
    time_max="2026-02-10T00:00:00Z"
)
```

### Find Events (Search)

```
mcp__composio_GOOGLECALENDAR_FIND_EVENT(
    calendar_id="primary",
    query="standup"
)
```

Search by text, time ranges, or last-modified date.

### Find Free Slots

```
mcp__composio_GOOGLECALENDAR_FIND_FREE_SLOTS(
    calendar_ids=["primary"],
    time_min="2026-02-10T08:00:00Z",
    time_max="2026-02-10T18:00:00Z"
)
```

Returns free/busy info for scheduling meetings.

### Update Event

```
mcp__composio_GOOGLECALENDAR_PATCH_EVENT(
    calendar_id="primary",
    event_id="event-id",
    summary="Updated Title",
    start="2026-02-10T10:00:00Z",
    end="2026-02-10T10:30:00Z"
)
```

Use `PATCH_EVENT` for partial updates. Use `UPDATE_EVENT` for full replacement.

### Delete Event

```
mcp__composio_GOOGLECALENDAR_DELETE_EVENT(
    calendar_id="primary",
    event_id="event-id"
)
```

### Remove Attendee

```
mcp__composio_GOOGLECALENDAR_REMOVE_ATTENDEE(
    calendar_id="primary",
    event_id="event-id",
    attendee_email="bob@example.com"
)
```

## Other Useful Tools

- `GOOGLECALENDAR_LIST_CALENDARS` -- list all calendars
- `GOOGLECALENDAR_GET_CALENDAR` -- get calendar details
- `GOOGLECALENDAR_DUPLICATE_CALENDAR` -- create a new calendar
- `GOOGLECALENDAR_CLEAR_CALENDAR` -- delete all events on primary calendar
- `GOOGLECALENDAR_EVENTS_MOVE` -- move event to another calendar
- `GOOGLECALENDAR_EVENTS_INSTANCES` -- get instances of a recurring event
- `GOOGLECALENDAR_FREE_BUSY_QUERY` -- free/busy for multiple calendars
- `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` -- get current time with timezone

## Workflow Patterns

### Schedule a Meeting
1. `GOOGLECALENDAR_FIND_FREE_SLOTS` to check availability
2. `GOOGLECALENDAR_CREATE_EVENT` with attendees
3. Confirm event details to the user

### Daily Agenda
1. `GOOGLECALENDAR_EVENTS_LIST` for today's date range
2. Summarize events for the user

## Error Handling

| Error | Solution |
|-------|----------|
| Invalid time format | Use RFC3339 UTC: `2026-02-10T09:00:00Z` |
| Calendar not found | Use `primary` or list calendars first |
| Event not found | Search with `GOOGLECALENDAR_FIND_EVENT` |
| End before start | Ensure end timestamp is after start |
