# AI Security Lab Report

## System Tested

| Field          | Value                                      |
|----------------|--------------------------------------------|
| System Name    |                                            |
| Version        |                                            |
| Test Date      |                                            |
| Tester         |                                            |
| Environment    |                                            |

---

## Control-Loop Summary

Describe the control-loop architecture of the system under test:
- **Reference signal**: What should the system do?
- **Controller**: How does the LLM make decisions?
- **Plant**: What external systems does the LLM affect?
- **Actuators**: What tools/APIs can the LLM invoke?
- **Sensors**: How does the system observe its environment?
- **Disturbances**: What external inputs can affect system behavior?

---

## Attack Scenario

| Field          | Value                                      |
|----------------|--------------------------------------------|
| Attack Type    |                                            |
| Attack Vector  |                                            |
| Target         |                                            |
| Attacker Model |                                            |

### Attack Description

[Detailed description of the attack scenario tested]

### Attack Steps

1. 
2. 
3. 

---

## Vulnerability

### Description

[What vulnerability was exploited or tested]

### Classification

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| OWASP LLM Top 10   |                                            |
| NIST AI RMF        |                                            |
| ISO 27001 Control  |                                            |
| Severity           | Critical / High / Medium / Low             |

---

## Impact

### Business Impact

[What is the potential business impact of this vulnerability?]

### Technical Impact

[What systems/data/operations are affected?]

### Likelihood

[How likely is this attack to succeed in practice?]

---

## Root Cause

### Control Failure Analysis

| Control Loop Element | Failure Mode | Description |
|---------------------|--------------|-------------|
| Reference signal    |              |             |
| Controller (LLM)    |              |             |
| Actuator (Tools)    |              |             |
| Sensor (Input)      |              |             |
| Feedback            |              |             |

### Why Existing Controls Failed

[Analysis of why the system's defenses did not prevent this vulnerability]

---

## Control Failure

| Field                | Value                                      |
|----------------------|--------------------------------------------|
| Failed Control       |                                            |
| Failure Type         | Missing / Insufficient / Bypassed / Misconfigured |
| Detection Method     |                                            |

---

## Defensive Control

### Recommended Controls

| Priority | Control | Description | Maps To |
|----------|---------|-------------|---------|
| P0       |         |             |         |
| P1       |         |             |         |
| P2       |         |             |         |

### Implementation Notes

[Specific implementation guidance for recommended controls]

---

## Test Evidence

### Test Case ID

| ID | Input | Expected | Actual | Pass/Fail |
|----|-------|----------|--------|-----------|
|    |       |          |        |           |
|    |       |          |        |           |

### Reproduction Steps

1. 
2. 
3. 

### Artifacts

- [ ] Screenshots
- [ ] Logs
- [ ] Network captures
- [ ] Control ledger events

---

## Monitoring Evidence

### Observable Indicators

| Indicator | Data Source | Threshold | Current |
|-----------|------------|-----------|---------|
|           |            |           |         |
|           |            |           |         |

### Control Ledger Events

[Relevant events from the control ledger]

---

## Residual Risk

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Risk Level         | Critical / High / Medium / Low / Acceptable |
| Accepted By        |                                            |
| Acceptance Date    |                                            |
| Next Review Date   |                                            |

### Residual Risk Description

[What risk remains after implementing recommended controls?]

---

## Recommendations

### Short-Term (0-30 days)

1. 
2. 
3. 

### Medium-Term (30-90 days)

1. 
2. 
3. 

### Long-Term (90+ days)

1. 
2. 
3. 

---

## Executive Summary

[A 2-3 paragraph summary suitable for leadership, covering: what was tested, what was found, what should be done]

---

## Sign-Off

| Role              | Name | Date | Signature |
|-------------------|------|------|-----------|
| Security Tester   |      |      |           |
| System Owner      |      |      |           |
| Risk Owner        |      |      |           |
| CISO / Approver   |      |      |           |
