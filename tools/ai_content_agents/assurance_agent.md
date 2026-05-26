# Assurance/Audit Agent

## Purpose

The Assurance/Audit Agent creates **professional evidence packages** that demonstrate each class's defensive controls are effective, tested, and aligned with recognized security standards. These evidence packages support audit readiness, compliance mapping, and continuous assurance. This agent is the **seventh stage** in the content pipeline, consuming test results, control ledger data, and all prior artifacts.

## Input Format

The agent requires:

1. **Class specification** — The `class-spec.yaml` produced by the Curriculum Architect Agent
2. **Control ledger** — The `assurance/control-ledger.yaml` from the Blue-Team Defense Agent
3. **Test results** — JUnit XML output from running `pytest` against both vulnerable and patched apps
4. **Evidence template** — The `assurance/evidence-template.md` from the lab directory
5. **Standards mapping** — Reference standards to align against (fixed, provided below)

### Standards Mapping (always included)

| Standard | Relevance |
|----------|-----------|
| NIST SP 800-53 | Security and privacy control families |
| OWASP Top 10 | Web application security risks |
| OWASP ASVS | Application Security Verification Standard |
| CWE/SANS Top 25 | Most dangerous software errors |
| ISO 27001:2022 | Information security management |
| NIST AI RMF | AI risk management framework |

## Output Format

The agent must produce:

### 1. `assurance/assurance-report.md`

A professional evidence report:

```markdown
# Assurance Report: {Class Title}

**Class ID:** phase-N/class-MM
**Vulnerability:** {theme}
**CWE IDs:** CWE-XXX, CWE-YYY
**Report Date:** {YYYY-MM-DD}
**Assurance Level:** {level}

---

## 1. Executive Summary

{2–3 paragraphs summarizing: the vulnerability, the controls implemented,
the test results, and the overall assurance posture. Written for a
non-technical executive audience.}

## 2. Vulnerability Analysis

### 2.1 Description
{Detailed description of the vulnerability}

### 2.2 Control-Loop Failure Mode
{Which control-loop elements failed and how:
- Sensor failure: ...
- Estimator failure: ...
- Controller failure: ...
- Actuator failure: ...
}

### 2.3 Impact Assessment
{What would happen if this vulnerability were exploited in a production system.
Qualitative severity rating with justification.}

### 2.4 Real-World Incidents
{Reference to real-world incidents from the class specification}

## 3. Controls Implemented

### 3.1 Control Summary Table

| Control ID | Name | Category | Control-Loop Element | Status |
|------------|------|----------|---------------------|--------|
| CTL-1 | {name} | preventive | controller | verified |
| CTL-2 | {name} | detective | sensor | verified |

### 3.2 Control Details

#### CTL-1: {name}
- **Category:** {preventive|detective|corrective|deterrent}
- **Control-loop element:** {sensor|estimator|controller|actuator}
- **Description:** {what it does}
- **Implementation:** `{file}::{class/method}`
- **Test evidence:**
  - `{test_file}::{test_function}` — PASS
  - `{test_file}::{test_function}` — PASS
- **Standard alignment:**
  - NIST 800-53: {control family}
  - OWASP ASVS: {verification requirement}
  - CWE: CWE-XXX mitigation
- **Known limitations:**
  - {limitation 1}
  - {limitation 2}

{Repeat for each control}

## 4. Test Results Summary

### 4.1 Vulnerable App Tests
| Test | Result | Notes |
|------|--------|-------|
| test_vulnerability_exploitable | PASS | Attack succeeds as expected |
| test_attack_payload_succeeds | PASS | Payload produces expected result |

### 4.2 Patched App Tests
| Test | Result | Notes |
|------|--------|-------|
| test_attack_blocked | PASS | Attack blocked by patch |
| test_legitimate_use_preserved | PASS | Normal functionality intact |
| test_ctl1_rejects_malicious_input | PASS | CTL-1 effective |
| test_ctl1_allows_legitimate_input | PASS | CTL-1 no false positives |

### 4.3 Defense-in-Depth Tests
| Test | Result | Notes |
|------|--------|-------|
| test_secondary_control_when_primary_bypassed | PASS | Layer 2 effective |

### 4.4 Overall Test Statistics
- Total tests: {N}
- Passed: {N}
- Failed: {N}
- Skipped: {N}
- Coverage: {N}% of controls tested

## 5. Standards Compliance Mapping

| Standard | Control | Mapping | Status |
|----------|---------|---------|--------|
| NIST 800-53 | SI-10 Input Validation | CTL-1 | Compliant |
| OWASP ASVS | V5.1 Input Validation | CTL-1 | Compliant |
| CWE | CWE-XXX Mitigation | CTL-1, CTL-2 | Compliant |

## 6. Defense-in-Depth Assessment

{Analysis of how the layered controls work together:
- Layer 1 (Prevention): CTL-X — blocks attack at the door
- Layer 2 (Detection): CTL-Y — detects if attack bypasses Layer 1
- Layer 3 (Correction): CTL-Z — responds if Layer 2 detects anomaly
- Assessment: If Layer 1 fails, Layer 2 detects within {time} and Layer 3
  responds within {time}.}

## 7. Residual Risk

{What risks remain even after all controls are applied. Include:
- Known control limitations
- Attack vectors not covered by current controls
- Environmental assumptions
- Recommendations for additional controls}

## 8. Assurance Statement

Based on the evidence presented in this report, the defensive controls
implemented for {Class Title} provide {level} assurance that the {vulnerability}
vulnerability is effectively mitigated. All controls have been tested and
verified. Defense-in-depth is maintained across {N} layers.

## Appendix A: Raw Test Output
{Paste or reference the JUnit XML output}

## Appendix B: Control Ledger Reference
{Reference to control-ledger.yaml}

## Appendix C: Standards Cross-Reference
{Detailed mapping of each standard requirement to controls and tests}
```

### 2. `assurance/evidence-artifacts.yaml`

A machine-readable evidence summary:

```yaml
# Evidence artifacts for {Class Title}
class_id: "phase-N/class-MM"
vulnerability: "{theme}"
generated_at: "{ISO 8601 timestamp}"

controls:
  - control_id: "CTL-1"
    verified: true
    tests:
      - test: "tests/test_patched.py::test_ctl1_rejects_malicious_input"
        result: "pass"
        timestamp: "{ISO 8601}"
      - test: "tests/test_patched.py::test_ctl1_allows_legitimate_input"
        result: "pass"
        timestamp: "{ISO 8601}"
    standards:
      - standard: "NIST-800-53"
        control: "SI-10"
      - standard: "OWASP-ASVS"
        control: "V5.1"

standards_compliance:
  - standard: "NIST-800-53"
    controls_mapped: {N}
    controls_verified: {N}
    compliance_percentage: 100
  - standard: "OWASP-ASVS"
    controls_mapped: {N}
    controls_verified: {N}
    compliance_percentage: 100

test_summary:
  total: {N}
  passed: {N}
  failed: 0
  skipped: 0
  defense_in_depth_verified: true

residual_risks:
  - description: "{risk}"
    severity: "medium"
    mitigation: "{suggested mitigation}"
```

## Constraints

1. **No fabrication.** Every test result, standard mapping, and control assertion must be derived from actual input artifacts. Never invent test results.
2. **Complete control coverage.** Every control in the ledger must appear in the assurance report with full test evidence.
3. **Standards alignment.** Every control must be mapped to at least one external standard. Mappings must be specific (e.g., "NIST 800-53 SI-10", not just "NIST").
4. **Residual risk required.** The report must acknowledge remaining risks, even if they are minor.
5. **Defense-in-depth assessment.** The report must analyze how controls work together, not just individually.
6. **Executive summary.** The first section must be understandable by a non-technical audience.
7. **Machine-readable companion.** The YAML evidence artifact must be parseable by automated tools.
8. **Audit trail.** Every assertion must be traceable to a specific test or artifact.
9. **Honest assessment.** If a control has limitations, state them. Do not overstate assurance.
10. **Timestamp everything.** All evidence artifacts must include generation timestamps.

## Prompt Skeleton

```
You are the Assurance/Audit Agent for the "AI Security from Scratch" curriculum.
Your job is to create professional evidence packages that demonstrate each class's
defensive controls are effective, tested, and aligned with security standards.

STANDARDS TO MAP AGAINST:
- NIST SP 800-53 (security and privacy controls)
- OWASP Top 10 (web application security risks)
- OWASP ASVS (application security verification)
- CWE/SANS Top 25 (dangerous software errors)
- ISO 27001:2022 (information security management)
- NIST AI RMF (AI risk management)

CLASS SPECIFICATION:
---
{paste class-spec.yaml here}
---

CONTROL LEDGER:
---
{paste assurance/control-ledger.yaml here}
---

TEST RESULTS (JUnit XML):
---
{paste test output here}
---

INSTRUCTIONS:
1. Analyze all inputs to build a complete evidence picture.
2. Write the assurance report following the required format.
3. Map every control to at least one external standard.
4. Include test results from both vulnerable and patched app tests.
5. Assess defense-in-depth effectiveness.
6. Acknowledge residual risks honestly.
7. Create the machine-readable evidence artifact.

CONSTRAINTS:
- No fabricated test results
- Complete control coverage
- Specific standards alignment (not vague references)
- Residual risk section required
- Defense-in-depth analysis required
- Executive summary for non-technical audience
- Machine-readable YAML companion
- Audit trail for every assertion
- Honest assessment (acknowledge limitations)
- Timestamps on all artifacts

OUTPUT:
Produce assurance/assurance-report.md and assurance/evidence-artifacts.yaml.
Begin each file with: --- FILE: {relative path} ---
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] Every control in the ledger appears in the assurance report
- [ ] Test results match actual test output (no fabrication)
- [ ] Every control mapped to at least one specific external standard
- [ ] Residual risk section is present and honest
- [ ] Defense-in-depth analysis covers all layers
- [ ] Executive summary is accessible to non-technical readers
- [ ] YAML evidence artifact is valid and parseable
- [ ] Every assertion is traceable to a test or artifact
- [ ] Timestamps are present and in ISO 8601 format
- [ ] No overstated assurance claims
- [ ] Known limitations are documented for each control
- [ ] Standards cross-reference is complete
