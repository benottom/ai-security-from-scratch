# ISO 27001 Mapping — AI Security Controls

## Overview

This directory contains mappings between AI security controls from the "AI Security from Scratch" curriculum and ISO 27001:2022 Annex A controls.

## Purpose

Organizations implementing AI systems need to demonstrate that their security controls align with established frameworks. This mapping shows how the AI-specific defenses address ISO 27001 requirements, providing a foundation for compliance audits.

## How AI Security Maps to ISO 27001

ISO 27001 was designed for general information security. AI systems introduce new threat vectors (prompt injection, model manipulation, data poisoning) that aren't explicitly covered. Our approach:

1. **Identify the intent** behind each ISO 27001 control
2. **Map the intent** to AI-specific threats and defenses
3. **Provide evidence** through the eval harness and control ledger

For example:
- **A.8.7 (Protection against malware)** → Context Firewall treats prompt injection as "AI malware"
- **A.8.12 (Data leakage prevention)** → Output Validator detects secrets and PII in AI outputs
- **A.5.33 (Protection of records)** → Control Ledger provides tamper-evident audit trail

## Key Mappings

| ISO 27001 Theme | AI Security Defense | Primary Threat Addressed |
|-----------------|---------------------|--------------------------|
| Access Control | Permission-Aware RAG | Unauthorized data access |
| Input Validation | Context Firewall | Prompt injection |
| Output Control | Output Validator | Data leakage |
| Policy Enforcement | Policy Engine | Policy violations |
| Tool Governance | Tool Gateway | Tool abuse |
| State Management | Memory Quarantine | Memory corruption |
| Audit & Logging | Control Ledger | Forensic analysis |

## See Also

- `mapping.md` — Detailed mapping table with all ISO 27001 controls
- `../nist-ai-rmf-mapping/` — NIST AI RMF mapping
- `../owasp-llm-top10-mapping/` — OWASP LLM Top 10 mapping
