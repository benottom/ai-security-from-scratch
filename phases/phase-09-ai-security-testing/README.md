# Phase 9 — AI Security Testing and CI/CD

> **Classes:** 51–56 | **Estimated Total Time:** ~21 hours

## Phase Description

This phase addresses the critical question: how do you know your controls still work? Security is not a state — it is a process, and without continuous validation, controls silently degrade as models are updated, prompts are modified, and new attack techniques emerge. Learners design comprehensive security test strategies, build custom evaluation harnesses, curate attack datasets, and develop quantitative scoring systems that measure security posture objectively. The phase then integrates these tests into CI/CD pipelines using GitHub Actions, ensuring that every code change is validated against the full attack suite before it reaches production. The key insight is that security tests are not optional — they are the feedback mechanism that closes the control loop for the security engineering process itself.

## Main Outcome

Learners can continuously test AI controls in engineering pipelines — building automated test suites, evaluation harnesses, and CI integrations that detect security regressions before they reach production.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 51 | AI Security Test Design | Designs comprehensive security test strategies covering attack categories, severity levels, and coverage goals |
| 52 | Evaluation Harness from Scratch | Builds a custom evaluation framework for running security tests with reproducible configurations |
| 53 | Attack Datasets | Curates and maintains datasets of known attack patterns, payloads, and adversarial inputs for testing |
| 54 | Security Scoring | Develops quantitative scoring methodologies for measuring AI system security posture over time |
| 55 | GitHub Actions for AI Security | Integrates security tests into CI/CD pipelines to validate every code change against the attack suite |
| 56 | Regression Testing AI Controls | Ensures security controls remain effective across model updates, prompt changes, and configuration drift |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
- Completion of Phase 8 — Defensive Controls (Classes 45–50) recommended
