"""AgentActivity — real-time event stream log.

All agent/gate/budget events appended in chronological order.
Colors distinguished by agent tier (executor/reviewer/pro).
"""

from textual.widgets import RichLog

from opencode_tui.theme import (
    TEXT, TEXT_MUTED, BG_PANEL, BG_ROOT,
    SECONDARY, ACCENT,
)


TIER_COLORS = {
    "executor": SECONDARY,
    "reviewer": SECONDARY,
    "pro": ACCENT,
}

MAX_LINES = 100


class AgentActivity(RichLog):
    """Real-time event stream."""

    def __init__(self, **kwargs):
        super().__init__(
            highlight=True,
            markup=True,
            max_lines=MAX_LINES,
            wrap=True,
            **kwargs,
        )

    def append_event(self, text: str, tier: str = ""):
        color = TIER_COLORS.get(tier, TEXT_MUTED)
        self.write(f"[dim {color}]·[/] [{color}]{text}[/]")
