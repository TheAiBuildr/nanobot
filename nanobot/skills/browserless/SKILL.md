---
name: browserless
description: "Web scraping, screenshots, PDF generation, and browser automation via Browserless. Use when the user needs to (1) take a screenshot of a webpage, (2) scrape or extract data from JavaScript-rendered pages, (3) generate a PDF from a URL, (4) fetch HTML content from dynamic sites, or (5) automate multi-step browser interactions."
---

# Browserless

Browser automation and web scraping for JavaScript-rendered content, screenshots, and PDFs.

## Quick Start

When the user says:
- "Screenshot this page"
- "Scrape data from [URL]"
- "Save this page as PDF"
- "Get the HTML from [URL]"

## Core Operations

### Screenshot

```
mcp__composio_BROWSERLESS_TAKE_SCREENSHOT(
    url="https://example.com"
)
```

Captures a viewport or full-page screenshot. Supports PNG, JPEG, WebP.

### Scrape Structured Data

```
mcp__composio_BROWSERLESS_SCRAPE_CONTENT(
    url="https://example.com/products",
    selectors={"name": ".product-name", "price": ".price"}
)
```

Extracts elements matching CSS selectors from a JavaScript-rendered page.

### Fetch HTML

```
mcp__composio_BROWSERLESS_FETCH_HTML_CONTENT(
    url="https://example.com"
)
```

Returns the full rendered HTML (after JS execution). Use when you need raw page content.

### Generate PDF

```
mcp__composio_BROWSERLESS_GENERATE_PDF(
    url="https://example.com/report"
)
```

Converts a webpage to PDF with configurable page size and margins.

### Unblock Protected Content

```
mcp__composio_BROWSERLESS_UNBLOCK_PROTECTED_CONTENT(
    url="https://example.com"
)
```

Accesses content from sites with bot-protection mechanisms. Use as a fallback when standard fetch is blocked.

### Custom Puppeteer Script

```
mcp__composio_BROWSERLESS_EXECUTE_CUSTOM_FUNCTION(
    code="...",
    url="https://example.com"
)
```

Runs arbitrary Puppeteer code for complex multi-step automation (login flows, form filling, navigation sequences).

## When to Use vs web_search

| web_search | browserless |
|------------|-------------|
| Research across multiple sources | Known specific URL |
| Quick facts and summaries | JavaScript-rendered content |
| General knowledge queries | Screenshots, PDFs, structured extraction |

## Error Handling

| Error | Solution |
|-------|----------|
| Timeout | Increase wait time or use `wait_for` selector |
| Blocked by bot protection | Use `BROWSERLESS_UNBLOCK_PROTECTED_CONTENT` |
| JS rendering incomplete | Add delay or wait for specific selector |
| Rate limited | Add delays between requests |
