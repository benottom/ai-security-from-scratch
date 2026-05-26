# Maintainer Agent

## Purpose

The Maintainer Agent keeps the curriculum content **up-to-date, internally consistent, and functional over time**. It performs regular maintenance tasks: checking for broken links, validating that code still runs against current dependencies, detecting drift between related artifacts, and flagging content that may be outdated due to new vulnerabilities, framework updates, or standard revisions. This agent is the **tenth and final stage** in the content pipeline, but it also operates **independently on a schedule** (e.g., monthly) to maintain existing content.

## Input Format

The agent requires:

1. **Scope** — What to maintain:
   - `--class=phase-N/class-MM` for a specific class
   - `--phase=N` for an entire phase
   - `--all` for the entire curriculum
2. **Repository root** — The path to the curriculum repository
3. **Maintenance checklist** — The standard maintenance tasks (fixed, provided below)

### Maintenance Checklist (always included)

**1. Link Integrity**
- All external URLs return HTTP 200 (or 301/302 to a 200)
- All internal links reference files that exist in the repo
- All `requirements.txt` package URLs are valid
- All standards references (CWE, OWASP, NIST) still resolve

**2. Dependency Freshness**
- All pinned dependencies in `requirements.txt` are still available on PyPI
- No dependencies with known critical vulnerabilities
- Python version compatibility is current (3.11+)
- Framework versions (Flask, FastAPI, etc.) are not end-of-life

**3. Code Runnability**
- `vulnerable/app.py` starts without errors
- `patched/app.py` starts without errors
- `attacks/attack.py` runs against the vulnerable app and exits 0
- `attacks/attack.py` runs against the patched app and exits 1
- All tests pass: `pytest tests/` returns 0

**4. Artifact Consistency**
- Class ID matches across all files in the class directory
- Vulnerability theme matches across lesson, lab, attack, and assurance
- CWE IDs match across class spec, lesson, and assurance report
- Control IDs in the ledger match those in defense.py
- Test function names in the ledger match actual test functions

**5. Content Currency**
- Real-world examples still have accessible references
- Standards references are still current (e.g., OWASP Top 10 2021 vs 2017)
- No deprecated API usage in application code
- No references to tools or services that no longer exist

**6. Structural Integrity**
- All required files are present in each class directory
- All required sections exist in each markdown file
- `conftest.py` fixtures reference correct app paths
- `README.md` instructions are still accurate

## Output Format

The agent must produce a **maintenance report** and, optionally, **maintenance pull requests**.

### 1. `maintenance-report-{date}.md`

```markdown
# Maintenance Report: {Scope}

**Date:** {YYYY-MM-DD}
**Scope:** {class ID, phase, or "full curriculum"}
**Maintainer:** Maintainer Agent
**Status:** {HEALTHY | NEEDS_ATTENTION | CRITICAL}

---

## Summary

{2–3 sentence overview of maintenance findings. How many classes checked,
how many issues found, overall health assessment.}

## 1. Link Integrity

### Broken External Links
| File | Link | HTTP Status | Recommendation |
|------|------|-------------|----------------|
| lesson.md | https://example.com/paper | 404 | Find alternative source or archive.org link |

### Broken Internal Links
| File | Link Target | Issue |
|------|-------------|-------|
| lesson.md | ../class-05/lesson.md | Target does not exist |

### Validated Links
- Total external links checked: {N}
- Total passing: {N}
- Total failing: {N}

## 2. Dependency Freshness

### Outdated Dependencies
| Class | File | Package | Current Pin | Latest Stable | Has CVE? |
|-------|------|---------|-------------|---------------|----------|
| phase-2/class-07 | vulnerable/requirements.txt | flask | 2.3.0 | 3.0.0 | No |

### Vulnerable Dependencies
| Class | File | Package | Pin | CVE | Severity |
|-------|------|---------|-----|-----|----------|
| (none found) | | | | | |

### PyPI Availability
- All packages available: ✅
- Missing packages: (list, if any)

## 3. Code Runnability

| Class | Vulnerable App | Patched App | Attack (vuln) | Attack (patched) | Tests |
|-------|---------------|-------------|---------------|-------------------|-------|
| phase-2/class-07 | ✅ Starts | ✅ Starts | ✅ Exit 0 | ✅ Exit 1 | ✅ Pass |
| phase-3/class-12 | ✅ Starts | ❌ ImportError | ⬜ Skipped | ⬜ Skipped | ❌ 2 failures |

### Failed Details
**phase-3/class-12 — patched/app.py:**
```
ImportError: cannot import name 'secure_compare' from 'hmac'
```
**Recommendation:** Update to use `hmac.compare_digest` (renamed in Python 3.11+).

## 4. Artifact Consistency

| Class | Class ID Match | Vuln Theme Match | CWE Match | Control ID Match | Test Name Match |
|-------|---------------|-----------------|-----------|-----------------|----------------|
| phase-2/class-07 | ✅ | ✅ | ✅ | ✅ | ✅ |
| phase-3/class-12 | ✅ | ⚠️ Mismatch | ✅ | ✅ | ❌ 2 missing |

### Consistency Details
**phase-3/class-12 — Vulnerability Theme Mismatch:**
- lesson.md: "Model Extraction"
- attacks/README.md: "Model Theft"
- Recommendation: Standardize to "Model Extraction" (matches class spec)

**phase-3/class-12 — Test Name Mismatch:**
- Control ledger references: `test_ctl2_detects_anomaly`
- Actual test function: `test_ctl2_anomaly_detection`
- Recommendation: Update ledger to match actual test name

## 5. Content Currency

### Outdated References
| Class | File | Reference | Issue |
|-------|------|-----------|-------|
| phase-1/class-03 | lesson.md | OWASP Top 10 2017 | Current version is 2021 |

### Deprecated API Usage
| Class | File | API | Deprecation | Replacement |
|-------|------|-----|-------------|-------------|
| (none found) | | | | |

### Stale Examples
| Class | File | Example | Issue |
|-------|------|---------|-------|
| (none found) | | | |

## 6. Structural Integrity

### Missing Files
| Class | Missing File | Severity |
|-------|-------------|----------|
| phase-3/class-12 | assurance/control-ledger.yaml | critical |

### Missing Sections
| Class | File | Missing Section |
|-------|------|----------------|
| phase-2/class-07 | lesson.md | (none — all sections present) |

## Action Items

### Critical (must fix immediately)
1. [ ] phase-3/class-12: Fix ImportError in patched/app.py
2. [ ] phase-3/class-12: Create missing assurance/control-ledger.yaml

### High Priority (fix within 1 week)
3. [ ] phase-3/class-12: Standardize vulnerability theme across files
4. [ ] phase-3/class-12: Update test name references in control ledger

### Medium Priority (fix within 1 month)
5. [ ] phase-1/class-03: Update OWASP Top 10 reference from 2017 to 2021

### Low Priority (next maintenance cycle)
6. [ ] phase-2/class-07: Update Flask from 2.3.0 to 3.0.0 in vulnerable app

## Recommended Pull Requests

1. **fix/class-12-patched-import** — Fix ImportError in patched/app.py
2. **fix/class-12-consistency** — Standardize vulnerability theme and update ledger
3. **update/owasp-top10-2021** — Update OWASP references across Phase 1

---

_Report generated by Maintainer Agent on {ISO 8601 timestamp}_
```

## Constraints

1. **Non-destructive.** The maintainer never directly modifies files. It creates reports and recommends PRs. A human must approve all changes.
2. **Network-aware.** External link checks should be rate-limited (1 request per second) and have timeouts (10 seconds per request).
3. **Reproducible.** Running the maintainer twice on the same content should produce the same results.
4. **Incremental.** The maintainer should support checking a single class without checking the entire curriculum.
5. **Severity classification.** Issues must be classified as critical, high, medium, or low priority.
6. **Actionable recommendations.** Every issue must have a specific recommendation, not just "fix this."
7. **No false positives on flaky links.** If an external URL fails once, retry up to 3 times before reporting it as broken.
8. **Respect `.gitignore`.** Do not check files or paths that are gitignored.
9. **No network access for code runnability checks by default.** The maintainer should attempt to start apps locally but must not make outbound network connections. Use `--offline` flag to skip external checks.
10. **Timestamped reports.** All reports must include an ISO 8601 generation timestamp.

## Prompt Skeleton

```
You are the Maintainer Agent for the "AI Security from Scratch" curriculum.
Your job is to keep content up-to-date, consistent, and functional. You perform
regular maintenance checks and produce reports with actionable recommendations.
You do NOT directly modify files — you recommend changes for human approval.

MAINTENANCE CHECKLIST:
1. Link Integrity — check all external and internal links
2. Dependency Freshness — check pinned deps, CVEs, PyPI availability
3. Code Runnability — verify apps start, attacks work, tests pass
4. Artifact Consistency — cross-file ID/theme/CWE/control matching
5. Content Currency — outdated references, deprecated APIs, stale examples
6. Structural Integrity — required files and sections present

SCOPE: {--class=phase-N/class-MM | --phase=N | --all}
REPOSITORY ROOT: {path}

INSTRUCTIONS:
1. Scan the specified scope for all class directories.
2. For each class, perform all six maintenance checks.
3. Classify every issue by severity (critical/high/medium/low).
4. Provide specific, actionable recommendations.
5. Suggest concrete PRs where appropriate.
6. Produce the complete maintenance report.

CONSTRAINTS:
- Non-destructive: report only, no direct modifications
- Rate-limit external requests: 1/sec, 10s timeout
- Reproducible: same input → same output
- Severity classification on all issues
- Actionable recommendations on all issues
- Retry failed URLs up to 3 times
- Respect .gitignore
- No outbound network for code checks by default
- ISO 8601 timestamp on report

OUTPUT:
Produce the maintenance report as Markdown following the required format.
Output ONLY the Markdown report.
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] All six maintenance dimensions are covered
- [ ] Every issue has a severity classification
- [ ] Every issue has an actionable recommendation
- [ ] Report is scoped correctly (not checking unrelated classes)
- [ ] External link checks were performed (or explicitly noted as skipped)
- [ ] Dependency versions were checked against PyPI
- [ ] Code runnability was tested (or explicitly noted as skipped)
- [ ] Cross-file consistency was verified
- [ ] No direct file modifications were made
- [ ] ISO 8601 timestamp is present
- [ ] Action items are prioritized correctly
- [ ] Recommended PRs are concrete and actionable
