# ISO 27001 Mapping — AI Security Controls

## Overview

This document maps the AI security controls from the "AI Security from Scratch" curriculum to relevant ISO 27001:2022 controls. This mapping helps organizations demonstrate compliance with ISO 27001 when implementing AI-specific security measures.

## How to Use This Mapping

1. Identify which ISO 27001 controls apply to your AI system
2. Find the corresponding AI security defenses in this mapping
3. Implement the defenses and run the eval harness for evidence
4. Use the eval results and control ledger as audit evidence

---

## Mapping Table

| ISO 27001 Control | Control Name | AI Security Defense | Implementation | Evidence |
|---|---|---|---|---|
| A.5.1 | Policies for information security | Policy Engine | Define AI security policies in YAML; evaluate all requests against policies | Policy YAML files, Policy Engine eval results |
| A.5.2 | Information security roles and responsibilities | Permission-Aware RAG, Tool Gateway | Role-based access on documents; role-based tool permissions | RAG access logs, Tool Gateway audit trail |
| A.5.3 | Segregation of duties | Tool Gateway | Human approval for critical tool calls; no single role can execute all operations | Approval request logs |
| A.5.8 | Information security in project management | Security Gateway, Policy Engine | Security gateway as default project component; policies applied from project start | Gateway configuration, policy files |
| A.5.10 | Acceptable use of information and other associated assets | Context Firewall, Policy Engine | Content policies define acceptable inputs/outputs; firewall enforces boundaries | Firewall audit log, policy eval results |
| A.5.14 | Information transfer | Output Validator, Security Gateway | Output validation prevents unauthorized information transfer; gateway inspects all outputs | Output validation findings, gateway audit log |
| A.5.15 | Access control | Permission-Aware RAG | Document-level access control based on user roles | RAG access decisions |
| A.5.16 | Identity management | Permission-Aware RAG, Tool Gateway | User roles verified before data access and tool execution | Role verification logs |
| A.5.33 | Protection of records | Control Ledger | Hash-chained, append-only audit trail for all security events | Ledger integrity verification |
| A.6.1 | Screening | Memory Quarantine | New memories screened (quarantined) before being trusted | Quarantine logs, promotion records |
| A.6.3 | Information security awareness, education and training | AI Security from Scratch Curriculum | Hands-on exercises covering attack vectors and defenses | Completion records, eval results |
| A.6.5 | Responding to information security incidents | Security Gateway, Control Ledger | Gateway blocks attacks; ledger provides forensic evidence | Incident response based on ledger events |
| A.7.1 | Physical security perimeters | (Out of scope for AI-specific controls) | N/A | N/A |
| A.8.1 | User endpoint devices | (Out of scope for AI-specific controls) | N/A | N/A |
| A.8.2 | Privileged access rights | Tool Gateway | Critical tools require admin role or explicit approval | Tool access logs |
| A.8.3 | Information access restriction | Permission-Aware RAG | Document access restricted by classification level | RAG access denied logs |
| A.8.5 | Secure authentication | Tool Gateway | Human approval serves as authentication for critical operations | Approval flow records |
| A.8.7 | Protection against malware | Context Firewall | Injection detection as "malware for AI" — quarantines malicious inputs | Firewall quarantine logs |
| A.8.9 | Configuration management | Policy Engine, Security Gateway | Policies as code; gateway configuration version-controlled | Policy files, gateway config |
| A.8.10 | Information deletion | Memory Quarantine | Expired quarantined memories are deleted; demoted memories returned to quarantine | Expiration logs |
| A.8.12 | Data leakage prevention | Output Validator, Security Gateway | Output validation detects secrets and PII; gateway blocks leakage | Validation findings, gateway blocks |
| A.8.15 | Logging | Control Ledger | Comprehensive, tamper-evident audit trail | Ledger events, integrity verification |
| A.8.16 | Monitoring activities | Control Ledger, Dashboard Examples | Real-time monitoring of security events via dashboards | Dashboard configurations |
| A.8.20 | Networks security | (Out of scope for AI-specific controls) | N/A | N/A |
| A.8.23 | Web filtering | Context Firewall | Input filtering blocks injection attempts from web inputs | Firewall block logs |
| A.8.24 | Use of cryptography | Control Ledger | Hash-chaining (SHA-256) for ledger integrity | Ledger hash verification |
| A.8.25 | Secure development life cycle | All defenses, Eval Harness | Security defenses built into development; eval harness runs in CI | CI pipeline results |
| A.8.26 | Application security requirements | Policy Engine, Security Gateway | Security requirements encoded as policies; gateway enforces them | Policy compliance results |
| A.8.28 | Secure coding | Context Firewall, Tool Gateway | Input validation, parameter validation, allowlisting | Code review, test results |
| A.8.29 | Security testing in development and acceptance | Eval Harness | Attack simulation suites test all defense layers | Eval reports |
| A.8.30 | Outsourced development | (Out of scope — depends on LLM provider) | N/A | N/A |
| A.8.31 | Separation of development, test and production | Eval Harness, Policy Engine | Different policy configurations for environments; eval harness for testing | Environment configs |
| A.8.32 | Change management | Policy Engine | Policy changes tracked in YAML; version-controlled | Git history of policy files |
| A.8.33 | Test information | Memory Quarantine | Test data isolated in quarantine; not promoted to trusted storage without validation | Quarantine records |
| A.8.34 | Attack surface management | Security Gateway, Eval Harness | Gateway reduces attack surface; eval harness tests for unknown exposures | Eval results, gateway config |

---

## Compliance Checklist

| ISO 27001 Control | Implemented | Defense | Evidence Available |
|---|---|---|---|
| A.5.1 | ✅ | Policy Engine | ✅ |
| A.5.2 | ✅ | Permission-RAG, Tool Gateway | ✅ |
| A.5.3 | ✅ | Tool Gateway | ✅ |
| A.5.8 | ✅ | Security Gateway | ✅ |
| A.5.10 | ✅ | Context Firewall, Policy Engine | ✅ |
| A.5.14 | ✅ | Output Validator | ✅ |
| A.5.15 | ✅ | Permission-RAG | ✅ |
| A.5.16 | ✅ | Permission-RAG, Tool Gateway | ✅ |
| A.5.33 | ✅ | Control Ledger | ✅ |
| A.6.1 | ✅ | Memory Quarantine | ✅ |
| A.8.2 | ✅ | Tool Gateway | ✅ |
| A.8.3 | ✅ | Permission-RAG | ✅ |
| A.8.7 | ✅ | Context Firewall | ✅ |
| A.8.9 | ✅ | Policy Engine | ✅ |
| A.8.12 | ✅ | Output Validator | ✅ |
| A.8.15 | ✅ | Control Ledger | ✅ |
| A.8.25 | ✅ | All defenses | ✅ |
| A.8.29 | ✅ | Eval Harness | ✅ |
