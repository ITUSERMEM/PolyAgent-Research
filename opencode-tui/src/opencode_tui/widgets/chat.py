"""ChatPanel — streaming message rendering.

Supports:
- completed messages: appended directly
- streaming messages: start → update → end real-time update on same line
- tool blocks: standalone Static widget for independent updates
"""

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static
from textual.widgets._static import RenderableType

from opencode_tui.theme import TEXT_MUTED


class ChatPanel(VerticalScroll):
    """Chat panel — streaming message list."""

    MAX_MESSAGES = 200

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stream_widget: Static | None = None
        self._msg_count = 0

    def write(self, content: RenderableType):
        """Append a completed message."""
        self._add_msg(Static(content, classes="message-block"))

    def start_stream(self, content: RenderableType = ""):
        """Start a streaming message."""
        self._stream_widget = Static(content, classes="message-block streaming")
        self._add_msg(self._stream_widget)

    def update_stream(self, content: RenderableType):
        """Update the current streaming message."""
        if self._stream_widget:
            self._stream_widget.update(content)
            self.scroll_end()

    def end_stream(self, content: RenderableType | None = None):
        """End the streaming message (becomes a completed message)."""
        if self._stream_widget:
            if content is not None:
                self._stream_widget.update(content)
            self._stream_widget.remove_class("streaming")
            self._stream_widget = None
        self.scroll_end()

    def write_stream(self, text: str, finished: bool = False):
        """Convenience: append a line of streaming text.

        When finished=True, ends the stream; otherwise appends to it.
        """
        content = f"[dim {TEXT_MUTED}]┃[/] {text}"
        if self._stream_widget is None:
            self.start_stream(content)
        elif finished:
            self.end_stream(content)
        else:
            self.update_stream(content)

    def tool_block(self, icon: str, title: str, output: str = "", status: str = "running"):
        """Render a tool call block."""
        icon_color = {"running": "#5c9cf5", "ok": "#7fd88f", "error": "#e06c75"}
        color = icon_color.get(status, "#808080")
        lines = [f"[dim {color}]┃[/] [{color}]{icon} {title}[/]"]
        if output:
            lines.append(f"[dim {TEXT_MUTED}]┃[/] [dim]{output[:200]}[/]")
        self.write("\n".join(lines))

    def write_bar(self, text: str, bar_color: str, text_color: str = "#eeeeee"):
        """Single-line message with ┃ left border."""
        self.write(f"[bold {bar_color}]┃[/] [{text_color}]{text}[/]")

    def clear(self):
        self._stream_widget = None
        self._msg_count = 0
        self.remove_children()

    def _add_msg(self, widget: Static):
        self.mount(widget)
        self._msg_count += 1
        self.scroll_end()
        if self._msg_count > self.MAX_MESSAGES:
            children = list(self.children)
            if len(children) > self.MAX_MESSAGES:
                to_remove = children[: len(children) - self.MAX_MESSAGES]
                for w in to_remove:
                    w.remove()
