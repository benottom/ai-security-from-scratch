# Phase 4 — Agent and Tool Security

> **Classes:** 20–26 | **Estimated Total Time:** ~24 hours

## Phase Description

This phase addresses the most dangerous class of AI security failures: those involving real-world actions. When LLM applications gain the ability to call tools — send emails, execute code, modify databases, make purchases — the consequences of security failures escalate from information disclosure to tangible harm. Learners build a tool-using agent with no security controls, then explore how excessive agency, command injection through tool parameters, and privilege escalation create paths from prompt injection to real-world damage. The phase introduces the tool mediation layer as the primary control: every tool call passes through validation, policy checks, and optional human approval before execution. The key insight is that tool-using agents require the same supervisory control architecture as industrial control systems — mediated capabilities, policy gates, and sandboxed execution.

## Main Outcome

Learners can constrain AI actions through mediated capabilities and policy gates — ensuring that every tool invocation is validated, authorized, and auditable before execution reaches the real world.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 20 | Build a Tool-Using Agent | Constructs an AI agent that invokes external tools with no security controls |
| 21 | Tool Abuse and Excessive Agency | Explores what happens when agents exceed their intended capabilities and authorization |
| 22 | Command Injection Through Tools | Examines injection vectors through tool parameters, arguments, and return values |
| 23 | Secure Tool Gateway | Implements mediation, validation, and policy gates for all tool invocations |
| 24 | Human Approval Gates | Adds human-in-the-loop approval for high-risk agent actions before execution |
| 25 | Agent Sandboxing | Constrains agent execution environments to limit blast radius of compromised actions |
| 26 | Agent Security Testing | Tests agent systems against abuse, injection, escalation, and tool-misuse scenarios |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
- Completion of Phase 3 — RAG Security (Classes 13–19) recommended
