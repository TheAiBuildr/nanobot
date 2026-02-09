---
name: google-drive
description: "Google Drive file management via Composio. Use when the user needs to (1) upload, download, or create files on Google Drive, (2) search for files or folders, (3) share files with specific permissions, (4) organize files into folders, (5) manage comments or revisions, or (6) work with shared drives."
---

# Google Drive

File storage, sharing, and organization on Google Drive.

## Quick Start

When the user says:
- "Upload this file to Drive"
- "Create a document on Drive"
- "Share this file with [email]"
- "Find my [file] on Drive"
- "Create a folder for [project]"

## Core Operations

### Create File from Text

```
mcp__composio_GOOGLEDRIVE_CREATE_FILE_FROM_TEXT(
    file_name="report.txt",
    content="File content here",
    mime_type="text/plain"
)
```

Creates a new file (up to 10MB) from text content. Supports various MIME types.

### Upload File

```
mcp__composio_GOOGLEDRIVE_UPLOAD_FILE(
    file_path="/path/to/file.pdf",
    folder_id="optional-folder-id"
)
```

Uploads a local file (max 5MB) to Drive. Specify `folder_id` to target a folder.

### Download File

```
mcp__composio_GOOGLEDRIVE_DOWNLOAD_FILE(
    file_id="file-id"
)
```

Downloads a file by ID. Google Workspace files are exported to a compatible format.

### Search for Files

```
mcp__composio_GOOGLEDRIVE_FIND_FILE(
    query="quarterly report"
)
```

Searches files and folders by name or content.

### Create Folder

```
mcp__composio_GOOGLEDRIVE_CREATE_FOLDER(
    folder_name="Project Assets",
    parent_folder_id="optional-parent-id"
)
```

### Share File

```
mcp__composio_GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE(
    file_id="file-id",
    role="reader",
    type="user"
)
```

Roles: `reader`, `writer`, `commenter`, `owner`. Types: `anyone`, `user`, `group`, `domain`.

### Move File

```
mcp__composio_GOOGLEDRIVE_MOVE_FILE(
    file_id="file-id",
    folder_id="destination-folder-id"
)
```

## Other Useful Tools

- `GOOGLEDRIVE_LIST_FILES` -- list files in a folder or search with filters
- `GOOGLEDRIVE_FIND_FOLDER` -- find a folder by name
- `GOOGLEDRIVE_COPY_FILE` -- duplicate a file
- `GOOGLEDRIVE_EDIT_FILE` -- overwrite file content
- `GOOGLEDRIVE_GET_FILE_METADATA` -- get metadata (name, size, modified date, etc.)
- `GOOGLEDRIVE_LIST_PERMISSIONS` -- list who has access
- `GOOGLEDRIVE_DELETE_PERMISSION` -- revoke access
- `GOOGLEDRIVE_CREATE_COMMENT` / `GOOGLEDRIVE_LIST_COMMENTS` -- file comments
- `GOOGLEDRIVE_LIST_REVISIONS` -- version history
- `GOOGLEDRIVE_EMPTY_TRASH` / `GOOGLEDRIVE_UNTRASH_FILE` -- trash management
- `GOOGLEDRIVE_LIST_SHARED_DRIVES` / `GOOGLEDRIVE_CREATE_DRIVE` -- shared drives

## Workflow Patterns

### Save and Share
1. Create file with `GOOGLEDRIVE_CREATE_FILE_FROM_TEXT`
2. Share with `GOOGLEDRIVE_ADD_FILE_SHARING_PREFERENCE`
3. Return the file link to the user

### Organize Project Files
1. Create project folder with `GOOGLEDRIVE_CREATE_FOLDER`
2. Upload/create files into the folder
3. Share the folder for team access

## Error Handling

| Error | Solution |
|-------|----------|
| File not found | Use `GOOGLEDRIVE_FIND_FILE` to search by name |
| Permission denied | Check sharing settings or re-authenticate |
| File too large | Upload limit is 5MB; split or compress |
| Folder not found | Create it first with `GOOGLEDRIVE_CREATE_FOLDER` |
