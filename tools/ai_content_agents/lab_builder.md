# Lab Builder Agent

## Purpose

The Lab Builder Agent creates the **vulnerable and patched application pairs** that form the hands-on core of each class. Students attack the vulnerable version and then study or deploy the patched version. This agent is the **third stage** in the content pipeline, consuming the class specification from the Curriculum Architect.

## Input Format

The agent requires:

1. **Class specification** — The `class-spec.yaml` produced by the Curriculum Architect Agent
2. **Technology constraints** — The approved technology stack from the class spec (typically Python + Flask/FastAPI + SQLite)
3. **Lab structure requirements** — The mandatory file layout (fixed, provided below)

### Lab Structure Requirements (always included)

```
labs/{class_id}/
├── README.md                  # Lab instructions for students
├── vulnerable/
│   ├── app.py                 # The vulnerable application
│   ├── requirements.txt       # Dependencies for the vulnerable app
│   └── (supporting files)     # Templates, static assets, seed data
├── patched/
│   ├── app.py                 # The patched application
│   ├── requirements.txt       # Dependencies for the patched app
│   └── (supporting files)     # Same as vulnerable, but updated if needed
├── attacks/
│   ├── attack.py              # Attack script (safe, constrained)
│   └── README.md              # Attack instructions with safety markers
├── tests/
│   ├── test_vulnerable.py     # Tests that verify the vulnerability exists
│   ├── test_patched.py        # Tests that verify the patch works
│   └── conftest.py            # Shared test fixtures
└── assurance/
    ├── control-ledger.yaml    # Mapping of controls to tests
    └── evidence-template.md   # Template for evidence collection
```

## Output Format

The agent must produce the following files:

### 1. `vulnerable/app.py`

A self-contained Python application that:
- Runs on `localhost` with a single command (`python app.py`)
- Contains exactly the vulnerability specified in the class spec
- Is a realistic, minimal application (not a toy "Hello World")
- Has enough functionality that the vulnerability is non-trivial but discoverable
- Includes inline comments marking the vulnerable code path with: `# VULNERABLE: {description}`
- Starts a server on a configurable port (default: 5000)
- Has a `/health` endpoint for test readiness checks

### 2. `patched/app.py`

The same application with:
- The vulnerability fixed
- Each fix annotated with: `# PATCH: {description of what changed and why}`
- No new vulnerabilities introduced by the fix
- Same API surface as the vulnerable version (tests must work against both)
- Performance overhead from the patch is acceptable (< 2x latency on affected endpoints)

### 3. `vulnerable/requirements.txt` and `patched/requirements.txt`

Pinned dependency versions:
```
flask==3.0.0
pytest==8.0.0
# ... etc
```

### 4. `README.md` (lab instructions)

```markdown
# Lab: {Class Title}

## Objective
<!-- What students will learn by completing this lab -->

## Prerequisites
<!-- What to install, what to know -->

## Setup
<!-- Step-by-step instructions to run the vulnerable app -->

## Tasks
### Task 1: Explore the Application
<!-- Instructions for getting familiar with the app -->

### Task 2: Find the Vulnerability
<!-- Hints for discovering the vulnerability -->

### Task 3: Exploit the Vulnerability
<!-- Instructions for running the attack -->

### Task 4: Study the Patch
<!-- Instructions for comparing vulnerable vs. patched code -->

### Task 5: Verify the Fix
<!-- Instructions for running the patched app and confirming the attack fails -->

## Cleanup
<!-- How to shut everything down -->

## Safety Notice
<!-- Mandatory safety disclaimer -->
```

### 5. Supporting files

Any templates, static assets, or seed data needed by the application.

## Constraints

1. **Self-contained.** The app must run with only `pip install -r requirements.txt && python app.py`. No external services, no Docker (unless the class spec explicitly requires it), no cloud resources.
2. **Single vulnerability.** The vulnerable app must contain exactly the one vulnerability specified in the class spec. Do not introduce additional vulnerabilities.
3. **Minimal but realistic.** The app should feel like a real (if small) application, not a contrived example. Include realistic data models, user flows, and error handling.
4. **Same API surface.** The vulnerable and patched versions must expose the same endpoints with the same signatures. Tests must work against both without modification.
5. **Inline annotations.** Vulnerable code must be marked with `# VULNERABLE:` comments. Patched code must be marked with `# PATCH:` comments.
6. **Health endpoint.** Both apps must expose `GET /health` returning `{"status": "ok"}` for test readiness.
7. **Pinned dependencies.** All `requirements.txt` files must use exact version pins (`==`). No ranges.
8. **No secrets.** Do not hardcode API keys, passwords, or tokens. Use environment variables or default development values clearly marked as insecure.
9. **Port configurable.** The server port must be configurable via an environment variable (default: 5000).
10. **Clean shutdown.** The app must shut down cleanly on SIGINT/SIGTERM.
11. **SQLite for databases.** Use SQLite as the default database. No external database servers.
12. **Seed data.** If the app needs data, include a seed script or seed data that auto-loads on first run.

## Prompt Skeleton

```
You are the Lab Builder Agent for the "AI Security from Scratch" curriculum.
Your job is to create a vulnerable/patched application pair for a specific class,
based on the class specification produced by the Curriculum Architect Agent.

LAB STRUCTURE REQUIREMENTS:
- Labs live in: labs/{class_id}/
- Required files: README.md, vulnerable/app.py, vulnerable/requirements.txt,
  patched/app.py, patched/requirements.txt, and any supporting files
- Vulnerable code marked with: # VULNERABLE: {description}
- Patched code marked with: # PATCH: {description}
- Both apps expose GET /health returning {"status": "ok"}
- Port configurable via PORT environment variable (default 5000)
- Dependencies pinned with == in requirements.txt

CLASS SPECIFICATION:
---
{paste class-spec.yaml here}
---

INSTRUCTIONS:
1. Read the class specification. Identify the vulnerability and the vulnerable system.
2. Design a minimal but realistic application that contains exactly this vulnerability.
3. Implement the vulnerable version (vulnerable/app.py) with # VULNERABLE: annotations.
4. Implement the patched version (patched/app.py) with # PATCH: annotations.
5. Ensure both versions have the same API surface.
6. Write the lab README.md with all required sections.
7. Write requirements.txt for both versions with pinned dependencies.
8. Create any supporting files (templates, seed data) needed.

CONSTRAINTS:
- Self-contained: runs with pip install && python app.py
- Single vulnerability only
- Minimal but realistic application
- Same API surface for both versions
- Inline annotations on vulnerable and patched code
- Health endpoint on both versions
- Pinned dependencies
- No hardcoded secrets
- Configurable port
- SQLite for database
- Clean shutdown on SIGINT/SIGTERM

OUTPUT:
Produce all files for the lab. Begin each file with a comment/header:
--- FILE: {relative path} ---
Followed by the file contents. Produce ALL files, not just the app.
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] Vulnerable app starts with `python app.py`
- [ ] Vulnerable app responds to `GET /health`
- [ ] Vulnerable app contains exactly the specified vulnerability
- [ ] All vulnerable code marked with `# VULNERABLE:` comments
- [ ] Patched app starts with `python app.py`
- [ ] Patched app responds to `GET /health`
- [ ] Patched app fixes the vulnerability without introducing new ones
- [ ] All patched code marked with `# PATCH:` comments
- [ ] Both apps have the same API surface
- [ ] Dependencies are pinned with `==`
- [ ] No hardcoded secrets
- [ ] Port is configurable via environment variable
- [ ] Lab README.md has all required sections
- [ ] Application uses SQLite (no external DB)
- [ ] Clean shutdown works
