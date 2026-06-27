# opencode-tui

Python TUI dashboard blending opencode visual style with dual-backend support (Redis / opencode HTTP API).

## Quick Start

### Installation

```bash
cd /home/opencode/ATTM/opencode-tui
pip install -e .
```

### Start (Redis Mode)

```bash
python -m opencode_tui
```

Connects to an existing Redis pipeline. Left panel: chat + right panel: dashboard (PhaseRing/CostBudget/GateStatus/AgentActivity).

### Start (OpenCode Mode)

```bash
# Terminal 1: start the opencode server first
opencode serve --port 4096

# Terminal 2: launch TUI
cd /home/opencode/ATTM/opencode-tui
python -m opencode_tui --mode opencode
```

The TUI connects to opencode via HTTP/SSE, sends prompts to the LLM, and streams responses.

### Startup Arguments

| Argument | Default | Description |
|---|---|---|
| `--redis` | `redis://localhost:6379` | Redis URL |
| `--mode` | `redis` | Default backend (redis/opencode) |

---

## TUI Usage

### Screen Layout

```
+---------------------------------+---------------------+
|  Header (clock)                 |                     |
+---------------------------------+                     |
|  Chat Panel                     |  Sidebar            |
|                                 |                     |
|  | User Message (| primary bar) |  ProjectInfo        |
|  | stream text (live append)   |  -- Phase --        |
|  | cog bash: command            |  P0 Environment     |
|  |   output                     |  P1 Literature      |
|  | agent model 12s             |  P2 Method Design   |
|                                 |  -- Budget --       |
|  | User Message                 |  Session ####.. 42% |
|  | Received (demo mode)         |  Cost $0.1125       |
|                                 |  -- Gate --         |
|  +-------------------------+   |  G1 PASS Novelty    |
|  | Input message...        |   |  G2 PASS Experiment |
|  | executor deepseek...    |   |  -- Activity --     |
|  +-------------------------+   |  Environment Ready  |
+---------------------------------+  G1 Novelty PASS   |
|  Footer (opencode-tui 1.0)    |                     |
+---------------------------------+---------------------+
```

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` | Send message |
| `Esc` | Focus input |
| `Ctrl+L` | Clear chat |
| `q` | Quit |

### TUI Commands

Type these in the input field:

| Command | Action |
|---|---|
| `/help` | Show all commands |
| `/clear` | Clear chat history |
| `/mode redis` | Switch to Redis backend |
| `/mode opencode` | Switch to opencode backend |
| `/status` | View connection status and backend info |
| `/connect` | Reconnect to current backend |
| `/diag` | Diagnostic info (phase/cost/gate/budget details) |

Backend switch example:

```
/mode opencode   -> switches to opencode, auto-connects to :4096
/mode redis      -> switches back to Redis, auto-connects to localhost:6379
/status          -> shows "opencode (connected)"
```

### Sending Messages

- Non-command text sends on Enter
- Redis mode: message published to `academic:inbox`, processed by pipeline
- OpenCode mode: sends prompt to current session, LLM reply streams into chat
- No backend connection: local echo demo mode

### Dashboard Widgets

| Widget | Content | Data Source |
|---|---|---|
| **ProjectInfo** | Project title + connection status + backend mode | poll 3s or event |
| **PhaseRing** | 6-phase progress icons: pending / running / done / error | poll 3s or event |
| **CostBudget** | Session/Task progress bar + cumulative USD cost | poll 3s |
| **GateStatus** | 7 gate reviews: PASS/REVISE/FAIL + fusion | poll 3s or event |
| **AgentActivity** | Real-time agent/gate/budget event log, color-coded by tier | real-time event |

---

## OpenCode Integration

opencode-tui ships with a complete `.opencode/` configuration, usable directly in opencode.

### Register with opencode

Reference or copy in your opencode project directory:

```jsonc
// opencode.jsonc or .opencode/opencode.jsonc
{
  "mcp": {
    "academic-pipeline": {
      "type": "local",
      "command": ["python", "-m", "academic_mcp.academic_server"],
      "cwd": "/home/opencode/ATTM/opencode-tui"
    }
  }
}
```

### Agents (Native opencode Scheduling)

6 agent definitions in `.opencode/agent/`, auto-discovered on opencode startup:

| Agent | Model | Role | Allowed Tools |
|---|---|---|---|
| `literature-researcher` | deepseek-v4-flash | Literature search and survey | Bash, Read, WebFetch, Grep |
| `methodologist` | deepseek-v4-pro | Method design | Bash, Read, Write, WebFetch |
| `code-engineer` | deepseek-v4-flash | Code implementation | Bash, Read, Edit, Write, Grep |
| `visualization-designer` | deepseek-v4-flash | Visualization output | Bash, Read, Edit, Write |
| `citation-auditor` | deepseek-v4-flash | Citation audit | Bash, Read, WebFetch |
| `academic-editor` | deepseek-v4-pro | Paper polishing | Bash, Read, Edit, Write |

Switch agents in opencode:

```
/agent literature-researcher
/agent code-engineer
```

### Phase Commands

6 slash commands in `.opencode/command/`:

```
/phase0 "Research Title"    # Environment Setup
/phase1                     # Literature Survey
/phase2                     # Method Design
/phase3                     # Experiment Validation
/phase4                     # Code Implementation
/phase5                     # Paper Writing
```

Each command defines specific steps for that phase, executed sequentially by opencode.

### MCP Server (6 Tools)

`academic_mcp/academic_server.py` registered with opencode. Call directly in chat:

```
call research-director to view pipeline status
call experimenter to launch experiment exp_001
call paper-writer to write abstract
call academic-reviewer to review the current paper
```

| Tool | Parameters | Function |
|---|---|---|
| `research-director` | `action: start/status/skip/stop` | Pipeline orchestration |
| `experimenter` | `action: design/run/monitor/report` | Experiment management |
| `scientific-computing-engineer` | `action: check_gpu/optimize/profile/fix_numerical` | GPU/compute |
| `paper-writer` | `section: abstract/intro/method/experiments/conclusion/full` | Paper writing |
| `method-reviewer` | `action: review_method/check_novelty/check_reproducibility` | Method review |
| `academic-reviewer` | `review_type: full/novelty/experiments/writing` | Full review |

### Pipeline Skill

`.opencode/skills/pipeline/SKILL.md` defines the full orchestration flow:

```
Phase 0: Environment Setup       -> G1 Academic Novelty
Phase 1: Literature Survey       -> G2 Experiment Design (fusion)
Phase 2: Method Design           -> G3 Methodology
Phase 3: Experiment Validation   -> G4 Data Analysis
Phase 4: Code Implementation     -> G5 Logical Consistency (fusion)
Phase 5: Paper Writing           -> G6 Reproducibility -> G7 Final Review (fusion)
```

Load the skill in opencode:

```
/skill pipeline
```

### Typical Workflow

```text
1. Start opencode serve
2. python -m opencode_tui --mode opencode
3. In TUI: type "Research rotating machinery fault diagnosis"
4. opencode backend creates a session, LLM starts inference
5. TUI displays streaming text, tool calls, and reasoning in real-time
6. Results shown in the chat panel
7. To switch back to Redis pipeline: /mode redis
```

---

## Architecture

```
+---------------------------------------------------+
|            opencode-tui (Python/Textual)            |
|  Chat + PhaseRing + CostBudget + GateStatus        |
|  [/mode redis  |  /mode opencode]                   |
+--------+--------------------------+-----------------+
         |                          |
   +-----v-----+             +------v------+
   |  Redis    |             |  opencode   |
   |  pub/sub  |             |  serve      |
   |  inbox/   |             |  :4096      |
   |  outbox/  |             |  HTTP/SSE   |
   |  progress |             |             |
   +-----+-----+             +------+------+
         |                          |
   +-----v-----+             +------v------+
   |academic_  |             | opencode    |
   |loop.py    |             | agent/*.md  |
   |12 agents  |             | command/*.md|
   |+ MCP srv  |             | + MCP tools |
   +-----------+             +-------------+
```

## Event Flow

### Redis Mode

```
TUI input text -> academic:inbox (pub) -> academic_loop.py
                                        -> academic:progress (pub) -> TUI widget update
                                        -> academic:outbox (pub) -> TUI displays reply
```

### OpenCode Mode

```
TUI input text -> POST /session/:id/message  -> opencode LLM
               -> GET /event (SSE)
               <- message.part.updated (text/tool/reasoning streaming)
               <- session.status (idle -> complete)
               <- permission.asked (auto reply once)
```

## File Structure

```
/home/opencode/ATTM/opencode-tui/
+-- pyproject.toml               # Dependencies: textual, httpx, redis, mcp
+-- src/opencode_tui/             # TUI core code
|   +-- app.py                   # Main App -- layout + event flow + command routing
|   +-- __main__.py              # python -m entry point
|   +-- theme.py / css.py        # opencode palette + CSS
|   +-- backend/                 # Redis / opencode dual backend
|   +-- client/                  # opencode HTTP client + SSE parsing
|   +-- widgets/                 # 7 widgets + spinner + message rendering
+-- academic_mcp/                # Python MCP server (6 tools)
+-- .opencode/                   # opencode integration
|   +-- opencode.jsonc           # provider + mcp + permission config
|   +-- agent/                   # 6 agent definitions
|   +-- command/                 # 6 phase commands
|   +-- skills/pipeline/         # pipeline orchestration skill
+-- tests/                       # 28 tests
```

## Testing

```bash
cd /home/opencode/ATTM/opencode-tui
python -m pytest tests/ -v
```

28 tests:
- SSE parsing (8): single/multi event, comments, empty data, invalid JSON
- Theme tokens (7): primary/secondary/accent/phase/gate/fusion
- Message rendering (9): bar_message/user/assistant/system/tool_header/output/footer
- Event classes (3): PhaseEvent/ChatMessage/BackendStatusEvent
