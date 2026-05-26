# NIST AI RMF Mapping — AI Security Controls

## Overview

This directory contains mappings between AI security controls from "AI Security from Scratch" and the NIST AI Risk Management Framework (AI RMF 1.0).

## NIST AI RMF Structure

The NIST AI RMF is organized into four core functions:

1. **GOVERN** — Establish and maintain AI risk management culture and processes
2. **MAP** — Understand context and characterize AI system risks
3. **MEASURE** — Quantify and assess AI risks
4. **MANAGE** — Prioritize and act upon AI risks

## How Our Controls Map

| NIST AI RMF Function | Primary Defense Alignment |
|---|---|
| **GOVERN** | Policy Engine (policy-as-code for governance), AI-BOM (inventory) |
| **MAP** | Security Gateway (boundary definition), Risk Register (threat identification) |
| **MEASURE** | Eval Harness (quantitative security measurement), Control Ledger (metrics tracking) |
| **MANAGE** | All defenses (risk mitigation), Control Ledger (incident forensics) |

## Key Insight

The NIST AI RMF is a *risk management* framework, not a *security* framework. Our mapping shows how security-specific controls contribute to broader AI risk management goals. Organizations should supplement these security controls with:

- **Bias and fairness** assessments (not covered by our security controls)
- **Transparency and explainability** mechanisms (partially covered by policy engine and ledger)
- **Human-AI interaction** design (partially covered by tool gateway approval flows)

## See Also

- `mapping.md` — Detailed mapping table
- `../iso27001-mapping/` — ISO 27001 mapping
- `../owasp-llm-top10-mapping/` — OWASP LLM Top 10 mapping
