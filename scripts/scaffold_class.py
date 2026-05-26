#!/usr/bin/env python3
"""Scaffold a new class directory with all required files.

Usage:
    python scripts/scaffold_class.py <phase-number> <class-number> <class-name>

Example:
    python scripts/scaffold_class.py 3 15 document-poisoning

This creates:
    phases/phase-03-rag-security/class-15-document-poisoning/
        README.md
        lesson.md
        notebook.ipynb
        control-loop-analysis.md
        threat-model.md
        lab.md
        assignment.md
        vulnerable_app/.gitkeep
        attacks/.gitkeep
        patched_app/.gitkeep
        tests/.gitkeep
        observability/.gitkeep
        assurance/.gitkeep
        solutions/.gitkeep
"""

import sys
import os
from pathlib import Path

PHASE_MAP = {
    1: "phase-01-foundations",
    2: "phase-02-prompt-injection",
    3: "phase-03-rag-security",
    4: "phase-04-agent-and-tool-security",
    5: "phase-05-memory-and-feedback-security",
    6: "phase-06-data-and-privacy-security",
    7: "phase-07-model-and-supply-chain-security",
    8: "phase-08-defensive-controls",
    9: "phase-09-ai-security-testing",
    10: "phase-10-observability-and-incident-response",
    11: "phase-11-governance-and-assurance",
    12: "phase-12-capstone",
}

SUBDIRS = [
    "vulnerable_app",
    "attacks",
    "patched_app",
    "tests",
    "observability",
    "assurance",
    "solutions",
]

README_TEMPLATE = """# Class {class_num:02d} - {class_title}

## Learning Objectives

By the end of this class, you will be able to:

- [Objective 1]
- [Objective 2]
- [Objective 3]
- [Objective 4]

## Control-Theoretic View

| Element | Description |
|---------|-------------|
| **Objective** | [What security property must the system maintain?] |
| **Controller** | [What component decides how to act?] |
| **Observations** | [What signals can the controller see?] |
| **Actions** | [What can the controller do?] |
| **Feedback** | [How does the controller know if actions worked?] |
| **Disturbances** | [What adversarial inputs disrupt the loop?] |
| **Unsafe states** | [What conditions violate the objective?] |
| **Supervisory controls** | [What higher-level controls monitor the controller?] |
| **Monitoring** | [How is control effectiveness observed?] |
| **Recovery** | [How is safe operation restored after failure?] |

## Lab Summary

You will build a vulnerable system, exploit it safely, patch it, and prove the fix with tests.

## Deliverables

- [ ] Working vulnerable app
- [ ] Attack transcript
- [ ] Patched implementation
- [ ] Passing security tests
- [ ] Short assurance note

## Estimated Time

90-180 minutes

## Prerequisites

- [List prerequisite classes]

## References

- [Add relevant references]
"""

LESSON_TEMPLATE = """# Class {class_num:02d} - {class_title}

## Overview

[2-3 paragraphs: What is this class about? Why does it matter?]

## Why This Matters

[2-3 paragraphs: Concrete motivation. What goes wrong in real systems? What is the impact?]

## Control-Theoretic Interpretation

[2-3 paragraphs: How does this topic map to the control-loop framework?]

```mermaid
graph TD
    OBJ[Objective] --> CTRL[Controller]
    OBS[Observations] --> CTRL
    CTRL --> ACT[Actions]
    ACT --> ENV[Environment]
    ENV --> OBS
    ENV -->|Disturbances| OBS
    FB[Feedback] --> CTRL
    SUP[Supervisory Controls] --> CTRL
    MON[Monitoring] --> SUP
```

## Security Failure Mode

[2-3 paragraphs: What specific control failure occurs? How does the attack exploit it?]

## Defensive Design

[2-3 paragraphs: What supervisory control addresses this? Why does it work?]

## What You Will Build

[2-3 paragraphs: Description of the vulnerable and patched applications]

## Common Mistakes

1. [Mistake 1 and why it happens]
2. [Mistake 2 and why it happens]
3. [Mistake 3 and why it happens]

## Key Takeaways

- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

## Responsible Use Warning

The attacks in this class are for educational purposes only. They must only be used against the local lab systems provided. Never use these techniques against systems you do not own or have explicit authorization to test.
"""

CONTROL_LOOP_TEMPLATE = """# Control-Loop Analysis — Class {class_num:02d}: {class_title}

## System Under Analysis

**System:** [Name of the AI system]
**Phase:** {phase_num}
**Class:** {class_num:02d}

## Control-Loop Decomposition

### Objective
[What security property must the system maintain?]

### Controller
[What component(s) make decisions?]

### Observations
- [Observation 1]
- [Observation 2]
- [Observation 3]

### Actions
- [Action 1]
- [Action 2]
- [Action 3]

### Environment
[What is the system's operating context?]

### Feedback
[How does the system learn about the effect of its actions?]

### Disturbances
- [Disturbance 1]
- [Disturbance 2]
- [Disturbance 3]

### Unsafe States
- [Unsafe state 1]
- [Unsafe state 2]
- [Unsafe state 3]

### Supervisory Controls
- [Control 1]
- [Control 2]
- [Control 3]

### Monitoring
[What should be observed to detect control degradation?]

### Recovery
[How is safe operation restored after a failure?]

## Mermaid Diagram

```mermaid
graph TD
    OBJ[Objective: ...] --> CTRL[Controller: ...]
    OBS[Observations] --> CTRL
    CTRL --> ACT[Actions]
    ACT --> ENV[Environment]
    ENV --> OBS
    ENV -->|Disturbances| OBS
    ENV -->|Unsafe states| FB[Feedback]
    FB --> CTRL
    CTRL --> SUP[Supervisory Controls]
    SUP --> CTRL
    MON[Monitoring] --> SUP
    ENV -->|Failure| REC[Recovery]
    REC --> ENV
```

## Analysis Summary

[Summarize the key insight from this control-loop decomposition.]
"""

THREAT_MODEL_TEMPLATE = """# Threat Model — Class {class_num:02d}: {class_title}

## System Description

[Brief description of the system being threat-modeled]

## Trust Boundaries

```mermaid
graph TB
    subgraph Trusted
        SYS[System Prompt]
        CTRL[Controller]
    end
    subgraph Untrusted
        USR[User Input]
        EXT[External Data]
    end
    USR --> CTRL
    EXT --> CTRL
    CTRL --> OUT[Output]
```

## STRIDE-AI Analysis

| ID | Threat | Category | Component | Impact | Likelihood | Risk |
|----|--------|----------|-----------|--------|------------|------|
| T01 | [Threat] | Spoofing | [Component] | High | Medium | High |
| T02 | [Threat] | Tampering | [Component] | High | Medium | High |
| T03 | [Threat] | Repudiation | [Component] | Low | Low | Low |
| T04 | [Threat] | Info Disclosure | [Component] | High | High | Critical |
| T05 | [Threat] | Denial of Service | [Component] | Medium | Medium | Medium |
| T06 | [Threat] | Elevation of Privilege | [Component] | High | Medium | High |

## Unsafe States

1. [Unsafe state 1]
2. [Unsafe state 2]
3. [Unsafe state 3]

## Existing Controls

| Control | Threats Mitigated | Effectiveness |
|---------|-------------------|---------------|
| [Control 1] | T01, T02 | Partial |

## Residual Risks

1. [Residual risk 1]
2. [Residual risk 2]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
"""

LAB_TEMPLATE = """# Lab — Class {class_num:02d}: {class_title}

## Lab Overview

[1-2 paragraphs: What will the learner build, attack, and defend?]

## Pre-Lab Setup

```bash
cd phases/phase-{phase_num:02d}-*/class-{class_num:02d}-*
make setup
```

## Lab Steps

### Step 1: Start the Vulnerable Application

```bash
make run-vulnerable
```

[What should the learner see?]

### Step 2: Run Normal Behavior Test

```bash
make test-normal
```

[What normal behavior looks like]

### Step 3: Execute the Attack

```bash
make attack
```

[What happens when the attack succeeds]

### Step 4: Observe the Failure

[Describe the control-loop failure. What unsafe state is reached?]

### Step 5: Explain the Control-Loop Failure

[Map the failure to the control-loop framework. Which element failed? Why?]

### Step 6: Implement the Defense

[Guidance for patching the vulnerable app]

### Step 7: Run Security Regression Test

```bash
make test-security
```

[What passing tests look like]

### Step 8: Generate Evidence Report

```bash
make evidence
```

[What the evidence report contains]

## Cleanup

```bash
make clean
```
"""

ASSIGNMENT_TEMPLATE = """# Assignment — Class {class_num:02d}: {class_title}

## Exercise 1 — Easy

**Task:** [Description]

**Deliverable:** [What to submit]

---

## Exercise 2 — Medium

**Task:** [Description]

**Deliverable:** [What to submit]

---

## Exercise 3 — Hard

**Task:** [Description]

**Deliverable:** [What to submit]

---

## Submission

Place your solutions in the `solutions/` directory.
"""


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    phase_num = int(sys.argv[1])
    class_num = int(sys.argv[2])
    class_name = sys.argv[3]

    if phase_num not in PHASE_MAP:
        print(f"Error: Phase must be 1-12. Got: {phase_num}")
        sys.exit(1)

    if class_num < 1 or class_num > 76:
        print(f"Error: Class number must be 1-76. Got: {class_num}")
        sys.exit(1)

    phase_dir = PHASE_MAP[phase_num]
    class_dir_name = f"class-{class_num:02d}-{class_name}"
    class_title = class_name.replace("-", " ").title()

    repo_root = Path(__file__).parent.parent
    class_path = repo_root / "phases" / phase_dir / class_dir_name

    if class_path.exists():
        print(f"Error: Directory already exists: {class_path}")
        sys.exit(1)

    # Create class directory
    class_path.mkdir(parents=True)

    # Create subdirectories with .gitkeep
    for subdir in SUBDIRS:
        (class_path / subdir).mkdir()
        (class_path / subdir / ".gitkeep").touch()

    # Create notebook.ipynb
    notebook_content = generate_notebook(phase_num, class_num, class_title)
    (class_path / "notebook.ipynb").write_text(notebook_content, encoding="utf-8")

    # Create template files
    templates = {
        "README.md": README_TEMPLATE,
        "lesson.md": LESSON_TEMPLATE,
        "control-loop-analysis.md": CONTROL_LOOP_TEMPLATE,
        "threat-model.md": THREAT_MODEL_TEMPLATE,
        "lab.md": LAB_TEMPLATE,
        "assignment.md": ASSIGNMENT_TEMPLATE,
    }

    for filename, template in templates.items():
        content = template.format(
            phase_num=phase_num,
            class_num=class_num,
            class_name=class_name,
            class_title=class_title,
        )
        (class_path / filename).write_text(content, encoding="utf-8")

    print(f"Created: {class_path}")
    print(f"  Phase {phase_num}: {phase_dir}")
    print(f"  Class {class_num:02d}: {class_title}")
    print()
    print("Next steps:")
    print(f"  1. Edit the lesson content in {class_path / 'lesson.md'}")
    print(f"  2. Build the vulnerable app in {class_path / 'vulnerable_app/'}")
    print(f"  3. Create the attack in {class_path / 'attacks/'}")
    print(f"  4. Build the patched app in {class_path / 'patched_app/'}")
    print(f"  5. Write tests in {class_path / 'tests/'}")
    print(f"  6. Add observability events in {class_path / 'observability/'}")
    print(f"  7. Create assurance evidence in {class_path / 'assurance/'}")
    print()
    print("Follow the class generation workflow in CONTRIBUTING.md")


def generate_notebook(phase_num: int, class_num: int, class_title: str) -> str:
    """Generate a Jupyter Notebook template for the class."""
    import json

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# Class {class_num:02d}: {class_title}\n",
                    "\n",
                    "> **Think. Play. Do.** This notebook is the *Play* part.\n",
                    "> Run every cell. Modify the code. Break things on purpose.\n",
                    "\n",
                    "## What You'll Learn\n",
                    "\n",
                    "1. [Learning objective 1]\n",
                    "2. [Learning objective 2]\n",
                    "3. [Learning objective 3]\n",
                    "\n",
                    "---"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Concept Check 1\n",
                    "\n",
                    "[Quick question to verify understanding before moving on]\n",
                    "\n",
                    "---"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Setup — import libraries\n",
                    "import matplotlib.pyplot as plt\n",
                    "import pandas as pd\n",
                    "import re\n",
                    "from typing import Optional\n",
                    "\n",
                    "print('Notebook ready. Let\\'s break things.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Part 1: Build the Vulnerable System\n",
                    "\n",
                    "[Build the intentionally vulnerable AI system for this class]"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Build the vulnerable system here\n",
                    "# TODO: Replace with actual vulnerable system code\n",
                    "print('Vulnerable system initialized.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Part 2: Attack the System\n",
                    "\n",
                    "[Execute attacks that exploit the control-loop gap]"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Attack 1\n",
                    "print('Running attack 1...')\n",
                    "# TODO: Implement attack"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## ✏️ YOUR TURN\n",
                    "\n",
                    "Modify the cell below to craft your own attack. Can you bypass the system?"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# YOUR ATTACK HERE\n",
                    "your_attack = 'TODO: Write your attack'\n",
                    "print(f'Your attack: {your_attack}')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Part 3: Analyze the Control-Loop Failure\n",
                    "\n",
                    "[Map each successful attack to a specific control-loop element]"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Build failure analysis with pandas\n",
                    "failure_analysis = pd.DataFrame({\n",
                    "    'Control-Loop Element': ['TODO'],\n",
                    "    'Status': ['TODO'],\n",
                    "    'What Should Exist': ['TODO'],\n",
                    "})\n",
                    "print(failure_analysis.to_string(index=False))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Part 4: Add a Supervisory Control\n",
                    "\n",
                    "[Implement the defense that closes the control loop]"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Implement supervisory control here\n",
                    "class SupervisoryControl:\n",
                    "    '''External, deterministic, auditable control.'''\n",
                    "    pass\n",
                    "\n",
                    "print('Supervisory control implemented.')"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Key Takeaways\n",
                    "\n",
                    "| # | Takeaway | Why It Matters |\n",
                    "|---|---|---|\n",
                    "| 1 | [Takeaway] | [Reason] |\n",
                    "| 2 | [Takeaway] | [Reason] |\n",
                    "| 3 | [Takeaway] | [Reason] |\n",
                    "\n",
                    "---\n",
                    f"\n",
                    f"*Class {class_num:02d} | AI Security from Scratch | Phase {phase_num}*\n",
                    "*Think. Play. Do.*"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    return json.dumps(notebook, indent=1)


if __name__ == "__main__":
    main()
