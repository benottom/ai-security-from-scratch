---
name: Bug Report
about: Report a bug in lab code, documentation, or tooling
title: "[BUG] "
labels: ["bug", "needs-triage"]
assignees: []
---

## Bug Category

<!-- Select the category that best describes this bug: -->

- [ ] **Lab code bug** — Vulnerable or patched application does not work as expected
- [ ] **Attack script bug** — Attack script does not work as expected
- [ ] **Test bug** — Test fails when it should pass, or passes when it should fail
- [ ] **Documentation error** — Lesson, README, or other documentation contains incorrect information
- [ ] **Tool bug** — Validator, report generator, or other tool does not work correctly
- [ ] **Security concern** — Found a safety issue in attack scripts, missing safety markers, or unintended vulnerability

## Affected Class

<!-- Which class/phase is affected? Leave blank if not class-specific. -->

**Phase:** 
**Class ID:** (e.g., phase-2/class-07)

## Description

<!-- Clearly describe what is wrong. What happened? What did you expect to happen? -->

## Steps to Reproduce

<!-- Provide step-by-step instructions to reproduce the bug. -->

1.
2.
3.
4.

## Expected Behavior

<!-- What should happen instead? -->

## Actual Behavior

<!-- What actually happened? Include error messages, stack traces, or screenshots. -->

## Environment

<!-- Help us reproduce the issue. -->

- **OS:** (e.g., Ubuntu 22.04, macOS 14, Windows 11)
- **Python version:** (e.g., 3.11.5)
- **Browser:** (if relevant, e.g., Chrome 120)
- **Dependencies installed from:** requirements.txt / pip / other

## Security Considerations

<!-- If this is a security concern, answer the following:
  - Does the attack script target non-localhost addresses?
  - Is there missing safety markup in attack files?
  - Does the patched app still contain the vulnerability?
  - Can the attack be used against real external targets?
  
  For critical security issues, consider reporting privately instead of
  filing a public issue. -->

- [ ] This bug has security implications
- [ ] This bug involves a safety marker violation
- [ ] This bug means the patch does not actually fix the vulnerability

## Additional Context

<!-- Any other relevant information: screenshots, logs, related issues, etc. -->

## Possible Fix

<!-- If you have a suggestion for how to fix this, describe it here. -->
