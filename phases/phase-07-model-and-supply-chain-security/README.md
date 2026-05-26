# Phase 7 — Model and Supply Chain Security

> **Classes:** 39–44 | **Estimated Total Time:** ~21 hours

## Phase Description

This phase zooms out from the application layer to examine the security of the AI supply chain itself — the models, datasets, fine-tuning processes, and dependencies that every AI application implicitly trusts. Learners map the full supply chain from base model to production deployment, identifying trust boundaries at every handoff: model downloads, weight files, tokenizer configurations, fine-tuning data, and dependency packages. The phase covers how poisoned datasets embed backdoors in models, how fine-tuning can degrade safety alignment, how model extraction threatens intellectual property, and how unsafe model loading introduces code-execution risks. It culminates in building an AI Bill of Materials — a comprehensive, machine-readable inventory of every component in the AI system's supply chain with verified provenance.

## Main Outcome

Learners can assess model, dataset, dependency, and provider risks — building an AI Bill of Materials that makes supply chain trust explicit, verifiable, and auditable rather than assumed.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 39 | Model Supply Chain Risks | Maps the full model supply chain and identifies trust boundaries at every handoff point |
| 40 | Unsafe Model Loading | Examines code-execution and integrity risks from loading untrusted model artifacts (pickle, safetensors) |
| 41 | Dataset Poisoning Concepts | Covers how poisoned training data creates embedded vulnerabilities and backdoors in models |
| 42 | Fine-Tuning Risks | Explores how fine-tuning can degrade safety alignment and introduce targeted backdoors |
| 43 | Model Extraction Concepts | Examines risks of model theft, reverse engineering, and intellectual property compromise |
| 44 | AI Bill of Materials | Builds a comprehensive inventory of model components, dependencies, and verified provenance |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
