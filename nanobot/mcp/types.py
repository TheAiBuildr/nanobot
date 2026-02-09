"""MCP type definitions for internal use."""

from dataclasses import dataclass
from typing import Any


@dataclass
class MCPToolInfo:
    """Information about a discovered MCP tool."""
    server_name: str
    name: str
    description: str
    input_schema: dict[str, Any]
