# Phase 2 — Prompt Injection

> **Classes:** 07–12 | **Estimated Total Time:** ~23 hours

## Phase Description

This phase confronts the most prevalent attack class in LLM applications: prompt injection. Starting from the vulnerable assistant built in Phase 1, learners systematically explore the three pillars of the prompt injection threat landscape — direct injection, indirect injection through external data, and instruction-conflict jailbreaks — before learning to defend against each with layered controls. The phase treats prompt injection not as a single vulnerability but as a family of control-loop failures: controller hijacking (direct), observation channel corruption (indirect), and reference signal conflict (jailbreaks). It culminates in building a regression test suite that continuously validates all defenses.

## Main Outcome

Learners can exploit and defend instruction-channel failures — recognizing that prompt injection is not one attack but a family of control-loop failures, each requiring different observations, actions, and feedback mechanisms to mitigate.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 07 | Direct Prompt Injection | Explores user-input attacks that override system instructions through the observation channel |
| 08 | System Prompt Leakage | Examines extraction of confidential system configuration as an information disclosure vulnerability |
| 09 | Indirect Prompt Injection | Covers injection through external data sources (RAG documents, API responses, web pages) |
| 10 | Jailbreaks and Instruction Conflicts | Analyzes role-playing, competing objectives, and multi-turn manipulation that exploit instruction-following |
| 11 | Prompt Injection Defense Patterns | Composes layered defenses: context separation, instruction hierarchy, input validation, output filtering, monitoring |
| 12 | Prompt Security Regression Testing | Builds automated pytest suites that continuously validate prompt injection defenses in CI/CD |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
