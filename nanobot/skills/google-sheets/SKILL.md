---
name: google-sheets
description: "Google Sheets spreadsheet operations via Composio. Use when the user needs to (1) create or read spreadsheets, (2) add, update, or delete rows and columns, (3) query or filter spreadsheet data, (4) execute SQL against sheet data, (5) create charts, (6) format cells, or (7) search for existing spreadsheets."
---

# Google Sheets

Create, read, update, and query Google Sheets spreadsheets.

## Quick Start

When the user says:
- "Create a spreadsheet for [topic]"
- "Add a row to my sheet"
- "Read data from [spreadsheet]"
- "Query the sheet for [condition]"
- "Create a chart from this data"

## Core Operations

### Create Spreadsheet

```
mcp__composio_GOOGLESHEETS_CREATE_GOOGLE_SHEET1(
    title="Sales Tracker"
)
```

### Create from JSON

```
mcp__composio_GOOGLESHEETS_SHEET_FROM_JSON(
    title="Data Export",
    sheet_json=[{"Name": "Alice", "Score": 95}, {"Name": "Bob", "Score": 87}]
)
```

Creates a spreadsheet and populates it from structured JSON data.

### Read Data (Batch Get)

```
mcp__composio_GOOGLESHEETS_BATCH_GET(
    spreadsheet_id="sheet-id",
    ranges=["Sheet1!A1:D10"]
)
```

Retrieves values from specified cell ranges in A1 notation.

### Write Data (Batch Update)

```
mcp__composio_GOOGLESHEETS_BATCH_UPDATE(
    spreadsheet_id="sheet-id",
    range="Sheet1!A1",
    values=[["Name", "Score"], ["Alice", 95], ["Bob", 87]]
)
```

Writes values to a range. Set `first_sheet_new_row=true` to append as new rows.

### Append Values

```
mcp__composio_GOOGLESHEETS_SPREADSHEETS_VALUES_APPEND(
    spreadsheet_id="sheet-id",
    range="Sheet1!A1",
    values=[["Charlie", 92]]
)
```

Appends rows after existing data.

### Execute SQL Query

```
mcp__composio_GOOGLESHEETS_EXECUTE_SQL(
    spreadsheet_id="sheet-id",
    query="SELECT * FROM Sheet1 WHERE Score > 90"
)
```

Run SQL (SELECT, INSERT, UPDATE, DELETE) against sheet tables.

### Search Spreadsheets

```
mcp__composio_GOOGLESHEETS_SEARCH_SPREADSHEETS(
    query="budget 2026"
)
```

### Lookup Row

```
mcp__composio_GOOGLESHEETS_LOOKUP_SPREADSHEET_ROW(
    spreadsheet_id="sheet-id",
    column="A",
    query="Alice"
)
```

Finds the first row where a column exactly matches the query.

## Other Useful Tools

- `GOOGLESHEETS_ADD_SHEET` -- add a new worksheet tab
- `GOOGLESHEETS_DELETE_SHEET` -- remove a worksheet
- `GOOGLESHEETS_GET_SHEET_NAMES` -- list all worksheet names
- `GOOGLESHEETS_CREATE_SPREADSHEET_ROW` -- insert a new empty row at index
- `GOOGLESHEETS_CREATE_SPREADSHEET_COLUMN` -- insert a new column
- `GOOGLESHEETS_DELETE_DIMENSION` -- delete rows or columns
- `GOOGLESHEETS_CLEAR_VALUES` -- clear cell content (preserves formatting)
- `GOOGLESHEETS_FORMAT_CELL` -- apply text and background formatting
- `GOOGLESHEETS_CREATE_CHART` -- create a chart from data
- `GOOGLESHEETS_SET_BASIC_FILTER` / `CLEAR_BASIC_FILTER` -- filter and sort data
- `GOOGLESHEETS_GET_TABLE_SCHEMA` -- get column types and structure
- `GOOGLESHEETS_AGGREGATE_COLUMN_DATA` -- aggregate (sum, avg, etc.) on filtered rows

## Workflow Patterns

### Create and Populate
1. Create spreadsheet with `GOOGLESHEETS_CREATE_GOOGLE_SHEET1`
2. Write data with `GOOGLESHEETS_BATCH_UPDATE`
3. Share via Google Drive if needed

### Data Analysis
1. Search with `GOOGLESHEETS_SEARCH_SPREADSHEETS`
2. Query with `GOOGLESHEETS_EXECUTE_SQL` or `GOOGLESHEETS_BATCH_GET`
3. Summarize results for the user

## Error Handling

| Error | Solution |
|-------|----------|
| Spreadsheet not found | Use `GOOGLESHEETS_SEARCH_SPREADSHEETS` to find by name |
| Sheet not found | Use `GOOGLESHEETS_GET_SHEET_NAMES` to list valid sheets |
| Invalid range | Use A1 notation (e.g., `Sheet1!A1:C10`) |
| Permission denied | Check sharing settings or re-authenticate |
