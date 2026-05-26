# Contributing to AI Security from Scratch

Thank you for your interest in contributing. This document describes how to contribute, the quality standards we enforce, and the workflows we follow.

---

## How to Contribute

There are four ways to contribute:

1. **Issues** — Report bugs, suggest improvements, or request new content. Open an issue using the appropriate template.
2. **Pull Requests** — Submit code, content, or fixes. Follow the PR template and quality gates described below.
3. **Discussions** — Propose ideas, ask questions, or debate approaches before committing to a PR.
4. **Reviews** — Review open PRs. Good reviews are as valuable as good code.

### One Contribution per PR

Every pull request must address exactly one concern. A PR that fixes a typo and adds a new attack class will be rejected. This rule exists because:

- It makes reviews faster and more focused.
- It keeps the git history clean and bisectable.
- It reduces the risk of a good change being blocked by an unrelated problem.

If you have multiple changes, open multiple PRs.

---

## Content Quality Gates

All contributions must pass five quality gates before merging:

### 1. Content Gate
- The contribution teaches something that is not already covered.
- The content is accurate and technically sound.
- Claims are supported by references or reproducible evidence.
- The writing is direct, clear, and free of jargon that is not defined.

### 2. Code Gate
- All code runs without errors in the lab environment.
- All code passes `make lint` with zero warnings.
- All code passes `make test` with zero failures.
- All code includes type hints and docstrings.
- Dependencies are declared in `requirements.txt`.

### 3. Security Gate
- Attack code is clearly labeled and confined to lab environments.
- No attack code targets external or production systems.
- Defenses are tested against the attacks they claim to stop.
- Unsafe code patterns (e.g., `eval`, unpickled objects) are used only in deliberately vulnerable lab systems and are clearly marked.
- No credentials, API keys, or secrets are included in any file.

### 4. Assurance Gate
- Every defense includes a test that demonstrates it stops the attack it addresses.
- Every control includes monitoring instrumentation.
- Every security claim is supported by evidence (test output, metric, or structured argument).
- Untested defenses are explicitly marked as unverified and do not merge.

### 5. Editorial Gate
- Prose is direct and concrete. No filler phrases ("It is important to note that...", "In today's rapidly evolving landscape...").
- No decorative emojis in headings or body text. Use emojis only in status markers (roadmap, CI badges) where convention demands.
- Code comments explain *why*, not *what*. The code explains what.
- Headings are descriptive, not clever.
- Consistent terminology throughout. Use the glossary.

---

## Style Rules

### Prose
- Write in direct, declarative sentences. Prefer "The controller blocks the request" over "The request is blocked by the controller."
- Avoid passive voice unless the agent is genuinely unknown or irrelevant.
- Do not hedge needlessly. "This defense stops the attack" is better than "This defense may help mitigate the attack in some cases."
- Use concrete examples instead of abstract descriptions wherever possible.
- No AI-generated filler. If a sentence can be removed without losing information, remove it.

### Code
- Python 3.10+ with type hints on all function signatures.
- Use `pytest` for all tests. No `unittest` or `doctest`.
- Every public function and class has a docstring.
- Docstrings follow Google style: `Args:`, `Returns:`, `Raises:`.
- Maximum line length: 100 characters.
- Use `ruff` for formatting and linting. Configuration is in `pyproject.toml`.
- Prefer standard library when possible. Avoid adding dependencies.

### Security Content
- Frame all attack content in defensive terms. "This attack exploits X to achieve Y. Here is how to detect it. Here is how to prevent it."
- Never provide attack tools intended for use against systems the learner does not own.
- Every attack section must include the corresponding defense section in the same class.
- Never include zero-day exploits for live, unpatched vulnerabilities.
- All attack demonstrations must use the project's intentionally vulnerable lab systems.

---

## Class Generation Workflow

New classes follow a 13-step human validation flow. No class merges without completing every step.

1. **Proposal** — Open a discussion describing the class topic, learning objectives, and which phase it belongs to.
2. **Approval** — A maintainer approves the proposal and assigns a class number.
3. **Outline** — Submit a detailed outline as a PR against the `draft` branch. Include all sections, attack descriptions, defense strategies, and lab exercises.
4. **Outline review** — At least one maintainer reviews the outline for completeness and accuracy.
5. **Content draft** — Write the full class content following the Build → Attack → Analyze → Defend → Test → Monitor → Assure structure.
6. **Code draft** — Implement all code for the class: vulnerable system, attacks, defenses, tests, and monitoring.
7. **Self-test** — Run `make check` locally. Fix all failures before requesting review.
8. **Peer review** — At least one maintainer and one community reviewer must approve the content.
9. **Security review** — A maintainer reviews all attack content for responsible disclosure compliance and lab safety.
10. **Assurance review** — A maintainer verifies that every defense has a passing test and every control has monitoring.
11. **Editorial review** — A maintainer checks prose quality, style compliance, and consistency with existing content.
12. **Integration test** — Run `make ci` to simulate the full CI pipeline. All checks must pass.
13. **Merge** — A maintainer merges the PR. The class is marked as complete in the roadmap.

Steps 1–4 ensure we build the right thing. Steps 5–7 ensure we build it correctly. Steps 8–11 ensure it meets our quality standards. Steps 12–13 ensure it integrates cleanly.

---

## Code Style Requirements

### Python
- **Version**: 3.10+
- **Type hints**: Required on all function signatures. Use `from __future__ import annotations` for forward references.
- **Docstrings**: Required on all public functions, classes, and modules. Google style.
- **Imports**: Standard library, then third-party, then local. Each group separated by a blank line. Use `isort` ordering.
- **Naming**: `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- **Error handling**: Use specific exceptions. Never catch bare `Exception` unless re-raising.
- **Testing**: `pytest` with descriptive test names. Use `test_<feature>_<scenario>_<expected_result>` naming convention.
- **Linting**: `ruff` with project configuration. Zero warnings required.

### Example

```python
from __future__ import annotations

from typing import Optional


def validate_input(user_input: str, max_length: int = 4096) -> Optional[str]:
    """Validate user input for injection markers.

    Args:
        user_input: The raw user input string to validate.
        max_length: Maximum allowed input length in characters.

    Returns:
        The validated input string, or None if validation fails.

    Raises:
        ValueError: If max_length is negative.
    """
    if max_length < 0:
        raise ValueError(f"max_length must be non-negative, got {max_length}")

    if len(user_input) > max_length:
        return None

    # Check for known injection patterns
    injection_markers = ["ignore previous", "system:", "### instruction"]
    normalized = user_input.lower()
    for marker in injection_markers:
        if marker in normalized:
            return None

    return user_input
```

---

## Safety Requirements for Attack Content

All attack content must comply with these requirements:

1. **Scope limitation** — Attacks target only the project's intentionally vulnerable lab systems. Never provide instructions for attacking specific third-party products or services.
2. **Defensive framing** — Every attack is presented as a means to understand and prevent the vulnerability, not as an enabling tool for malicious use.
3. **No weaponization** — Do not provide turnkey exploit tools. Code demonstrates the vulnerability; it is not packaged as an attack tool.
4. **Disclosure check** — Before including any vulnerability, verify it is publicly known and the vendor has had reasonable time to patch. Do not include zero-day exploits.
5. **Lab isolation** — All attack code must include a check that it is running in the lab environment, not against production systems.
6. **Responsible context** — Include a note at the start of every attack section: "This content is for defensive education. Do not use these techniques against systems you do not own or have authorization to test."

---

## PR Template

```markdown
## Description

[What does this PR change and why?]

## Type of Change

- [ ] Bug fix
- [ ] New class content
- [ ] New code (attack/defense/lab)
- [ ] Documentation improvement
- [ ] Infrastructure/tooling

## Quality Gates

- [ ] Content: Accurate, original, well-referenced
- [ ] Code: Runs, passes lint, passes tests, has type hints and docstrings
- [ ] Security: Attack content properly scoped and defensively framed
- [ ] Assurance: Defenses tested, controls monitored, claims evidenced
- [ ] Editorial: Direct prose, no filler, consistent terminology

## Testing

[Describe how you tested this change. Include command output if applicable.]

## Checklist

- [ ] I have read CONTRIBUTING.md
- [ ] This PR addresses exactly one concern
- [ ] All new code passes `make check`
- [ ] Attack content is defensively framed and lab-only
- [ ] No credentials, API keys, or secrets included
```

---

## Review Checklist

Reviewers should verify:

- [ ] The PR addresses exactly one concern.
- [ ] The content is accurate and technically sound.
- [ ] All code runs, passes lint, and passes tests.
- [ ] Attack content is properly scoped to lab environments.
- [ ] Every defense has a corresponding test.
- [ ] Every control includes monitoring instrumentation.
- [ ] Prose is direct and free of filler.
- [ ] No decorative emojis in headings or body text.
- [ ] No credentials, API keys, or secrets are present.
- [ ] Type hints and docstrings are present on all public code.
- [ ] Dependencies are declared in `requirements.txt`.
- [ ] The change is consistent with existing content and terminology.

---

Thank you for contributing. Every class, every review, every fix makes this curriculum better for everyone who wants to learn AI security the right way: by building, breaking, and proving.
