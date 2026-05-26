# AI Content Agents

An AI-agent-assisted content pipeline for the **AI Security from Scratch** curriculum. Each agent is a specialized prompt specification that, when invoked against a capable LLM, produces draft content following strict formatting, safety, and quality constraints. Humans validate every output before merge.

## Architecture

The pipeline is organized as a **stage-gate workflow**: each agent produces a deliverable that feeds the next agent. No stage can be skipped. Every output must pass human review before the next stage begins.

```
Curriculum Architect ──► Lesson Writer ──┐
       │                                 │
       ▼                                 ▼
  Lab Builder ──────► Red-Team Scenario ──► Blue-Team Defense
       │                                 │          │
       ▼                                 ▼          ▼
  Test Engineer ◄───────────────────────────────────┘
       │
       ▼
  Assurance Agent ──► Technical Reviewer ──► Editor ──► Maintainer
```

## The 10 Agents

| # | Agent | Purpose | Primary Input | Primary Output |
|---|-------|---------|---------------|----------------|
| 1 | **Curriculum Architect** | Turns the roadmap into per-class specifications | Roadmap document | `class-spec.yaml` |
| 2 | **Lesson Writer** | Writes educational explanations and walkthroughs | Class spec | `lesson.md` |
| 3 | **Lab Builder** | Creates vulnerable and patched application pairs | Class spec | `app.py` (vuln + patched) |
| 4 | **Red-Team Scenario** | Creates safe, constrained attack scripts | Vulnerable app | `attack.py` |
| 5 | **Blue-Team Defense** | Designs mitigations and control implementations | Attack + vuln app | `defense.py` + control mapping |
| 6 | **Test Engineer** | Turns attacks into automated, repeatable tests | Attack + patched app | `test_*.py` |
| 7 | **Assurance Agent** | Creates professional evidence and audit artifacts | Test results + controls | `assurance-report.md` |
| 8 | **Technical Reviewer** | Reviews correctness, safety, and completeness | All class artifacts | Review checklist with pass/fail |
| 9 | **Editor** | Polishes content for clarity, consistency, and voice | Lesson + all markdown | Final markdown |
| 10 | **Maintainer** | Keeps content up-to-date, checks links, validates consistency | Entire repo | Maintenance PRs |

## Workflow Rules

1. **Human-in-the-loop at every gate.** Agents produce drafts; a human reviewer must approve before the next agent runs.
2. **Safety markers are mandatory.** Every attack file must contain `<!-- SAFETY: ... -->` markers describing scope and constraints.
3. **No real external targets.** All attacks run against localhost services bundled with the lab. No outbound network calls.
4. **Deterministic where possible.** Seed random generators. Pin dependency versions. Tests must be reproducible.
5. **Control-theoretic framing.** Every class must map its content to a control-loop model: sensor → estimator → controller → actuator → plant.
6. **Patch-before-publish.** No vulnerable code is merged without its corresponding patched version and passing tests.
7. **Evidence trail.** Every class produces an assurance report linking controls → tests → evidence.

## How to Use an Agent

Each agent specification file (`.md`) contains:

- **Purpose** — what the agent does and why it exists
- **Input format** — the exact shape of data the agent expects
- **Output format** — the exact shape of data the agent must produce
- **Constraints** — hard rules the agent must never violate
- **Prompt skeleton** — a copy-paste-ready prompt you can feed to an LLM

To use:

1. Read the agent's `.md` file
2. Gather the required inputs
3. Fill in the prompt skeleton with your specific context
4. Run the prompt against your LLM
5. Review the output against the constraints checklist
6. If all constraints pass, commit the output; otherwise, iterate

## File Map

```
tools/ai_content_agents/
├── README.md                    ← you are here
├── curriculum_architect.md      ← Agent 1
├── lesson_writer.md             ← Agent 2
├── lab_builder.md               ← Agent 3
├── red_team_scenario.md         ← Agent 4
├── blue_team_defense.md         ← Agent 5
├── test_engineer.md             ← Agent 6
├── assurance_agent.md           ← Agent 7
├── technical_reviewer.md        ← Agent 8
├── editor.md                    ← Agent 9
└── maintainer.md                ← Agent 10
```

## Contributing

To add a new agent:

1. Create a `.md` file following the same structure (Purpose, Input, Output, Constraints, Prompt Skeleton)
2. Update this README's agent table
3. Submit a PR with a test run showing the agent producing valid output

## License

Same as the parent repository.
