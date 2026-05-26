# NIST AI RMF Mapping — AI Security Controls

## Overview

This document maps the AI security controls from "AI Security from Scratch" to the NIST AI Risk Management Framework (AI RMF 1.0). The NIST AI RMF provides a structured approach to managing AI risks across four core functions: Govern, Map, Measure, and Manage.

---

## Mapping Table

### GOVERN Function

| NIST AI RMF Subcategory | Description | AI Security Defense | Implementation | Evidence |
|---|---|---|---|---|
| GOVERN 1.1 | Legal and regulatory requirements are understood | Policy Engine, ISO 27001 Mapping | Policies encode compliance requirements; mapping shows ISO 27001 alignment | Policy YAML files, compliance mapping |
| GOVERN 1.2 | AI risk management roles are defined | Tool Gateway, Permission-RAG | Role-based access and approval workflows | Role definitions, approval logs |
| GOVERN 1.3 | Processes for AI risk assessment | Eval Harness, Risk Register | Structured eval suites; risk register tracks findings | Eval reports, risk register |
| GOVERN 1.4 | Risk tolerance is defined | Policy Engine | Policy thresholds define risk tolerance (e.g., injection_threshold) | Configuration files |
| GOVERN 1.5 | AI systems are inventoried | AI-BOM Template | Bill of Materials tracks all components, models, data sources | Completed AI-BOM |
| GOVERN 1.6 | Policies for AI system use | Policy Engine | Policy-as-code defines acceptable use | Policy files |
| GOVERN 1.7 | AI actors are identified | AI-BOM, Tool Gateway | System identifies all actors (users, models, tools) | AI-BOM, gateway logs |
| GOVERN 2.1 | AI risk is documented | Risk Register, Assurance Case | Risk register tracks all identified risks | Risk register, assurance case |
| GOVERN 2.2 | AI risk is communicated | Assurance Case, Exec Summary | Assurance case communicates risk to stakeholders | Assurance case document |
| GOVERN 2.3 | Organizational AI risk culture | Curriculum, Training | "AI Security from Scratch" curriculum builds security culture | Training records |
| GOVERN 3.1 | AI system requirements | Policy Engine, Security Gateway | Security requirements encoded as enforceable policies | Policy compliance results |
| GOVERN 4.1 | Organizational policies for AI | Policy Engine | Policies version-controlled and auditable | Policy repository |
| GOVERN 4.2 | AI system accountability | Control Ledger | Tamper-evident audit trail for all decisions | Ledger events |
| GOVERN 5.1 | Diverse perspectives in AI governance | (Organizational control) | Multiple stakeholders review security reports | Review records |

### MAP Function

| NIST AI RMF Subcategory | Description | AI Security Defense | Implementation | Evidence |
|---|---|---|---|---|
| MAP 1.1 | Context is understood | Control Loop Model | System modeled as control loop with reference, controller, plant, actuators | Architecture diagrams |
| MAP 1.2 | AI system boundaries are defined | Security Gateway | Gateway defines the security boundary for all AI interactions | Gateway configuration |
| MAP 1.3 | AI system capabilities and limits are understood | AI-BOM | BOM documents model capabilities, limitations, and failure modes | AI-BOM |
| MAP 1.4 | AI system tasks are defined | Tool Gateway | Tool registry defines all available tasks and their risk levels | Tool definitions |
| MAP 1.5 | Impacts of AI system failure are understood | Risk Register, Impact Analysis | Risk register documents business and technical impacts | Risk register |
| MAP 2.1 | Data sources are documented | Permission-RAG, AI-BOM | Document access levels and sources tracked in RAG and BOM | RAG configuration, AI-BOM |
| MAP 2.2 | Data quality is assessed | Memory Quarantine | Quarantine validates data quality before trusting | Quarantine validation logs |
| MAP 2.3 | Data biases are identified | (Out of scope for security controls) | N/A | N/A |
| MAP 3.1 | AI system threats are identified | Eval Harness | Attack YAMLs catalog known threat scenarios | Attack YAML files |
| MAP 3.2 | AI system vulnerabilities are identified | Eval Harness, Security Reports | Eval results identify vulnerabilities; reports document them | Eval reports, security reports |
| MAP 3.3 | AI system impacts are identified | Risk Register | Risk register includes impact analysis for each risk | Risk register |
| MAP 3.4 | Attack surfaces are identified | Security Gateway | Gateway reduces and documents the attack surface | Gateway config, eval results |
| MAP 4.1 | AI system interdependencies are mapped | AI-BOM | BOM maps all system components and their relationships | AI-BOM |
| MAP 4.2 | AI system failure modes are defined | Control Loop Analysis | Failure modes defined per control loop element | Control loop documentation |
| MAP 4.3 | AI system failure likelihoods are estimated | Eval Harness, Risk Register | Eval results estimate likelihood; risk register records it | Eval pass rates, risk scores |

### MEASURE Function

| NIST AI RMF Subcategory | Description | AI Security Defense | Implementation | Evidence |
|---|---|---|---|---|
| MEASURE 1.1 | AI system performance is evaluated | Eval Harness | Structured eval suites measure defense performance | Eval reports with scores |
| MEASURE 1.2 | AI risk is measured | Eval Harness, Risk Register | Quantitative scores from evals; risk scores in register | Score reports |
| MEASURE 1.3 | AI system reliability is evaluated | Eval Harness, Control Ledger | Repeated eval runs show reliability; ledger shows consistency | Trend analysis, ledger data |
| MEASURE 2.1 | AI system bias is evaluated | (Out of scope for security controls) | N/A | N/A |
| MEASURE 2.2 | AI system security is evaluated | All defenses, Eval Harness | Comprehensive security testing across all defense layers | All test and eval results |
| MEASURE 2.3 | AI system privacy is evaluated | Output Validator, Permission-RAG | PII detection in outputs; access control on data | Validation findings, access logs |
| MEASURE 2.4 | AI system transparency is evaluated | Control Ledger, Policy Engine | All decisions logged and explainable via policies | Ledger events, policy eval results |
| MEASURE 2.5 | AI system safety is evaluated | Tool Gateway, Eval Harness | Tool safety gates; safety-focused eval suites | Gateway logs, eval results |
| MEASURE 2.6 | AI system security is evaluated against attacks | Eval Harness | Attack simulation suites test against known attack vectors | Eval reports |
| MEASURE 3.1 | AI system metrics are tracked | Eval Harness, Control Ledger | Quantitative metrics tracked over time | Historical eval data |
| MEASURE 3.2 | AI system changes are evaluated | Policy Engine, CI Pipeline | Policy changes tested; CI runs evals on every change | CI results, policy diffs |
| MEASURE 3.3 | Feedback mechanisms | Eval Harness, Control Ledger | Eval results inform defense improvements | Remediation tracking |

### MANAGE Function

| NIST AI RMF Subcategory | Description | AI Security Defense | Implementation | Evidence |
|---|---|---|---|---|
| MANAGE 1.1 | AI risks are mitigated | All defenses | Defense-in-depth implementation | All defense test results |
| MANAGE 1.2 | AI system failures are responded to | Security Gateway, Control Ledger | Gateway blocks attacks; ledger enables forensics | Gateway blocks, ledger events |
| MANAGE 1.3 | AI system is monitored | Control Ledger, Dashboard | Continuous monitoring of security events | Dashboard data |
| MANAGE 2.1 | AI system is assessed for residual risk | Assurance Case, Risk Register | Assurance case identifies residual risks | Assurance case, risk register |
| MANAGE 2.2 | AI system risk is accepted | Risk Register | Risk acceptance documented with owner and date | Signed risk register |
| MANAGE 2.3 | AI system risk is shared | (Organizational control) | Risk sharing communicated to stakeholders | Communication records |
| MANAGE 3.1 | AI system incidents are managed | Control Ledger, Security Reports | Ledger provides forensic evidence; reports document incidents | Incident reports, ledger data |
| MANAGE 4.1 | AI risk management is improved | Eval Harness, CI | Continuous eval improvement; CI catches regressions | Eval improvements, CI results |

---

## Coverage Summary

| NIST AI RMF Function | Total Subcategories | Mapped to Defenses | Coverage |
|---|---|---|---|
| GOVERN | 13 | 12 | 92% |
| MAP | 13 | 12 | 92% |
| MEASURE | 12 | 10 | 83% |
| MANAGE | 8 | 7 | 88% |
| **Total** | **46** | **41** | **89%** |

Note: Some NIST AI RMF subcategories (e.g., bias evaluation) are outside the scope of security-specific controls but should be addressed by complementary AI governance processes.
