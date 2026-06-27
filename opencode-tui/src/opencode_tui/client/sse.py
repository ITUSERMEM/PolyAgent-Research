"""SSE (Server-Sent Events) stream parser.

opencode uses SSE to push real-time events:
  event: message
  data: {"id":"evt_...","type":"event_type","properties":{...}}

Each message is delimited by a blank line.
"""

import json
from dataclasses import dataclass, field
from typing import AsyncIterator


@dataclass
class SSEEvent:
    id: str = ""
    type: str = ""
    properties: dict = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: dict) -> "SSEEvent":
        return cls(
            id=data.get("id", ""),
            type=data.get("type", ""),
            properties=data.get("properties", {}),
        )


class SSEClient:
    """SSE stream parser."""

    @staticmethod
    async def iter_events(response) -> AsyncIterator[SSEEvent]:
        """Iterate SSE events from an httpx stream response."""
        buffer = ""
        async for chunk in response.aiter_text():
            buffer += chunk
            while "\n\n" in buffer or "\r\n\r\n" in buffer:
                if "\r\n\r\n" in buffer:
                    block, buffer = buffer.split("\r\n\r\n", 1)
                else:
                    block, buffer = buffer.split("\n\n", 1)
                event = SSEClient._parse_block(block)
                if event is not None:
                    yield event

    @staticmethod
    def _parse_block(block: str) -> SSEEvent | None:
        lines = block.strip().split("\n")
        event_type = "message"
        data_lines: list[str] = []
        for line in lines:
            line = line.strip()
            if line.startswith("event:"):
                event_type = line[6:].strip()
            elif line.startswith("data:"):
                data_lines.append(line[5:].strip())
            elif line.startswith(":"):
                continue

        if not data_lines:
            return None

        raw = "".join(data_lines)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None

        if event_type == "message":
            return SSEEvent.from_data(data)

        return SSEEvent(
            id=data.get("id", ""),
            type=event_type,
            properties=data.get("properties", {}),
        )
