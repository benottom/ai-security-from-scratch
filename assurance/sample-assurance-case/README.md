# Sample Assurance Case — RAG Assistant

## Overview

This directory contains a sample assurance case for a Retrieval-Augmented Generation (RAG) assistant. The assurance case demonstrates how to argue that the system is adequately secure against known AI-specific threats, supported by evidence from the defense implementations and eval harness.

## Contents

- `assurance-case.md` — The full assurance case document
- `evidence/` — Directory for supporting evidence (test results, logs, configurations)

## How to Use This Sample

1. Review the assurance case structure and argument pattern
2. Replace the RAG assistant specifics with your system's details
3. Link to actual evidence from your eval runs and control ledger
4. Have the case reviewed by security assessors and stakeholders

## Assurance Case Pattern

The assurance case follows the Goal-Structuring Notation (GSN) pattern:

```
Goal: System is secure against AI-specific threats
├── Strategy: Defense-in-depth security controls
│   ├── Goal: Input integrity is maintained
│   │   ├── Context: Context Firewall isolates trusted from untrusted input
│   │   ├── Evidence: Context Firewall test results (100% injection detection)
│   │   └── Evidence: Prompt injection eval suite results
│   ├── Goal: Access control is enforced
│   │   ├── Context: Permission-Aware RAG filters by user role
│   │   ├── Evidence: Permission RAG test results
│   │   └── Evidence: RAG poisoning eval suite results
│   ├── Goal: Tool calls are safely governed
│   │   ├── Context: Tool Gateway validates, rate-limits, and approves calls
│   │   ├── Evidence: Tool Gateway test results
│   │   └── Evidence: Tool abuse eval suite results
│   ├── Goal: Output does not leak sensitive information
│   │   ├── Context: Output Validator detects and redacts secrets/PII
│   │   ├── Evidence: Output Validator test results
│   │   └── Evidence: Data leakage eval suite results
│   └── Goal: State/memory integrity is maintained
│       ├── Context: Memory Quarantine validates before trusting
│       ├── Evidence: Memory Quarantine test results
│       └── Evidence: No stale/compromised memories in audit log
└── Assumption: Attackers have no physical access to infrastructure
```
