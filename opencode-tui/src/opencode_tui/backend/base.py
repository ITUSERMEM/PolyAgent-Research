"""Abstract Backend interface.

The TUI does not directly consume Redis pub/sub or opencode SSE.
All events flow through the `Backend` interface's `subscribe` method,
forwarded by the App layer as Textual Messages.
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class Backend(ABC):
    """Backend interface — TUI switches backends without knowing concrete implementation."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to backend, return success status."""
        ...

    @abstractmethod
    async def disconnect(self):
        ...

    @abstractmethod
    async def send_message(self, text: str) -> str:
        """Send user message, return message ID."""
        ...

    @abstractmethod
    async def subscribe(self) -> AsyncIterator[dict]:
        """Subscribe to event stream. Each yield returns an event dict.

        THIS IS THE TUI'S SINGLE DATA SOURCE.
        The App layer reads events here → converts to Textual Message → updates widgets.
        """
        ...

    @abstractmethod
    async def get_phase_state(self) -> dict:
        ...

    @abstractmethod
    async def get_cost_summary(self) -> dict:
        ...

    @abstractmethod
    async def get_gate_results(self) -> dict:
        ...

    @abstractmethod
    async def get_project_info(self) -> dict:
        ...

    @abstractmethod
    async def get_available_agents(self) -> list[dict]:
        ...

    @abstractmethod
    async def get_available_models(self) -> list[dict]:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...
