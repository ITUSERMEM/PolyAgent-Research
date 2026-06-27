"""opencode palette port — 40+ color tokens.

Ported from opencode default theme opencode.json.
All colors verified on dark background.
"""

# ── Brand / Core ─────────────────────────────────────────
PRIMARY = "#fab283"      # Warm peach — primary accent, prompt border, links
SECONDARY = "#5c9cf5"    # Blue — file attachments, secondary accent
ACCENT = "#9d7cd8"       # Purple — Markdown headings, syntax keywords

# ── Status ───────────────────────────────────────────────
ERROR = "#e06c75"        # Red — errors, permission denied
WARNING = "#f5a742"      # Orange — warnings, thinking blocks, in-progress
SUCCESS = "#7fd88f"      # Green — success, MCP connected
INFO = "#56b6c2"         # Cyan — informational notices

# ── Text ─────────────────────────────────────────────────
TEXT = "#eeeeee"         # Primary foreground
TEXT_MUTED = "#808080"   # Secondary/muted text, timestamps, hints

# ── Background (3-layer hierarchy) ───────────────────────
BG_ROOT = "#0a0a0a"       # Deepest canvas
BG_PANEL = "#141414"       # Content blocks (messages, sidebar)
BG_ELEMENT = "#1e1e1e"     # Interactive elements (input, hover)

# ── Borders (5-level gray) ────────────────────────────────
BORDER = "#484848"
BORDER_ACTIVE = "#606060"
BORDER_SUBTLE = "#3c3c3c"

# ── Diff colors ───────────────────────────────────────────
DIFF_ADDED = "#4fd6be"
DIFF_REMOVED = "#c53b53"
DIFF_CONTEXT = "#828bb8"
DIFF_ADDED_BG = "#20303b"
DIFF_REMOVED_BG = "#37222c"
DIFF_CONTEXT_BG = "#141414"
DIFF_LINE_NUM = "#8f8f8f"
DIFF_HUNK_HEADER = "#828bb8"
DIFF_HIGHLIGHT_ADDED = "#b8db87"
DIFF_HIGHLIGHT_REMOVED = "#e26a75"

# ── Markdown ─────────────────────────────────────────────
MD_TEXT = TEXT
MD_HEADING = ACCENT
MD_LINK = PRIMARY
MD_LINK_TEXT = INFO
MD_CODE = SUCCESS
MD_BLOCK_QUOTE = "#e5c07b"
MD_EMPH = "#e5c07b"
MD_STRONG = WARNING
MD_LIST_ITEM = PRIMARY
MD_LIST_ENUM = INFO
MD_CODE_BLOCK = TEXT

# ── Syntax Highlighting ──────────────────────────────────
SYNTAX_COMMENT = "#808080"
SYNTAX_KEYWORD = ACCENT
SYNTAX_FUNCTION = PRIMARY
SYNTAX_VARIABLE = ERROR
SYNTAX_STRING = SUCCESS
SYNTAX_NUMBER = WARNING
SYNTAX_TYPE = "#e5c07b"
SYNTAX_OPERATOR = INFO
SYNTAX_PUNCTUATION = TEXT

# ── Phase (P0-P5) ───────────────────────────────────────
PHASE_COLORS = {
    0: SECONDARY,      # Blue — Environment Init
    1: SECONDARY,      # Blue — Literature Review
    2: ACCENT,         # Purple — Method Design
    3: SUCCESS,        # Green — Experiments
    4: WARNING,        # Orange — Coding
    5: ERROR,          # Rose — Paper Writing
}

PHASE_LABELS = {
    0: "Environment Init",
    1: "Literature Review",
    2: "Method Design",
    3: "Experiments",
    4: "Coding",
    5: "Paper Writing",
}

# ── Gate (G1-G7) ────────────────────────────────────────
GATE_LABELS = {
    1: "Novelty", 2: "Exp. Design", 3: "Methodology",
    4: "Data Analysis", 5: "Consistency", 6: "Reproducibility", 7: "Final Review",
}
FUSION_GATES = {2, 5, 7}

# ── Agent Tier Colors ───────────────────────────────────
TIER_COLORS = {
    "executor": SECONDARY,
    "reviewer": SECONDARY,
    "pro": ACCENT,
}

# ── Event Icons ─────────────────────────────────────────
EVENT_ICONS = {
    "pipeline_start": "🚀", "pipeline_error": "❌",
    "phase_start": "▶", "phase_complete": "✓",
    "agent_start": "▸", "agent_done": "◂",
    "agent_reasoning": "💭", "agent_iter": "◇",
    "agent_skill_select": "🔧", "agent_skill_run": "⚙",
    "agent_skill_ok": "✓", "agent_skill_error": "✗",
    "agent_skill_hang": "⚠", "agent_skill_timeout": "⌛",
    "agent_skill_output": "📄", "agent_skip_skill": "⏭",
    "budget_degrade": "↓", "budget_stop": "⛔",
    "gate_pass": "PASS", "gate_revise": "REVISE", "gate_fail": "FAIL",
    "heartbeat_ok": "♥", "heartbeat_alert": "💔",
}

# ── Helper ──────────────────────────────────────────────
def phase_label(idx: int) -> str:
    return PHASE_LABELS.get(idx, f"Phase {idx}")


def phase_color(idx: int) -> str:
    return PHASE_COLORS.get(idx, TEXT_MUTED)


def tier_color(tier: str) -> str:
    return TIER_COLORS.get(tier, TEXT)
