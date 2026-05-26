# OWASP LLM Top 10 Mapping — AI Security Controls

## Overview

This directory contains mappings between AI security controls from "AI Security from Scratch" and the OWASP Top 10 for Large Language Model Applications (2025).

## Why This Mapping Matters

The OWASP LLM Top 10 is the most widely referenced threat taxonomy for LLM applications. By mapping our controls to these risks, we:

1. **Demonstrate coverage** — Show that our defense-in-depth approach addresses the most critical LLM threats
2. **Guide implementation** — Help teams prioritize which defenses to implement first
3. **Provide evidence** — Generate audit-ready documentation for compliance

## Control-to-Risk Mapping

| Defense | OWASP Risks Addressed |
|---|---|
| Context Firewall | LLM01 (Prompt Injection), LLM07 (System Prompt Leakage) |
| Permission-Aware RAG | LLM02 (Info Disclosure), LLM04 (Data Poisoning), LLM08 (Vector Weaknesses) |
| Secure Tool Gateway | LLM05 (Output Handling), LLM06 (Excessive Agency), LLM10 (Unbounded Consumption) |
| Policy Engine | LLM01, LLM02, LLM05, LLM06, LLM07, LLM08 |
| Output Validator | LLM02 (Info Disclosure), LLM05 (Output Handling), LLM07 (System Prompt Leakage) |
| Memory Quarantine | LLM03 (Supply Chain), LLM04 (Data Poisoning), LLM09 (Misinformation) |
| Security Gateway | All risks (unified pipeline) |

## See Also

- `mapping.md` — Detailed mapping table with evidence sources
- `../iso27001-mapping/` — ISO 27001 mapping
- `../nist-ai-rmf-mapping/` — NIST AI RMF mapping
