"""Progress tool for subagent progress updates.

A restricted messaging tool that lets subagents send brief status
updates back to the user's original channel/thread without giving
them full message-sending capabilities.
"""

from typing import Any, Callable, Awaitable

from nanobot.agent.tools.base import Tool
from nanobot.bus.events import OutboundMessage


class ProgressTool(Tool):
    """
    Tool for subagents to send progress updates to the user.

    Unlike :class:`MessageTool`, this is locked to a single destination
    (the originating channel/chat_id) and marks every message as a
    progress update so channels can style them accordingly.
    """

    def __init__(
        self,
        send_callback: Callable[[OutboundMessage], Awaitable[None]],
        channel: str,
        chat_id: str,
        metadata: dict[str, Any] | None = None,
    ):
        self._send_callback = send_callback
        self._channel = channel
        self._chat_id = chat_id
        self._metadata = metadata or {}

    @property
    def name(self) -> str:
        return "progress"

    @property
    def description(self) -> str:
        return (
            "Send a brief progress update to the user. "
            "Use this to let the user know what you're currently working on, "
            "especially for tasks that involve multiple steps or may take a while."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": (
                        "A short progress message (1-2 sentences). "
                        "Example: 'Searching the web for recent articles...'"
                    ),
                },
            },
            "required": ["content"],
        }

    async def execute(self, content: str, **kwargs: Any) -> str:
        msg = OutboundMessage(
            channel=self._channel,
            chat_id=self._chat_id,
            content=content,
            metadata=self._metadata,
            is_progress=True,
        )
        try:
            await self._send_callback(msg)
            return "Progress update sent."
        except Exception as e:
            return f"Error sending progress update: {e}"
