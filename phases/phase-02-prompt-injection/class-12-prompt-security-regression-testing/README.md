# Prompt Security Regression Testing

> **Module:** Phase 2 — Prompt Injection | **Class:** 12 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Convert prompt injection attack scenarios into automated pytest security regression tests
2. Design a security test harness that exercises both positive (attack blocked) and negative (legitimate use preserved) test cases
3. Implement test fixtures and parameterized test suites that cover the full spectrum of prompt injection attacks
4. Integrate security regression tests into a CI/CD pipeline for continuous validation
5. Generate auditable evidence from test runs that supports compliance and assurance requirements

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for security regression testing.

### Objective

The safety goal the system must maintain:

> Ensure that every known prompt injection attack is continuously validated against the defense stack, and that any regression in defense effectiveness is detected immediately and prevented from reaching production.

### Controller

The component responsible for making decisions to maintain the objective:

> The security regression test harness — an automated testing framework that executes a comprehensive suite of attack simulations and legitimate-use verifications on every code change, comparing results against expected security outcomes and blocking deployments that introduce regressions.

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Test pass/fail results | Security test harness | Per CI run |
| Per-attack defense effectiveness | Test result database | Per CI run |
| False positive rate (legitimate inputs blocked) | Negative test results | Per CI run |
| Defense latency impact | Test performance metrics | Per CI run |
| Test coverage percentage | Coverage analysis tool | Per CI run |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Block deployment | Prevents code with security regressions from reaching production | Security test failure detected |
| Alert on new bypass | Notifies security team of previously-unknown attack success | Test reveals new failure |
| Generate evidence report | Produces compliance-ready documentation | Test run completes |
| Flag coverage gap | Identifies attack categories not covered by tests | Coverage analysis reveals gap |
| Update test baseline | Adjusts expected results for intentional defense changes | Defense tuning verified by security team |

### Feedback

How the controller learns whether its actions achieved the objective:

> Test results feed back into the test maintenance cycle. When a new attack is discovered in production, it is converted into a test case and added to the regression suite. When a defense is updated, the expected results for affected tests are updated after verification. Coverage analysis identifies gaps that inform new test case development.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| LLM output non-determinism | Model temperature and sampling | Deterministic test configuration + retry logic |
| New attack variants not in test suite | Evolving threat landscape | Regular test suite updates + red team input |
| Test flakiness from API latency | External service dependencies | Timeouts + mocking + retry thresholds |
| False test confidence from narrow coverage | Incomplete test design | Coverage analysis + attack category taxonomy |
| Test suite drift from changing model behavior | Model updates | Baseline recalibration process |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Regression in production | Security test not run before deployment | Known attack succeeds against production system |
| False confidence | Tests pass but don't cover real attack vectors | Security theater instead of real security |
| Test suite rot | Tests not updated as defenses evolve | Tests validate obsolete behavior |
| Coverage gap | Attack categories missing from test suite | Unknown vulnerabilities in production |
| Non-deterministic tests | LLM output variability causes intermittent failures | Tests ignored or disabled |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> A test coverage dashboard that tracks the percentage of known attack categories covered by the regression suite, the pass/fail trend over time, and the mean time between test failure and resolution. A deployment gate that blocks any deployment not accompanied by a passing security test run. A quarterly red-team review that validates the test suite against the current threat landscape.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Security test pass rate | < 100% on known attacks | Deployment blocked |
| Test coverage (attack categories) | < 90% | Coverage gap alert |
| Test flakiness rate | > 5% | Test maintenance alert |
| Mean time to fix (security test failures) | > 24 hours | Engineering alert |
| Time since last test suite update | > 30 days | Staleness alert |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Immediately block the deployment that introduced the regression
2. Identify the specific test failure and the defense layer that regressed
3. Root-cause the regression (code change, model update, or new attack variant)
4. Fix the defense and verify with the failing test
5. Run the full regression suite to confirm no additional regressions
6. Document the regression, the fix, and the evidence
7. Add a variant test case to prevent similar regressions

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 12a | Converting Attack Scenarios to pytest Tests | 45 minutes |
| Lab 12b | Building the Security Test Harness | 45 minutes |
| Lab 12c | CI Integration and Evidence Generation | 30 minutes |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Completed lab worksheet documenting test design decisions
- [ ] Working security regression test suite (minimum 20 test cases across all attack categories)
- [ ] Test harness with positive and negative test cases, fixtures, and parameterization
- [ ] CI pipeline configuration that runs security tests on every PR
- [ ] Evidence generation script producing JUnit XML + compliance report
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

- Completion of Classes 07-11 (all prompt injection attack and defense classes)
- Familiarity with pytest, fixtures, and parameterized testing
- Working development environment with CI/CD access
- Understanding of the control-loop model and defense-in-depth architecture

---

## References

1. OWASP Top 10 for LLM Applications (2025) — LLM01: Prompt Injection (testing guidance)
2. NIST SP 800-53 Rev. 5 — CA-2: Security Assessments, SA-11: Development Security Testing
3. Leveson, N. (2011). *Engineering a Safer World* — Safety-Guided Design and Testing
4. ISO/IEC 29119: Software Testing Standards
5. "Automated Security Testing for LLM Applications" — Emerging practices (2024)

---

*Class 12 | AI Security from Scratch*
