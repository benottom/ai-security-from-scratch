---
name: New Class Proposal
about: Propose a new class for the AI Security from Scratch curriculum
title: "[CLASS PROPOSAL] "
labels: ["class-proposal", "needs-review"]
assignees: []
---

## Class Title

<!-- What is the descriptive title for this class? -->

## Phase

<!-- Which phase does this class belong to?
  Phase 1: Foundations (remember/understand)
  Phase 2: Core Vulnerabilities (apply/analyze)
  Phase 3: Advanced Topics (evaluate/create)
-->

## Learning Objectives

<!-- List 3–5 specific, measurable learning objectives.
  Use Bloom's taxonomy verbs appropriate for the phase:
  Phase 1: define, describe, identify, explain
  Phase 2: apply, demonstrate, analyze, distinguish
  Phase 3: design, evaluate, construct, assess
-->

1.
2.
3.
4.
5.

## Control-Theoretic Focus

<!-- Map this class to the control-loop model. Fill in each element: -->

- **Sensor:** What is observed/monitored?
- **Estimator:** How does the system infer state?
- **Controller:** What is the decision logic or policy?
- **Actuator:** What mechanism enforces the decision?
- **Plant:** What system is under protection?
- **Disturbance:** What is the threat or adversarial input?
- **Reference:** What is the desired secure state?

## Vulnerable System

<!-- Describe the vulnerable application that will be built for this class.
  Include: type (web_app, api, ml_pipeline, cli_tool, notebook),
  technology stack, and what the app does. -->

## Attack Scenario

<!-- Describe the attack that demonstrates the vulnerability.
  Must be safe: localhost only, no external targets, no destructive payloads. -->

- **Attacker profile:**
- **Attack steps:**
- **Expected result:**

## Defensive Controls

<!-- List the defensive controls that will mitigate this vulnerability.
  At least 2 controls required (defense in depth).
  Map each to a control-loop element and category (preventive/detective/corrective). -->

1. **Control name:** | **Category:** | **Control-loop element:**
2. **Control name:** | **Category:** | **Control-loop element:**

## Tests Required

<!-- What automated tests are needed?
  - Tests that verify the vulnerability exists (vulnerable app)
  - Tests that verify the patch works (patched app)
  - Tests that verify each control is effective
-->

- [ ] Vulnerability existence tests
- [ ] Patch effectiveness tests
- [ ] Control verification tests
- [ ] Defense-in-depth tests
- [ ] Legitimate use preservation tests

## Assurance Evidence

<!-- What evidence artifacts are needed for assurance? -->

- [ ] Control ledger (YAML)
- [ ] Test results (JUnit XML)
- [ ] Assurance report (Markdown)
- [ ] Standards compliance mapping

## Safety Notes

<!-- Any safety considerations specific to this class.
  All attacks must be localhost-safe, deterministic, and bounded.
  Flag anything that needs special attention. -->

## CWE Mapping

<!-- Which CWE IDs does this vulnerability map to?
  Reference: https://cwe.mitre.org/ -->

## Real-World Examples

<!-- At least one real-world incident or publicly discussed case.
  Include citations/URLs. -->

1.

## Prerequisites

<!-- Which prior classes must be completed before this one? -->

-

## Estimated Duration

<!-- Target: 90–120 minutes (lecture + lab + assessment) -->

## Additional Notes

<!-- Any other relevant information -->
