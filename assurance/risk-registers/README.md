# Risk Registers in AI Security

## Overview

A risk register is a structured document that tracks identified risks, their severity, current controls, gaps, and mitigation plans. In AI security, risk registers are essential for managing the unique and evolving threat landscape of AI systems.

## Why Risk Registers Matter for AI

AI systems introduce risks that traditional security risk registers may not cover:

1. **Novel attack vectors**: Prompt injection, data poisoning, and model manipulation are new threat categories
2. **Probabilistic behavior**: LLMs are non-deterministic, making risk likelihood harder to estimate
3. **Emergent risks**: New attack techniques are discovered regularly
4. **Cascading effects**: A single LLM vulnerability can affect multiple downstream systems
5. **Human-like interaction**: AI systems can be social-engineered through natural language

## How to Use This Template

### Step 1: Identify Risks

Use the following sources to identify AI-specific risks:
- OWASP LLM Top 10
- NIST AI RMF risk categories
- AI Security from Scratch eval harness results
- Threat modeling exercises
- Incident post-mortems

### Step 2: Assess Risks

Score each risk on:
- **Likelihood** (1-5): How likely is this to occur?
- **Impact** (1-5): How severe would the consequences be?
- **Risk Score**: Likelihood × Impact

### Step 3: Map to Controls

For each risk, document:
- What controls currently exist (from the defense implementations)
- What gaps remain
- What additional controls are needed

### Step 4: Track Mitigation

Assign:
- Owner: Who is responsible for mitigation
- Target Date: When mitigation should be complete
- Review Date: When to check progress

### Step 5: Review Regularly

AI risk registers should be reviewed:
- After every eval harness run (regressions may introduce new risks)
- After every security incident
- At least quarterly as a standing agenda item

## Linking to Other Assurance Artifacts

| Artifact | How It Connects |
|---|---|
| Eval Harness Results | Quantitative evidence for risk likelihood and impact |
| Control Ledger | Forensic evidence for incident analysis |
| Assurance Case | Argument that residual risks are acceptable |
| AI-BOM | Inventory of components that may introduce risks |
| Framework Mappings | Compliance justification for risk acceptance |

## Sample Risk Register

See `sample-risk-register.md` for a complete example with 8 risks for a corporate RAG assistant.
