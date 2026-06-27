"""PromptInput — bottom input bar.

opencode style:
- ┃ left border (gray #484848, gradients to agent color when active)
- backgroundElement (#1e1e1e) uniform base
- textarea + meta row inside a bordered container
- bottom status bar (borderless): spinner / agent·model·provider / shortcut hints
"""

from textual.widgets import TextArea, Static
from textual.reactive import reactive
from textual.containers import Vertical
from textual._text_area_theme import TextAreaTheme
from rich.style import Style

from opencode_tui.theme import (
    ACCENT, TEXT, TEXT_MUTED,
    BG_ROOT, BG_PANEL, BG_ELEMENT, BORDER,
)


_OPENCODE_TEXTAREA_THEME = TextAreaTheme(
    name="opencode-input",
    base_style=Style(color="#eeeeee", bgcolor="#1e1e1e"),
    cursor_style=Style(color="#1e1e1e", bgcolor="#808080"),
    cursor_line_style=Style(bgcolor="#2a2a2a"),
    selection_style=Style(bgcolor="#484848"),
)


COMMANDS = {
    "/help":   "Show command list",
    "/clear":  "Clear chat",
    "/mode":   "Switch backend (redis/opencode)",
    "/status": "View pipeline status",
    "/connect": "Reconnect backend",
    "/diag":   "Diagnostic info",
}


class PromptInput(Vertical):
    """Bottom input bar."""

    _busy = reactive(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent = "executor"
        self._model = "deepseek-v4-flash"
        self._provider = "zen"

    def compose(self):
        with Vertical(id="input-box"):
            yield TextArea("", id="input-textarea")
            yield Static("", id="input-hint")
        yield Static("", id="input-status")
        yield Static("", id="cmd-suggest")

    def on_mount(self):
        ta = self.query_one("#input-textarea", TextArea)
        ta.register_theme(_OPENCODE_TEXTAREA_THEME)
        ta.theme = "opencode-input"
        self._update_hint()

    def on_text_area_changed(self, event: TextArea.Changed):
        if event.text_area.id != "input-textarea":
            return
        text = event.text_area.text
        if text.startswith("/"):
            self._show_suggestions(text)
        else:
            self._hide_suggestions()

    def _show_suggestions(self, text: str):
        prefix = text.lower()
        matches = [f"  {c}  {d}" for c, d in COMMANDS.items() if c.startswith(prefix)]
        sg = self.query_one("#cmd-suggest", Static)
        if matches:
            sg.update(f"[dim {TEXT_MUTED}]{chr(10).join(matches)}[/]")
        else:
            sg.update("")

    def _hide_suggestions(self):
        self.query_one("#cmd-suggest", Static).update("")

    def _update_hint(self):
        hint = self.query_one("#input-hint", Static)
        if self._busy:
            hint.update(f"[dim {TEXT_MUTED}]⠋ Thinking...[/]")
        else:
            hint.update(
                f"[{TEXT_MUTED}]{self._agent}[/]"
                f" [dim {TEXT_MUTED}]·[/]"
                f" [dim {TEXT_MUTED}]{self._model}[/]"
                f" [dim {TEXT_MUTED}]· {self._provider}[/]"
            )

    def watch__busy(self, busy: bool):
        self._update_hint()
        st = self.query_one("#input-status", Static)
        if busy:
            st.update(
                f"[dim {TEXT_MUTED}]⠋ Thinking   esc to abort[/]"
            )
        else:
            st.update(
                f"[dim {TEXT_MUTED}]/help for commands[/]"
            )

    def set_busy(self, busy: bool):
        self._busy = busy
