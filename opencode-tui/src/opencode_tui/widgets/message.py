"""Message rendering — opencode-style chat bubbles.

Each line starts with ┃ left border, background layered by message role:
- user: backgroundPanel + primary border
- assistant: backgroundPanel + secondary border
- system: backgroundPanel + muted border

Uses Rich Table for zero-gap ┃ + content layout.
"""

from datetime import datetime

from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from textual.widgets import Static

from opencode_tui.theme import (
    SECONDARY, TEXT, TEXT_MUTED,
    BG_PANEL, BG_ROOT, BORDER, SUCCESS, ERROR,
)


def bar_message(
    text: str,
    *,
    bar_color: str = TEXT,
    text_color: str = TEXT,
    bg: str = BG_PANEL,
    bold: bool = False,
) -> Table:
    """Generate a Rich Table with ┃ left border, zero spacing."""
    table = Table.grid(padding=0)
    table.add_column(width=1)
    table.add_column(ratio=1)
    style = f"bold {bar_color}" if bold else bar_color
    row_style = f"bold {text_color} on {bg}" if bold else f"{text_color} on {bg}"
    table.add_row(Text("┃", style=style), Text(text, style=row_style))
    return table


def user_message(text: str) -> Table:
    return bar_message(text, bar_color=TEXT, text_color=TEXT, bg=BG_PANEL)


def assistant_message(text: str) -> Table:
    return bar_message(text, bar_color=SECONDARY, text_color=TEXT, bg=BG_PANEL)


def system_message(text: str, urgent: bool = False) -> Table:
    c = ERROR if urgent else TEXT_MUTED
    return bar_message(text, bar_color=c, text_color=c, bg=BG_ROOT)


def tool_header(icon: str, title: str, *, color: str = SECONDARY) -> Table:
    """Tool call header line."""
    table = Table.grid(padding=0)
    table.add_column(width=1)
    table.add_column(ratio=1)
    table.add_row(
        Text("┃", style=f"bold {color}"),
        Text(f"{icon} {title}", style=f"bold {color} on {BG_PANEL}"),
    )
    return table


def tool_output(text: str, *, color: str = TEXT_MUTED) -> Table:
    """Tool call output content line."""
    table = Table.grid(padding=0)
    table.add_column(width=1)
    table.add_column(ratio=1)
    table.add_row(
        Text("┃", style=TEXT_MUTED),
        Text(text, style=f"{color} on {BG_PANEL}"),
    )
    return table


def message_footer(agent: str, model: str, duration: float) -> Table:
    """Message footer: ▣ agent · model · duration"""
    dur = f"{duration:.1f}s" if duration else ""
    text = f"▣ {agent} · {model}"
    if dur:
        text += f" · {dur}"
    return bar_message(text, bar_color=TEXT_MUTED, text_color=TEXT_MUTED, bg=BG_PANEL)
