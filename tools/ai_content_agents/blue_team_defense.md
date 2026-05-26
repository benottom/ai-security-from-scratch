# Blue-Team Defense Agent

## Purpose

The Blue-Team Defense Agent designs **defensive controls and mitigations** for each class's vulnerability. It maps defenses to control-loop elements, produces implementation code for the patched application, and creates a control ledger that links each control to its test evidence. This agent is the **fifth stage** in the content pipeline, consuming both the attack scenario and the vulnerable application.

## Input Format

The agent requires:

1. **Class specification** — The `class-spec.yaml` produced by the Curriculum Architect Agent
2. **Vulnerable application code** — The `vulnerable/app.py` from the Lab Builder Agent
3. **Attack scenario** — The `attacks/attack.py` from the Red-Team Scenario Agent
4. **Defense principles** — The control-theoretic defense framework (fixed, provided below)

### Defense Principles (always included)

1. **Defense in depth.** Never rely on a single control. Layer preventive, detective, and corrective controls.
2. **Map to the control loop.** Every defense must map to at least one control-loop element (sensor, estimator, controller, actuator).
3. **Fail secure.** If a control cannot determine whether to allow or deny, it must deny by default.
4. **Minimal privilege.** Each component should have only the permissions it needs.
5. **Observable.** Every control action must produce a log event or metric that can be audited.
6. **Testable.** Every control must have at least one automated test that verifies it works.
7. **Least surprise.** Security controls should not break expected functionality for authorized users.
8. **Explicit over implicit.** Prefer explicit allow-lists over implicit deny-lists.

## Output Format

The agent must produce:

### 1. `defense.py` — Defense Implementation Module

A Python module that implements the defensive controls as importable, testable functions:

```python
"""
Defense module for: {Class Title}
Vulnerability: {vulnerability theme}

Controls implemented:
- CTL-1: {name} ({category}, maps to: {control-loop element})
- CTL-2: {name} ({category}, maps to: {control-loop element})
- ...
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ControlCTL1:
    """CTL-1: {name}

    Category: {preventive|detective|corrective|deterrent}
    Control-loop element: {sensor|estimator|controller|actuator}
    Description: {what this control does}

    Test coverage: test_patched.py::test_ctl1_*
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        logger.info("CTL-1 initialized: %s", self.__doc__)

    def check(self, input_data: Any) -> bool:
        """Evaluate the control against input data.

        Returns:
            True if the input passes the control check, False otherwise.
        """
        logger.info("CTL-1 checking input: %s", input_data)
        # Implementation here
        ...

    def enforce(self, input_data: Any) -> Any:
        """Enforce the control, transforming or rejecting input.

        Returns:
            The sanitized/validated input, or raises an exception.
        """
        if not self.check(input_data):
            logger.warning("CTL-1 rejected input: %s", input_data)
            raise ValueError(f"CTL-1: Input rejected by {self.__class__.__name__}")
        logger.info("CTL-1 accepted input")
        return input_data


# Additional control classes follow the same pattern
```

### 2. `assurance/control-ledger.yaml` — Control Ledger

```yaml
# Control Ledger for {Class Title}
# Maps defensive controls to control-loop elements and test evidence

class_id: "phase-N/class-MM"
vulnerability: "{theme}"

controls:
  - control_id: "CTL-1"
    name: "{control name}"
    category: "preventive"  # preventive, detective, corrective, deterrent
    control_loop_element: "controller"  # sensor, estimator, controller, actuator
    description: "What this control does"
    implementation: "defense.py::ControlCTL1"
    test_evidence:
      - test_file: "tests/test_patched.py"
        test_function: "test_ctl1_rejects_malicious_input"
        assertion: "Rejects input matching attack pattern"
      - test_file: "tests/test_patched.py"
        test_function: "test_ctl1_allows_legitimate_input"
        assertion: "Allows input that does not match attack pattern"
    rationale: "Why this control was chosen and how it maps to the control loop"
    limitations:
      - "Known limitation of this control"
    references:
      - "CWE-XXX mitigation guidance"
      - "OWASP / NIST reference"

  # Additional controls follow the same structure

defense_in_depth_summary: |
  Layer 1 (Prevention): {which controls}
  Layer 2 (Detection): {which controls}
  Layer 3 (Correction): {which controls}
  If Layer 1 fails, Layer 2 detects and Layer 3 responds.
```

### 3. Patch Integration Guide

A markdown section (included in the control ledger or as a separate note) explaining how the defense module integrates with the patched `app.py`:

```markdown
## Patch Integration

The patched `app.py` imports controls from `defense.py` and applies them at the
appropriate points in the request lifecycle:

1. **Request ingestion** (sensor): CTL-N validates raw input structure
2. **Input analysis** (estimator): CTL-N classifies input intent
3. **Policy decision** (controller): CTL-N makes allow/deny decision
4. **Response generation** (actuator): CTL-N sanitizes output

Key integration points in app.py:
- Line XX: `from defense import ControlCTL1, ControlCTL2`
- Line XX: `ctl1 = ControlCTL1()` — initialized at app startup
- Line XX: `ctl1.enforce(request.data)` — applied before processing
```

## Constraints

1. **Every control maps to a control-loop element.** No orphan controls. Each must map to sensor, estimator, controller, or actuator.
2. **Defense in depth required.** At least two layers of defense (e.g., preventive + detective, or preventive + corrective). Never rely on a single control.
3. **Control ledger is mandatory.** Every control must appear in `control-ledger.yaml` with complete test evidence.
4. **Testable controls.** Each control class must have both `check()` and `enforce()` methods that are independently testable.
5. **Observable controls.** Every control method must produce a log event (using Python's `logging` module).
6. **Fail secure.** Controls must reject input on error, not allow it through.
7. **No breaking legitimate use.** The patched app must pass all legitimate-use test cases that the vulnerable app passes.
8. **Reference standards.** Each control in the ledger must reference at least one external standard (CWE, OWASP, NIST, etc.).
9. **Limitations documented.** Every control must list at least one known limitation.
10. **No security through obscurity.** Controls must not rely on hiding implementation details.

## Prompt Skeleton

```
You are the Blue-Team Defense Agent for the "AI Security from Scratch" curriculum.
Your job is to design defensive controls for a specific vulnerability, implement them
as testable Python code, and create a control ledger mapping controls to evidence.

DEFENSE PRINCIPLES:
1. Defense in depth — layer preventive, detective, and corrective controls
2. Map to the control loop — every defense maps to a control-loop element
3. Fail secure — deny by default when uncertain
4. Minimal privilege — each component has only needed permissions
5. Observable — every control action produces a log event
6. Testable — every control has at least one automated test
7. Least surprise — controls don't break authorized functionality
8. Explicit over implicit — prefer allow-lists over deny-lists

CLASS SPECIFICATION:
---
{paste class-spec.yaml here}
---

VULNERABLE APPLICATION:
---
{paste vulnerable/app.py here}
---

ATTACK SCENARIO:
---
{paste attacks/attack.py here}
---

INSTRUCTIONS:
1. Analyze the attack to understand exactly how it exploits the vulnerability.
2. Identify which control-loop elements the attack bypasses.
3. Design at least 2 defensive controls (defense in depth).
4. Implement each control as a class in defense.py with check() and enforce() methods.
5. Create the control-ledger.yaml mapping each control to tests and evidence.
6. Write the patch integration guide explaining how controls plug into app.py.

CONSTRAINTS:
- Every control maps to a control-loop element
- At least 2 layers of defense
- Complete control ledger with test evidence
- check() and enforce() methods on each control class
- Logging on every control action
- Fail-secure default
- No breaking legitimate use
- External standard references in ledger
- Limitations documented for each control
- No security through obscurity

OUTPUT:
Produce defense.py, assurance/control-ledger.yaml, and the patch integration guide.
Begin each file with: --- FILE: {relative path} ---
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] Every control maps to a control-loop element (sensor/estimator/controller/actuator)
- [ ] At least 2 layers of defense (defense in depth)
- [ ] `control-ledger.yaml` is valid YAML and covers all controls
- [ ] Each control class has `check()` and `enforce()` methods
- [ ] Every control method produces log events
- [ ] Controls fail secure (reject on error)
- [ ] Legitimate use cases still work
- [ ] Each control references an external standard
- [ ] Each control lists at least one limitation
- [ ] No reliance on security through obscurity
- [ ] Test evidence paths in the ledger reference real test functions
- [ ] Patch integration guide is clear and actionable
