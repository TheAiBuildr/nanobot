---
name: google-docs
description: "Google Docs document creation and editing via Composio. Use when the user needs to (1) create a new Google Doc, (2) insert or replace text in a document, (3) add headers, footers, or tables, (4) format document content, (5) insert images or page breaks, (6) search for existing documents, or (7) update a document with markdown."
metadata: {"nanobot":{"emoji":"📝"}}
---

# Google Docs

Create, edit, and manage Google Docs documents.

## Quick Start

When the user says:
- "Create a Google Doc with this content"
- "Write a document about [topic]"
- "Search my Google Docs for [query]"
- "Add a table to the document"
- "Update the document with this text"

## Core Operations

### Create Document

```
mcp__composio_GOOGLEDOCS_CREATE_DOCUMENT(
    title="Meeting Notes",
    text="Initial content here"
)
```

Creates a new doc with a title and optional initial text.

### Create Document from Markdown

```
mcp__composio_GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN(
    title="Project Plan",
    content="# Heading\n\n- Item 1\n- Item 2"
)
```

Creates a doc from markdown content with automatic formatting.

### Insert Text

```
mcp__composio_GOOGLEDOCS_INSERT_TEXT_ACTION(
    document_id="doc-id",
    text="New paragraph text",
    index=1
)
```

Inserts text at a specific position (index) in the document.

### Replace All Text

```
mcp__composio_GOOGLEDOCS_REPLACE_ALL_TEXT(
    document_id="doc-id",
    find_text="old text",
    replace_text="new text"
)
```

Finds and replaces all occurrences throughout the document.

### Update Document with Markdown

```
mcp__composio_GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN(
    document_id="doc-id",
    content="# Updated Content\n\nNew body text"
)
```

Replaces the entire document content with new markdown. Requires edit access.

### Search Documents

```
mcp__composio_GOOGLEDOCS_SEARCH_DOCUMENTS(
    query="quarterly review"
)
```

Find docs by name, content, date range, and other filters.

### Copy Document

```
mcp__composio_GOOGLEDOCS_COPY_DOCUMENT(
    document_id="doc-id",
    title="Copy of Meeting Notes"
)
```

## Other Useful Tools

- `GOOGLEDOCS_INSERT_TABLE_ACTION` -- insert a table (rows x columns)
- `GOOGLEDOCS_INSERT_TABLE_COLUMN` / `INSERT_TABLE_ROW` -- add rows or columns
- `GOOGLEDOCS_MERGE_TABLE_CELLS` / `UNMERGE_TABLE_CELLS` -- merge/unmerge cells
- `GOOGLEDOCS_CREATE_HEADER` / `CREATE_FOOTER` -- add headers and footers
- `GOOGLEDOCS_CREATE_FOOTNOTE` -- add footnotes
- `GOOGLEDOCS_INSERT_INLINE_IMAGE` -- insert image from URL
- `GOOGLEDOCS_INSERT_PAGE_BREAK` -- insert page break
- `GOOGLEDOCS_UPDATE_DOCUMENT_STYLE` -- set page size, margins, direction
- `GOOGLEDOCS_UPDATE_EXISTING_DOCUMENT` -- apply programmatic edits (insert, delete, format)
- `GOOGLEDOCS_REPLACE_IMAGE` -- replace an image with a new one

## Workflow Patterns

### Write and Share
1. Create document with `GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN`
2. Share via Google Drive: `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE`

### Edit Existing Document
1. Search with `GOOGLEDOCS_SEARCH_DOCUMENTS`
2. Use `GOOGLEDOCS_INSERT_TEXT_ACTION` or `GOOGLEDOCS_REPLACE_ALL_TEXT`

## Error Handling

| Error | Solution |
|-------|----------|
| Document not found | Use `GOOGLEDOCS_SEARCH_DOCUMENTS` to find by name |
| Permission denied | Check sharing permissions or re-authenticate |
| Invalid index | Get document structure first to find valid insert positions |
