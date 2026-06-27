"""PhaseRing — Phase 0-5 progress ring.

opencode style:
- 6 phases, each with status icon + progress bar + label
- States: pending · running · done · error
- Colors distinguished by phase index
"""

from textual.widgets import Static

from opencode_tui.theme import (
    phase_label, PHASE_COLORS,
    TEXT, TEXT_MUTED, BG_PANEL, SUCCESS, ERROR,
)


class PhaseRing(Static):
    """Phase 0-5 progress."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._phases = {i: "pending" for i in range(6)}
        self._current = -1

    def on_mount(self):
        self._render()

    def set_phase(self, idx: int, status: str):
        self._phases[idx] = status
        if status == "running":
            self._current = idx
        self._render()

    def set_from_state(self, state: dict):
        status = state.get("status", "idle")

        if status == "running":
            started = state.get("phase_started_at")
            if started:
                try:
                    import datetime as _dt
                    started_dt = _dt.datetime.fromisoformat(started)
                    age = (_dt.datetime.now(_dt.timezone.utc) - started_dt).total_seconds()
                    if age > 120:
                        status = "idle"
                except Exception:
                    pass

        if status != "running":
            self._phases = {i: "pending" for i in range(6)}
            self._current = -1
        else:
            current = state.get("current_phase", 0)
            completed = state.get("completed_phases", [])
            for i in range(6):
                if i in completed:
                    self._phases[i] = "done"
                elif i == current:
                    self._phases[i] = "running"
                else:
                    self._phases[i] = "pending"
            self._current = current
        self._render()

    def reset_all(self):
        self._phases = {i: "pending" for i in range(6)}
        self._current = -1
        self._render()

    def _render(self):
        lines = ["[bold #61afef]── Phase Progress ──[/]"]
        for i in range(6):
            label = phase_label(i)
            color = PHASE_COLORS.get(i, TEXT_MUTED)
            state = self._phases.get(i, "pending")

            if state == "done":
                icon = "[bold #7fd88f]✓[/]"
                bar = f"[#7fd88f]{'─' * 12}[/]"
                tag = f"[#7fd88f]{label}[/]"
            elif state == "running":
                icon = f"[bold {color}]▸[/]"
                bar = f"[{color}]{'█' * 6}{'─' * 6}[/]"
                tag = f"[bold {color}]{label}[/]"
            elif state == "error":
                icon = "[bold #e06c75]✗[/]"
                bar = f"[#e06c75]{'─' * 12}[/]"
                tag = f"[#e06c75]{label}[/]"
            else:
                icon = "[dim]·[/]"
                bar = f"[#484848]{'─' * 12}[/]"
                tag = f"[#808080]{label}[/]"

            lines.append(f"  P{i} {icon} {bar} {tag}")

        self.update("\n".join(lines))

    @property
    def current_phase(self) -> int:
        return self._current
