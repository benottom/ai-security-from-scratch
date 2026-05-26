# [CLASS TITLE]

> **Module:** [MODULE NAME] | **Class:** [CLASS NUMBER] | **Duration:** [ESTIMATED HOURS] hours

## Learning Objectives

By the end of this class, students will be able to:

1. [OBJECTIVE_1]
2. [OBJECTIVE_2]
3. [OBJECTIVE_3]
4. [OBJECTIVE_4]
5. [OBJECTIVE_5]

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for the topic covered in this class.

### Objective

The safety goal the system must maintain:

> [CONTROL_OBJECTIVE — e.g., "Ensure that user-supplied input never influences system-level instructions."]

### Controller

The component responsible for making decisions to maintain the objective:

> [CONTROLLER — e.g., "The context-separation firewall inspects and classifies every token before it enters the model context window."]

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| [OBSERVATION_1] | [SOURCE_1] | [FREQUENCY_1] |
| [OBSERVATION_2] | [SOURCE_2] | [FREQUENCY_2] |
| [OBSERVATION_3] | [SOURCE_3] | [FREQUENCY_3] |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| [ACTION_1] | [EFFECT_1] | [PRECONDITION_1] |
| [ACTION_2] | [EFFECT_2] | [PRECONDITION_2] |
| [ACTION_3] | [EFFECT_3] | [PRECONDITION_3] |

### Feedback

How the controller learns whether its actions achieved the objective:

> [FEEDBACK_DESCRIPTION — e.g., "Post-generation output classification confirms whether system-instruction leakage occurred, feeding back into the firewall rule set."]

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| [DISTURBANCE_1] | [SOURCE_1] | [MITIGATION_1] |
| [DISTURBANCE_2] | [SOURCE_2] | [MITIGATION_2] |
| [DISTURBANCE_3] | [SOURCE_3] | [MITIGATION_3] |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| [UNSAFE_STATE_1] | [CONDITION_1] | [CONSEQUENCE_1] |
| [UNSAFE_STATE_2] | [CONDITION_2] | [CONSEQUENCE_2] |
| [UNSAFE_STATE_3] | [CONDITION_3] | [CONSEQUENCE_3] |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> [SUPERVISORY_CONTROL — e.g., "A human-approval gate that intercepts any action classified as high-risk before execution, with a configurable timeout that defaults to denial."]

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| [METRIC_1] | [THRESHOLD_1] | [ALERT_1] |
| [METRIC_2] | [THRESHOLD_2] | [ALERT_2] |
| [METRIC_3] | [THRESHOLD_3] | [ALERT_3] |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. [RECOVERY_STEP_1]
2. [RECOVERY_STEP_2]
3. [RECOVERY_STEP_3]

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| [LAB_1_NAME] | [LAB_1_TOPIC] | [LAB_1_DURATION] |
| [LAB_2_NAME] | [LAB_2_TOPIC] | [LAB_2_DURATION] |
| [LAB_3_NAME] | [LAB_3_TOPIC] | [LAB_3_DURATION] |

Each lab follows the standard 8-step flow:

1. Start the vulnerable application
2. Run a normal test to establish baseline behavior
3. Execute the attack
4. Observe the failure
5. Explain the control-loop failure
6. Implement the defense
7. Run the security regression test
8. Generate evidence

---

## Deliverables

- [ ] [DELIVERABLE_1 — e.g., "Completed lab worksheet with control-loop analysis"]
- [ ] [DELIVERABLE_2 — e.g., "Passing security regression test suite"]
- [ ] [DELIVERABLE_3 — e.g., "Threat model document for the lab scenario"]
- [ ] [DELIVERABLE_4 — e.g., "Written explanation of the control-loop failure and remediation"]
- [ ] [DELIVERABLE_5 — e.g., "Evidence artifacts from `make evidence`"]

---

## Estimated Time

| Activity | Duration |
|---|---|
| Lecture / Reading | [LECTURE_HOURS] hours |
| Lab Work | [LAB_HOURS] hours |
| Exercises | [EXERCISE_HOURS] hours |
| Review & Deliverables | [REVIEW_HOURS] hours |
| **Total** | **[TOTAL_HOURS] hours** |

---

## Prerequisites

- [PREREQUISITE_1 — e.g., "Completion of Class [N]: [PREVIOUS_CLASS_TITLE]"]
- [PREREQUISITE_2 — e.g., "Familiarity with [TECHNOLOGY/CONCEPT]"]
- [PREREQUISITE_3 — e.g., "Working development environment (see setup guide)"]

---

## References

1. [REFERENCE_1 — e.g., "NIST AI Risk Management Framework (AI RMF 1.0)"]
2. [REFERENCE_2 — e.g., "OWASP Top 10 for LLM Applications (2025)"]
3. [REFERENCE_3 — e.g., "Leveson, N. (2011). Engineering a Safer World: Systems Thinking Applied to Safety"]
4. [REFERENCE_4 — e.g., "ISO/IEC 27001:2022 — Information Security Management Systems"]
5. [REFERENCE_5 — e.g., "Relevant academic paper or industry report"]

---

*Template version: 1.0.0 | AI Security from Scratch*
