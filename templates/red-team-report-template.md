# Red Team Report: [ENGAGEMENT_NAME]

> **Classification:** [CONFIDENTIAL|INTERNAL] | **Date:** [DATE] | **Lead:** [LEAD_NAME] | **Engagement ID:** [ENG-XXXX]

---

## Executive Summary

[Provide a 3–5 paragraph executive summary suitable for C-suite and board-level audiences. Cover: what was tested, the overall security posture, the most critical findings, and the top-priority recommendations. Write in plain language without jargon.]

**Overall Risk Rating:** [CRITICAL|HIGH|MEDIUM|LOW]

**Key Findings:**
- [CRITICAL_FINDING_1 — e.g., "System prompt fully extractable via prompt injection, enabling complete control of AI behavior"]
- [CRITICAL_FINDING_2 — e.g., "Tool execution gateway lacks parameter validation, allowing unauthorized API calls"]
- [HIGH_FINDING_1 — e.g., "RAG pipeline returns documents regardless of user authorization level"]
- [MEDIUM_FINDING_1 — e.g., "Insufficient rate limiting enables automated probing"]

**Positive Observations:**
- [POSITIVE_1 — e.g., "API gateway enforces TLS and authentication consistently"]
- [POSITIVE_2 — e.g., "Audit logging captures most security-relevant events"]

---

## Scope and Rules of Engagement

### Scope

| Dimension | In Scope | Out of Scope |
|---|---|---|
| **Systems** | [SYSTEMS_IN_SCOPE] | [SYSTEMS_OUT_OF_SCOPE] |
| **Attack Vectors** | [VECTORS_IN_SCOPE] | [VECTORS_OUT_OF_SCOPE] |
| **Data** | [DATA_IN_SCOPE] | [DATA_OUT_OF_SCOPE] |
| **Time Period** | [START_DATE] — [END_DATE] | — |
| **Environments** | [ENVIRONMENTS] | Production data exfiltration |

### Rules of Engagement

1. **No denial of service:** Attacks must not degrade system availability for other users.
2. **No data exfiltration from production:** Demonstrated POC only; no real data removed.
3. **No social engineering of staff:** Technical attacks only.
4. **Full coordination:** All activities logged and reported to [POINT_OF_CONTACT].
5. **Stop on critical finding:** If a critical vulnerability is confirmed, immediately notify [POINT_OF_CONTACT] before continuing.
6. [ADDITIONAL_ROE_1]
7. [ADDITIONAL_ROE_2]

### Methodology

This engagement follows the **AI Security from Scratch** red-teaming methodology, grounded in control-theoretic analysis:

1. Threat model review and control-loop decomposition
2. Attack surface mapping and reconnaissance
3. Control-loop failure scenario development
4. Attack execution and evidence collection
5. Control-theoretic root cause analysis
6. Remediation recommendations with control-loop restoration

---

## System Under Test

| Attribute | Value |
|---|---|
| **System Name** | [SYSTEM_NAME] |
| **Version** | [VERSION] |
| **Environment** | [STAGING|PRODUCTION|DEVELOPMENT] |
| **Architecture** | [BRIEF_ARCHITECTURE_DESCRIPTION] |
| **Primary AI Model** | [MODEL_NAME_AND_VERSION] |
| **Key Integrations** | [INTEGRATION_LIST] |
| **Authentication** | [AUTH_MECHANISM] |
| **Deployment** | [CLOUD_PROVIDER / ON-PREM] |

---

## Findings Summary

| ID | Severity | Category | Description | Control Failure |
|---|---|---|---|---|
| RT-01 | 🔴 Critical | [CATEGORY_1 — e.g., Prompt Injection] | [BRIEF_DESCRIPTION_1] | [CONTROL_FAILURE_1] |
| RT-02 | 🔴 Critical | [CATEGORY_2] | [BRIEF_DESCRIPTION_2] | [CONTROL_FAILURE_2] |
| RT-03 | 🟠 High | [CATEGORY_3] | [BRIEF_DESCRIPTION_3] | [CONTROL_FAILURE_3] |
| RT-04 | 🟠 High | [CATEGORY_4] | [BRIEF_DESCRIPTION_4] | [CONTROL_FAILURE_4] |
| RT-05 | 🟡 Medium | [CATEGORY_5] | [BRIEF_DESCRIPTION_5] | [CONTROL_FAILURE_5] |
| RT-06 | 🟡 Medium | [CATEGORY_6] | [BRIEF_DESCRIPTION_6] | [CONTROL_FAILURE_6] |
| RT-07 | 🔵 Low | [CATEGORY_7] | [BRIEF_DESCRIPTION_7] | [CONTROL_FAILURE_7] |

**Severity Distribution:**
- 🔴 Critical: [N]
- 🟠 High: [N]
- 🟡 Medium: [N]
- 🔵 Low: [N]

---

## Detailed Findings

### RT-01: [FINDING_TITLE]

**Severity:** 🔴 Critical
**Category:** [CATEGORY]
**CVSS Score:** [SCORE]
**Affected Components:** [COMPONENT_LIST]

#### Description

[Detailed description of the vulnerability, including what was found, why it exists, and its security implications. Provide enough detail for the engineering team to understand the issue without needing to reproduce it first.]

#### Reproduction Steps

1. [STEP_1 — e.g., "Authenticate as a standard user via the API gateway"]
2. [STEP_2 — e.g., "Submit the following prompt: `[ATTACK_PAYLOAD]`"]
3. [STEP_3 — e.g., "Observe the model response, which contains: `[LEAKED_CONTENT]`"]
4. [STEP_4]
5. [STEP_5]

**Reproducibility:** [ALWAYS|MOSTLY|SOMETIMES|RARELY]

#### Control-Loop Analysis

| Element | Status | Analysis |
|---|---|---|
| **Objective** | ❌ Violated | [WHY_VIOLATED] |
| **Controller** | ❌ Absent/Failed | [WHY_FAILED] |
| **Observations** | ❌ Blind spot | [WHAT_WAS_MISSED] |
| **Actions** | ❌ No corrective action taken | [WHAT_SHOULD_HAVE_HAPPENED] |
| **Feedback** | ❌ No feedback to controller | [WHY_NO_FEEDBACK] |
| **Disturbance** | ⚠️ Unmitigated | [WHAT_DISTURBANCE_SUCCEEDED] |

**Root Cause:** [ROOT_CAUSE_ANALYSIS_FROM_CONTROL_LOOP_PERSPECTIVE]

#### Impact

- **Confidentiality:** [IMPACT_DESCRIPTION]
- **Integrity:** [IMPACT_DESCRIPTION]
- **Availability:** [IMPACT_DESCRIPTION]
- **Business Impact:** [BUSINESS_IMPACT_DESCRIPTION]

#### Evidence

```
[ATTACK_LOGS, SCREENSHOT_DESCRIPTIONS, OUTPUT_CAPTURES, TIMESTAMPS]
```

**Evidence artifacts:** [LINK_TO_EVIDENCE_DIRECTORY]

#### Remediation

**Immediate (P1):**
- [IMMEDIATE_FIX_1]
- [IMMEDIATE_FIX_2]

**Long-term (P2):**
- [LONG_TERM_FIX_1]
- [LONG_TERM_FIX_2]

**Control-loop restoration:**
- Add controller: [CONTROLLER_SPECIFICATION]
- Add observations: [OBSERVATION_SPECIFICATION]
- Add actions: [ACTION_SPECIFICATION]
- Add feedback: [FEEDBACK_SPECIFICATION]

---

### RT-02: [FINDING_TITLE]

**Severity:** 🟠 High
**Category:** [CATEGORY]
**CVSS Score:** [SCORE]
**Affected Components:** [COMPONENT_LIST]

#### Description

[Detailed description]

#### Reproduction Steps

1. [STEP_1]
2. [STEP_2]
3. [STEP_3]
4. [STEP_4]

**Reproducibility:** [ALWAYS|MOSTLY|SOMETIMES|RARELY]

#### Control-Loop Analysis

| Element | Status | Analysis |
|---|---|---|
| **Objective** | ❌/⚠️/✅ | [ANALYSIS] |
| **Controller** | ❌/⚠️/✅ | [ANALYSIS] |
| **Observations** | ❌/⚠️/✅ | [ANALYSIS] |
| **Actions** | ❌/⚠️/✅ | [ANALYSIS] |
| **Feedback** | ❌/⚠️/✅ | [ANALYSIS] |
| **Disturbance** | ❌/⚠️/✅ | [ANALYSIS] |

**Root Cause:** [ROOT_CAUSE]

#### Impact

- **Confidentiality:** [IMPACT]
- **Integrity:** [IMPACT]
- **Availability:** [IMPACT]
- **Business Impact:** [IMPACT]

#### Evidence

```
[EVIDENCE_CAPTURE]
```

#### Remediation

**Immediate:**
- [FIX_1]

**Long-term:**
- [FIX_2]

---

### RT-03: [FINDING_TITLE]

*(Continue the same structure for each finding)*

---

## Attack Tree Diagram

```mermaid
graph TD
    GOAL[Attacker Goal: [ATTACK_GOAL]]

    GOAL --> A1[Attack Vector 1: [VECTOR_1]]
    GOAL --> A2[Attack Vector 2: [VECTOR_2]]
    GOAL --> A3[Attack Vector 3: [VECTOR_3]]

    A1 --> A1a[Step 1a: [STEP]]
    A1 --> A1b[Step 1b: [STEP]]
    A1a --> A1a1[Step 1a.1: [STEP]]
    A1a --> A1a2[Step 1a.2: [STEP]]
    A1b --> A1b1[Step 1b.1: [STEP]]

    A2 --> A2a[Step 2a: [STEP]]
    A2 --> A2b[Step 2b: [STEP]]

    A3 --> A3a[Step 3a: [STEP]]
    A3 --> A3b[Step 3b: [STEP]]

    style GOAL fill:#ff4444,color:#fff
    style A1 fill:#ff8800,color:#fff
    style A2 fill:#ff8800,color:#fff
    style A3 fill:#ff8800,color:#fff
```

---

## Summary of Control Failures

| Control Objective | Findings That Violate It | Primary Failure Mode | Recommended Control Pattern |
|---|---|---|---|
| [OBJECTIVE_1] | RT-01, RT-03 | [FAILURE_MODE] | [PATTERN_NAME] |
| [OBJECTIVE_2] | RT-02, RT-04 | [FAILURE_MODE] | [PATTERN_NAME] |
| [OBJECTIVE_3] | RT-05 | [FAILURE_MODE] | [PATTERN_NAME] |
| [OBJECTIVE_4] | RT-06, RT-07 | [FAILURE_MODE] | [PATTERN_NAME] |

**Common failure patterns identified:**
1. [COMMON_FAILURE_1 — e.g., "Missing controllers at trust boundaries"]
2. [COMMON_FAILURE_2 — e.g., "No feedback loops from output validation to input processing"]
3. [COMMON_FAILURE_3 — e.g., "Insufficient observation of internal model state"]

---

## Recommendations

### Priority 1 — Critical (Remediate within 7 days)

| Rec ID | Finding(s) | Recommendation | Control Pattern | Estimated Effort |
|---|---|---|---|---|
| REC-01 | RT-01 | [RECOMMENDATION] | [PATTERN] | [EFFORT] |
| REC-02 | RT-02 | [RECOMMENDATION] | [PATTERN] | [EFFORT] |

### Priority 2 — High (Remediate within 30 days)

| Rec ID | Finding(s) | Recommendation | Control Pattern | Estimated Effort |
|---|---|---|---|---|
| REC-03 | RT-03 | [RECOMMENDATION] | [PATTERN] | [EFFORT] |
| REC-04 | RT-04 | [RECOMMENDATION] | [PATTERN] | [EFFORT] |

### Priority 3 — Medium (Remediate within 90 days)

| Rec ID | Finding(s) | Recommendation | Control Pattern | Estimated Effort |
|---|---|---|---|---|
| REC-05 | RT-05, RT-06 | [RECOMMENDATION] | [PATTERN] | [EFFORT] |

### Strategic Recommendations

1. [STRATEGIC_REC_1 — e.g., "Implement a centralized AI Security Gateway as a control point for all model interactions"]
2. [STRATEGIC_REC_2 — e.g., "Adopt control-ledger logging for all security-relevant decisions to support assurance evidence"]
3. [STRATEGIC_REC_3 — e.g., "Establish a recurring red-team cadence (quarterly) with evolving attack scenarios"]

---

## Appendices

### A. Tools Used

| Tool | Purpose | Version |
|---|---|---|
| [TOOL_1] | [PURPOSE] | [VERSION] |
| [TOOL_2] | [PURPOSE] | [VERSION] |
| [TOOL_3] | [PURPOSE] | [VERSION] |

### B. Test Timeline

| Date | Activity | Findings |
|---|---|---|
| [DATE_1] | [ACTIVITY_1] | [FINDINGS] |
| [DATE_2] | [ACTIVITY_2] | [FINDINGS] |
| [DATE_3] | [ACTIVITY_3] | [FINDINGS] |

### C. Evidence Archive

- Location: [EVIDENCE_STORAGE_LOCATION]
- Hash (SHA-256): [EVIDENCE_HASH]
- Retention: [RETENTION_POLICY]

---

*Template version: 1.0.0 | AI Security from Scratch*
