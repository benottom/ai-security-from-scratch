# Phase 6 — Data, Privacy, and Leakage

> **Classes:** 33–38 | **Estimated Total Time:** ~21 hours

## Phase Description

This phase addresses the data-exposure risks inherent in AI systems that process, retrieve, and generate text based on large corpora of potentially sensitive information. LLM applications are data pipelines: they ingest user queries, retrieve documents, generate completions, and log interactions — and at every stage, sensitive data can leak. Learners explore how models inadvertently reveal PII, secrets, and internal configuration in their outputs; how vector embeddings create privacy risks through reconstruction and inference attacks; and how logging systems designed for debugging can become compliance liabilities. The phase introduces data classification, redaction pipelines, embedding privacy controls, and privacy-preserving logging as the controls that reduce sensitive-data exposure across the full AI pipeline.

## Main Outcome

Learners can identify and reduce sensitive-data exposure across AI pipelines — implementing classification, redaction, access control, and privacy-preserving logging that minimize the risk of PII, secrets, and confidential data appearing in model outputs or observability systems.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 33 | Sensitive Data Exposure | Identifies how AI systems inadvertently reveal sensitive information in generated outputs |
| 34 | Secrets Leakage | Examines leakage of API keys, credentials, and internal configuration through model completions |
| 35 | PII Detection and Redaction | Implements detection and removal of personally identifiable information from inputs and outputs |
| 36 | Embedding Privacy | Covers privacy risks in vector embeddings, including reconstruction and inference attacks |
| 37 | Vector Database Access Control | Secures vector stores with proper authorization, isolation, and tenant boundaries |
| 38 | Privacy-Preserving AI Logging | Designs logging systems that support debugging and auditing without exposing sensitive data |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
- Completion of Phase 3 — RAG Security (Classes 13–19) recommended
