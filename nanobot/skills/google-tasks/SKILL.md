---
name: google-tasks
description: "Google Tasks management via Composio. Use when the user needs to (1) create, update, or delete tasks, (2) list or organize task lists, (3) manage to-do items and subtasks, (4) mark tasks as complete, or (5) move or reorder tasks."
metadata: {"nanobot":{"emoji":"✅"}}
---

# Google Tasks

Task and to-do list management with Google Tasks.

## Quick Start

When the user says:
- "Add a task to my list"
- "Show my tasks"
- "Mark [task] as done"
- "Create a new task list"
- "What's on my to-do list?"

## Core Operations

### Create a Task

```
mcp__composio_GOOGLETASKS_INSERT_TASK(
    tasklist_id="task-list-id",
    title="Buy groceries",
    notes="Milk, eggs, bread",
    due="2026-02-10T00:00:00Z"
)
```

Optionally set `parent` for subtasks or `previous` to position after a specific task.

### List Tasks

```
mcp__composio_GOOGLETASKS_LIST_TASKS(
    tasklist_id="task-list-id"
)
```

Returns all tasks in a list. Use `showCompleted=true` to include completed tasks. Dates are RFC3339 UTC.

### Get a Specific Task

```
mcp__composio_GOOGLETASKS_GET_TASK(
    tasklist_id="task-list-id",
    task_id="task-id"
)
```

### Update a Task

```
mcp__composio_GOOGLETASKS_PATCH_TASK(
    tasklist_id="task-list-id",
    task_id="task-id",
    status="completed"
)
```

Use `PATCH_TASK` for partial updates (e.g., mark complete, change title). Use `UPDATE_TASK` for full replacement.

### Delete a Task

```
mcp__composio_GOOGLETASKS_DELETE_TASK(
    tasklist_id="task-list-id",
    task_id="task-id"
)
```

### Move a Task

```
mcp__composio_GOOGLETASKS_MOVE_TASK(
    tasklist_id="task-list-id",
    task_id="task-id",
    parent="new-parent-id"
)
```

Reorder or nest a task under a parent.

## Task List Management

```
mcp__composio_GOOGLETASKS_LIST_TASK_LISTS()
```

- `GOOGLETASKS_CREATE_TASK_LIST` -- create a new list
- `GOOGLETASKS_GET_TASK_LIST` -- get list details
- `GOOGLETASKS_PATCH_TASK_LIST` -- rename a list
- `GOOGLETASKS_DELETE_TASK_LIST` -- delete a list and all its tasks
- `GOOGLETASKS_CLEAR_TASKS` -- permanently remove all completed tasks from a list

## Workflow Patterns

### Quick Add
1. Get task lists with `GOOGLETASKS_LIST_TASK_LISTS`
2. Insert task into the appropriate list with `GOOGLETASKS_INSERT_TASK`
3. Confirm to user with task details

### Daily Review
1. List all task lists with `GOOGLETASKS_LIST_TASK_LISTS`
2. For each list, get tasks with `GOOGLETASKS_LIST_TASKS`
3. Summarize pending tasks for the user

## Error Handling

| Error | Solution |
|-------|----------|
| Task list not found | List all lists first with `GOOGLETASKS_LIST_TASK_LISTS` |
| Invalid date format | Use RFC3339 UTC format: `2026-02-10T00:00:00Z` |
| Task not found | Verify task ID with `GOOGLETASKS_LIST_TASKS` |
