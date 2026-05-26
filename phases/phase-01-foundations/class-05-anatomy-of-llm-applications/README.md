# Class 05 — Anatomy of LLM Applications

## Overview

An LLM application is not a single monolith — it is a **control system** composed of interdependent components, each with its own inputs, outputs, failure modes, and trust boundaries. Before you can secure an LLM application, you must understand how it is constructed, how data flows through it, and where the seams between components create opportunities for exploitation.

This class dissects a working LLM application into its constituent parts and examines each through the lens of control theory. Every component — from the prompt template to the retrieval pipeline to the tool execution layer — is a control-loop element with observables, actions, and potential disturbances. By mapping these elements, we can identify where security boundaries should exist and what happens when those boundaries are absent or poorly enforced.

## Learning Objectives

By the end of this class, you will be able to:

1. **Understand the components of LLM applications** — Identify and describe the six core components of production LLM applications: prompts, context management, retrieval (RAG), tool use, memory, and API layers.
2. **Identify the attack surface** — Map the full attack surface of an LLM application, including indirect prompt injection through retrieval, tool-result manipulation, and memory corruption.
3. **Map where security boundaries should exist** — Delineate trust boundaries between components and specify what validation, authorization, and monitoring each boundary requires.
4. **Recognize how each component can fail** — Characterize the failure modes of each component and understand how failures cascade through the system.

## Control-Theoretic View

| Control Element | LLM Application Mapping |
|---|---|
| **Objective** | Process user requests through LLM while maintaining safety and policy compliance |
| **Controller** | LLM + orchestration layer + prompt management |
| **Observations** | User input, system prompts, retrieved context, tool results, conversation history |
| **Actions** | Generate text, call tools, retrieve documents, store memories |
| **Feedback** | User responses, tool execution results, retrieval relevance scores |
| **Disturbances** | Malicious inputs, poisoned retrieval, manipulated tool results, corrupted memory |
| **Unsafe states** | Policy violation, data leakage, unauthorized tool execution, hallucinated citations |
| **Supervisory controls** | Input validation, output filtering, tool approval, retrieval authorization |
| **Monitoring** | Request logs, tool calls, policy decisions, output checks |
| **Recovery** | Reset context, revoke access, quarantine data, rollback state |

## Lab Summary

Dissect a working LLM application to identify all components and their security boundaries. You will examine a deliberately vulnerable application, map its data flows, trace trust boundaries, and produce a comprehensive security assessment of its architecture.

## Deliverables

| Deliverable | Description |
|---|---|
| **Component Inventory** | A complete catalog of every component in the LLM application with its role, inputs, outputs, and trust level |
| **Attack Surface Map** | A visual map showing all entry points, data flows, and exploitable boundaries |
| **Security Boundary Diagram** | A diagram identifying where security boundaries exist, where they are missing, and what controls each boundary should enforce |

## Estimated Time

**120 minutes** — Approximately 30 minutes for lesson review, 70 minutes for the lab, and 20 minutes for exercises and discussion.

## Directory Structure

```
class-05-anatomy-of-llm-applications/
├── README.md                    # This file
├── lesson.md                    # Full lesson content
├── control-loop-analysis.md     # Control-loop diagram and analysis
├── threat-model.md              # STRIDE-AI threat model
├── lab.md                       # Step-by-step lab instructions
├── assignment.md                # Graded exercises
├── vulnerable_app/              # Deliberately vulnerable LLM application
├── attacks/                     # Attack scripts and payloads
├── patched_app/                 # Secured version of the application
├── tests/                       # Security test suites
├── observability/               # Monitoring and logging configurations
├── assurance/                   # Safety validation and audit tools
└── solutions/                   # Reference solutions for exercises
```

## Prerequisites

- Completion of Classes 01–04 (control theory fundamentals, threat modeling, LLM internals)
- Familiarity with Python and basic web application concepts
- Understanding of API design and client-server architecture

## Key Concepts

**The LLM application is a system, not a model.** Security failures in LLM applications rarely originate from the model alone. They emerge from the interactions between components — from the way user input flows into prompts, from the way retrieval results are concatenated without validation, from the way tool outputs are trusted without verification. Understanding the anatomy of the application is understanding where these interaction failures can occur.

**Every boundary is a security boundary.** The seam between any two components — the user input and the prompt template, the retrieval result and the context window, the LLM output and the tool executor — is a trust boundary. If you do not explicitly define what crosses that boundary and how it is validated, an attacker will define it for you.

**Defense-in-depth is not optional.** No single control can secure an LLM application. Input validation alone cannot prevent indirect prompt injection. Output filtering alone cannot prevent data leakage through tool calls. You need layered controls — validation at every boundary, monitoring at every junction, and recovery mechanisms for every failure mode.
