"""GateStatus — 7-gate review status grid.

Each gate displays verdict (PASS/REVISE/FAIL) or pending.
Fusion gates (G2/G5/G7) marked with ⚡.
"""

from textual.widgets import Static

from opencode_tui.theme import (
    TEXT, TEXT_MUTED, SUCCESS, ERROR, SECONDARY, FUSION_GATES,
)


VERDICT_COLORS = {
    "pass": SUCCESS,
    "revise": SECONDARY,
    "fail": ERROR,
    "pending": TEXT_MUTED,
}

VERDICT_LABELS = {
    "pass": "PASS",
    "revise": "REVISE",
    "fail": "FAIL",
    "pending": "··",
}

GATE_LABELS = {
    1: "Novelty", 2: "Exp. Design", 3: "Methodology",
    4: "Data Analysis", 5: "Consistency", 6: "Reproducibility", 7: "Final Review",
}


class GateStatus(Static):
    """Gate review status panel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._gates: dict[int, str] = {}

    def on_mount(self):
        self._render()

    def update_gate(self, gate_id: int, verdict: str):
        self._gates[gate_id] = verdict
        self._render()

    def load_from_state(self, results: dict):
        for key, val in results.items():
            try:
                gid = int(key.replace("phase", "").replace("gate", "").split("_")[-1])
                self._gates[gid] = val.get("verdict", "pending")
            except (ValueError, KeyError):
                pass
        self._render()

    def _render(self):
        lines = ["[bold #61afef]── Gate Status ──[/]"]
        for gid in range(1, 8):
            verdict = self._gates.get(gid, "pending")
            color = VERDICT_COLORS.get(verdict, TEXT_MUTED)
            label = VERDICT_LABELS.get(verdict, "··")
            name = GATE_LABELS.get(gid, f"G{gid}")
            fusion = " ⚡" if gid in FUSION_GATES else ""
            lines.append(
                f"  G{gid} [{color}]{label:>5}[/]"
                f" [dim {TEXT_MUTED}]{name}{fusion}[/]"
            )
        self.update("\n".join(lines))
