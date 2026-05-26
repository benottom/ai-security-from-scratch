# Phase 3 — RAG Security

> **Classes:** 13–19 | **Estimated Total Time:** ~24 hours

## Phase Description

This phase examines the security implications of retrieval-augmented generation — one of the most common production patterns for LLM applications. RAG introduces a new trust boundary between the LLM and an external knowledge base, creating opportunities for document poisoning, citation fabrication, and unauthorized data access that do not exist in simple chatbot architectures. Learners first build a basic RAG system with no security controls, then systematically explore each attack vector before implementing permission-aware retrieval, source trust scoring, and evidence-grounded generation. The phase reframes RAG as an observation system: the retrieval pipeline is a sensor, and poisoned documents are corrupted sensor data that must be validated before they influence the controller.

## Main Outcome

Learners can build RAG that respects source trust, permissions, and evidence — treating the retrieval pipeline as a sensor system that requires provenance validation, access control, and attribution before its outputs can be trusted.

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 13 | Build a Basic RAG System | Constructs a retrieval-augmented generation pipeline with no security controls |
| 14 | RAG as an Observation System | Models the retrieval pipeline as a sensor system with trust and provenance requirements |
| 15 | Document Poisoning | Explores injection and manipulation of documents in the retrieval corpus |
| 16 | Citation Spoofing | Examines how LLMs fabricate or misattribute retrieved evidence in generated output |
| 17 | Unauthorized Retrieval | Covers data access violations where retrieval queries return information beyond user authorization |
| 18 | Permission-Aware RAG | Implements access control, source trust scoring, and authorization in the retrieval pipeline |
| 19 | Secure RAG Evaluation | Assesses RAG security with metrics for trust, evidence fidelity, and access control effectiveness |

## Prerequisites

- Completion of Phase 1 — Foundations (Classes 01–06)
- Completion of Phase 2 — Prompt Injection (Classes 07–12)
