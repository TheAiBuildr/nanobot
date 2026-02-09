"""Progress notifier for long-running agent tasks.

Sends automatic "working on it" acknowledgments when processing
takes longer than a configurable threshold.
"""

import asyncio
from typing import Any

from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus


class ProgressNotifier:
    """
    Timer-based progress notifier.

    Starts a background timer when the agent begins processing a message.
    If the agent hasn't finished within ``delay_seconds``, an automatic
    acknowledgment is sent to the originating channel/thread so the user
    knows the bot is still working.
    """

    def __init__(self, bus: MessageBus, delay_seconds: float = 10.0):
        self.bus = bus
        self.delay = delay_seconds
        self._task: asyncio.Task[None] | None = None

    async def start(
        self,
        channel: str,
        chat_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Start the progress timer.

        If :meth:`cancel` is not called before *delay_seconds* elapse,
        a brief progress message is published to the outbound bus.
        """
        self._task = asyncio.create_task(
            self._delayed_notify(channel, chat_id, metadata or {})
        )

    async def cancel(self) -> None:
        """Cancel the pending progress notification (response was fast enough)."""
        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None

    async def _delayed_notify(
        self,
        channel: str,
        chat_id: str,
        metadata: dict[str, Any],
    ) -> None:
        """Wait for the delay, then send a progress acknowledgment."""
        try:
            await asyncio.sleep(self.delay)
        except asyncio.CancelledError:
            return

        logger.debug(f"Progress: auto-acknowledging to {channel}:{chat_id}")
        msg = OutboundMessage(
            channel=channel,
            chat_id=chat_id,
            content="Working on it\u2026",
            metadata=metadata,
            is_progress=True,
        )
        try:
            await self.bus.publish_outbound(msg)
        except Exception as e:
            logger.warning(f"Progress: failed to send acknowledgment: {e}")
