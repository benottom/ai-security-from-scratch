# Pull Request

## Summary

<!-- Brief description of what this PR does and why. Link to any related issues. -->

Related to: #

## Type of Change

- [ ] **New class** — Adding a complete new class (lesson + lab + tests + assurance)
- [ ] **New lab** — Adding a new lab to an existing class
- [ ] **Bug fix** — Fixing a bug in existing code or content
- [ ] **Content update** — Updating lesson content, documentation, or explanations
- [ ] **Security patch** — Fixing a vulnerability in patched code or strengthening a control
- [ ] **Tool update** — Updating validator, report generator, or other tooling
- [ ] **CI/CD** — Updating workflows or automation
- [ ] **Maintenance** — Dependency updates, link fixes, consistency improvements

## Files Added/Modified

<!-- List the key files changed. For new classes, list all new files. -->

| File | Action | Description |
|------|--------|-------------|
| | Added/Modified/Deleted | |

---

## Lab Tested Checklist

<!-- Complete this section if the PR includes lab code changes. -->

- [ ] **Vulnerable app runs:** `python vulnerable/app.py` starts without errors
- [ ] **Vulnerable app health check:** `GET /health` returns `{"status": "ok"}`
- [ ] **Attack works locally:** `python attacks/attack.py` exits with code 0 against vulnerable app
- [ ] **Patched app runs:** `python patched/app.py` starts without errors
- [ ] **Patched app health check:** `GET /health` returns `{"status": "ok"}`
- [ ] **Attack fails against patch:** `python attacks/attack.py` exits with code 1 against patched app
- [ ] **Security tests pass:** `pytest tests/test_patched.py` — all tests pass
- [ ] **Vulnerability tests pass:** `pytest tests/test_vulnerable.py` — all tests pass
- [ ] **CI passes:** All GitHub Actions checks pass

---

## Safety Review Checklist

<!-- Complete this section if the PR includes attack scripts or vulnerability code. -->

- [ ] **Localhost-only:** Attack script validates target is localhost before proceeding
- [ ] **No exfiltration:** Attack script does not transmit data outside the lab environment
- [ ] **No persistence:** Attack script does not install backdoors or modify system files
- [ ] **No OS privilege escalation:** Attack script does not attempt OS-level privilege escalation
- [ ] **Safety markers present:** Attack files contain `<!-- SAFETY: ... -->` or `# SAFETY:` markers
- [ ] **Deterministic:** Attack uses fixed payloads and seeded random values
- [ ] **Bounded duration:** Attack completes within 60 seconds
- [ ] **No denial-of-service:** Attack does not crash the target application
- [ ] **Annotations present:** Vulnerable code has `# VULNERABLE:` comments; patched code has `# PATCH:` comments

---

## Content Review Checklist

<!-- Complete this section if the PR includes lesson or documentation content. -->

- [ ] **Control-loop mapping complete:** All 7 elements present (sensor, estimator, controller, actuator, plant, disturbance, reference)
- [ ] **Learning objectives measurable:** Objectives use Bloom's taxonomy verbs
- [ ] **Real-world example included:** At least one documented real-world incident with citation
- [ ] **CWE mapping present:** Vulnerability maps to at least one CWE ID
- [ ] **Defense in depth:** At least 2 layers of defense (preventive + detective/corrective)
- [ ] **Control ledger updated:** `assurance/control-ledger.yaml` reflects current controls
- [ ] **Glossary entries:** New terms defined in the lesson glossary
- [ ] **Terminology consistent:** Same terms used consistently across lesson, lab README, and attack README
- [ ] **No victim-blaming language:** Vulnerabilities described as system design issues, not developer failures
- [ ] **No dramatic/sensational language:** Attacks described factually

---

## Screenshots / Evidence

<!-- If applicable, include screenshots of:
  - Attack running against vulnerable app (showing success)
  - Attack running against patched app (showing failure)
  - Test results (pytest output)
  - App health checks
-->

---

## Additional Notes

<!-- Anything else reviewers should know? Breaking changes? Migration steps? -->
