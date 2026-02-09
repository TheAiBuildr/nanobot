"""Composio type definitions for internal use."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ComposioToolInfo:
    """Information about a discovered Composio tool."""
    slug: str
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)
