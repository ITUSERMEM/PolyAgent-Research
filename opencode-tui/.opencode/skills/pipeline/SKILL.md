---
name: pipeline
description: Academic Pipeline orchestration skill. Load this when running multi-phase research workflows: Phase 0 (Environment Setup) → Phase 1 (Literature Survey) → Phase 2 (Method Design) → Phase 3 (Experiment Validation) → Phase 4 (Code Implementation) → Phase 5 (Paper Writing). Each phase uses a specialized agent from the academic team and runs through GateJudge review before transitioning.
---

# Academic Pipeline

## Phase Flow
```
Phase 0: Environment Setup    → G1 Academic Novelty
Phase 1: Literature Survey    → G2 Experiment Design (fusion)
Phase 2: Method Design        → G3 Methodology
Phase 3: Experiment Validation → G4 Data Analysis
Phase 4: Code Implementation  → G5 Logical Consistency (fusion)
Phase 5: Paper Writing        → G6 Reproducibility → G7 Final Review (fusion)
```

## Quick Start
```
/phase0 "research topic"
# or full pipeline
/research "topic description"
```

## Gate Pass Criteria
- G1: Novelty score > 6/10
- G2: Experiment design covers key baselines
- G3: Method technically sound and reproducible
- G4: Results statistically significant
- G5: Claims supported by evidence
- G6: All code and data available
- G7: Paper submission ready

## Fusion Gates (G2, G5, G7)
These require dual-model review. Both models must pass.

## Context
- Pipeline orchestrator: academic_loop.py
- Redis state key: academic:phase:state
- Progress events: academic:progress (pub/sub)
- Agent registration: agent/*.md
- Phase commands: command/*.md
