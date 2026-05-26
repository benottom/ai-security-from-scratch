# Phase 1 — Foundations

> **Classes:** 01–06 | **Estimated Total Time:** ~22 hours

## Phase Description

This phase establishes the intellectual foundation for the entire curriculum by redefining AI security as a control-engineering discipline. Rather than treating security as a checklist of vulnerabilities, we model AI systems as control loops with observables, actions, feedback, and disturbances — and show that security failures are fundamentally control-loop failures. Learners build fluency in control-theoretic thinking, learn to decompose real AI architectures (chatbots, RAG systems, agents) into their control elements, and practice systematic threat modeling using the STRIDE-AI framework adapted for AI-specific threats. The phase culminates in building a deliberately vulnerable AI assistant — the system that will serve as the attack target throughout Phase 2.

## Main Outcome

Learners understand AI applications as control systems and can build a vulnerable assistant, mapping every security failure back to a specific control-loop deficiency (missing observations, absent actions, broken feedback, or unmitigated disturbances).

## Classes

| Class | Title | Description |
|-------|-------|-------------|
| 01 | AI Security as Control | Establishes AI security as an engineering discipline grounded in control theory — behavior, safe bounds, and adversarial disturbances |
| 02 | Control Theory for AI Security | Maps core control theory concepts (feedback loops, controllers, plants, disturbances) to AI system analogs |
| 03 | AI Systems as Adversarial Control Loops | Decomposes chatbot, RAG, and agent systems into control-loop elements and traces disturbance propagation |
| 04 | Threat Modeling AI Systems | Applies control-loop decomposition and STRIDE-AI classification to systematically catalog AI threats |
| 05 | Anatomy of LLM Applications | Dissects LLM application components (prompts, retrieval, tools, memory) and their security boundaries |
| 06 | Build Your First Vulnerable AI Assistant | Constructs and attacks an unprotected AI assistant to experience open-loop security failure firsthand |

## Prerequisites

- Familiarity with basic AI/ML concepts (what a language model is, what it does)
- Working development environment (Python 3.11+, Docker, make)
- No prior security or control theory knowledge required — this is the starting point
