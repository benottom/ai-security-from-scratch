# Phase 8 — Defensive Controls

> **Classes:** 45–50 | **Estimated Total Time:** ~21 hours

## Phase Description

This phase shifts from analysis to construction: learners build the core defensive controls that form the supervisory layer of any secure AI system. Each control is implemented from scratch — not as a library call, but as a deterministic, auditable mechanism that the learner understands end-to-end. The phase covers five essential control families: guardrails that enforce safety boundaries on inputs and outputs, policy-as-code systems that make security rules versioned and testable, output validation layers that independently verify model responses, context firewalls that separate instruction channels from data channels, and the AI security gateway that orchestrates all controls into a unified defense. It culminates in circuit breakers and kill switches — the automated safety mechanisms that halt the system when controls are overwhelmed. The key principle is that every control must be external to the model, deterministic in operation, and auditable in decision.

## Main Outcome

Learners can design layered supervisory controls — building deterministic, auditable safety mechanisms that operate independently of the model and can override it when necessary.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 45 | Guardrails from Scratch | Builds input and output guardrails as deterministic safety layers external to the model |
| 46 | Policy as Code | Implements security policies as versioned, testable, and auditable code rather than prompt instructions |
| 47 | Output Validation | Constructs independent output classification and verification systems that run after generation |
| 48 | Context Firewalls | Separates instruction channels from data channels in the LLM context window to prevent injection |
| 49 | AI Security Gateway | Designs a centralized security gateway that orchestrates all controls for every AI system interaction |
| 50 | Circuit Breakers and Kill Switches | Implements automated safety shutdown mechanisms that halt the system when controls are overwhelmed |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
- Completion of Phases 3–7 recommended for full context on what the controls must defend against
