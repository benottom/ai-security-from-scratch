# Prompt Injection Defense Patterns

> **Module:** Phase 2 — Prompt Injection | **Class:** 11 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Enumerate and explain the five primary defense patterns: context separation, instruction hierarchy, input validation, output filtering, and monitoring
2. Implement each defense pattern as an independent, composable control component
3. Explain why no single defense is sufficient and how layered defenses provide defense in depth
4. Compose multiple defense patterns into a complete security architecture for an LLM application
5. Evaluate the tradeoffs between security and usability for each defense pattern

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for defense patterns.

### Objective

The safety goal the system must maintain:

> Ensure that the LLM application is defended against prompt injection through multiple independent, complementary layers, such that the failure of any single layer does not result in a complete security failure.

### Controller

The component responsible for making decisions to maintain the objective:

> The defense orchestration layer — a middleware that composes multiple defense patterns into a coordinated defense-in-depth architecture, routing each request through the appropriate sequence of defenses and managing their interactions.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Input classification result | Input validation layer | Per request |
| Context composition integrity | Context separation layer | Per request |
| Instruction hierarchy compliance | Priority enforcer | Per response |
| Output safety classification | Output filter | Per response |
| System-wide attack metrics | Monitoring layer | Continuous |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Route through defense layers | Applies appropriate defenses to each request | Request received |
| Adjust defense sensitivity | Increases or decreases defense strictness based on threat level | Anomalous patterns detected |
| Activate additional layers | Enables backup defenses when primary layers fail | Layer failure detected |
| Escalate to human | Routes ambiguous cases to human review | Low-confidence classification |
| Circuit break | Temporarily disables the application | Critical security failure |

### Feedback

How the controller learns whether its actions achieved the objective:

> Each defense layer produces metrics (detection rates, false positive rates, processing latency) that feed back into the orchestration layer. When an attack bypasses one layer but is caught by another, the bypass analysis feeds back to improve the bypassed layer. System-wide attack metrics inform dynamic adjustment of defense sensitivity.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Novel injection techniques that bypass pattern-based defenses | Evolving threat landscape | Monitoring + output filtering as backstop |
| Adversarial adaptation to known defenses | Dedicated attackers | Defense diversity + regular updates |
| False positives from overly aggressive defenses | Legitimate user input | Sensitivity tuning + human review escalation |
| Performance degradation from multiple defense layers | Processing overhead | Async processing + selective layer activation |
| Defense interaction bugs | Complex layered architecture | Integration testing + defense regression tests |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| All layers bypassed | Novel attack evades every defense | Complete security failure |
| Defense disabled for performance | Layers turned off under load | Reduced security posture |
| False positive spiral | Over-aggressive defenses block legitimate use | System becomes unusable |
| Defense interaction conflict | Layer A modifies input in a way that defeats Layer B | Reduced effectiveness |
| Complacent monitoring | No attacks detected → monitoring neglected | Unnoticed security degradation |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> A defense effectiveness dashboard that tracks each layer's detection rate, false positive rate, and bypass rate independently. When any layer's effectiveness drops below a threshold, an alert triggers investigation. Additionally, a red-team testing schedule that periodically validates the entire defense stack against known and novel attack techniques.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Overall injection bypass rate | > 0.5% | Critical alert |
| Individual layer detection rate | < 90% per layer | Layer investigation |
| False positive rate per layer | > 10% | Sensitivity adjustment |
| Defense processing latency | > 500ms p99 | Performance review |
| Layer interaction failure rate | > 0.1% | Integration testing |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Identify which defense layer(s) failed and why
2. Temporarily increase sensitivity of downstream layers to compensate
3. Analyze the bypass technique and update the failed layer
4. Run the full defense regression test suite
5. Verify that the updated defense stack blocks the bypass
6. Return defense sensitivities to normal levels
7. Document the incident and update the threat model

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 11a | Composing Defense Layers Against Combined Attacks | 50 minutes |
| Lab 11b | Defense Effectiveness Measurement and Tuning | 40 minutes |
| Lab 11c | False Positive Management and Usability Tradeoffs | 30 minutes |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Completed lab worksheet documenting defense composition and effectiveness
- [ ] Working multi-layer defense architecture with all five patterns
- [ ] Defense effectiveness report with detection rates, false positive rates, and latency measurements
- [ ] Passing security regression test suite (minimum 10 test cases across all defense layers)
- [ ] Evidence artifacts from `make evidence`

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | 1.0 hours |
| Lab Work | 1.5 hours |
| Exercises | 1.0 hours |
| Review & Deliverables | 0.5 hours |
| **Total** | **4.0 hours** |

---

## Prerequisites

- Completion of Classes 07-10
- Familiarity with all individual defense patterns (context separation, input validation, etc.)
- Working development environment

---

## References

1. OWASP Top 10 for LLM Applications (2025) — LLM01: Prompt Injection (defenses)
2. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety* — Defense in Depth
3. NIST SP 800-53 Rev. 5 — Control families: AC, AU, CM, IA, RA, SA, SC, SI
4. ISO/IEC 27001:2022 — Annex A Controls
5. "Prompt Injection Defenses" — Community-maintained defense catalog (2024)

---

*Class 11 | AI Security from Scratch*
