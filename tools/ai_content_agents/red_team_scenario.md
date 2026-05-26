# Red-Team Scenario Agent

## Purpose

The Red-Team Scenario Agent creates **safe, constrained attack scripts** that demonstrate the vulnerability in each class's lab application. These attacks are educational tools, not weaponized exploits. They must be deterministic, scoped to the lab sandbox, and thoroughly documented. This agent is the **fourth stage** in the content pipeline, consuming the vulnerable application produced by the Lab Builder Agent.

## Input Format

The agent requires:

1. **Class specification** — The `class-spec.yaml` produced by the Curriculum Architect Agent
2. **Vulnerable application code** — The `vulnerable/app.py` from the Lab Builder Agent
3. **Attack safety rules** — Hard constraints on what attacks may and may not do (fixed, provided below)

### Attack Safety Rules (always included)

1. **Localhost only.** All network requests must target `localhost` or `127.0.0.1`. The attack script must refuse to run if the target is not localhost.
2. **No data exfiltration.** The attack may demonstrate data access but must not transmit data outside the lab environment.
3. **No persistence.** The attack must not install backdoors, modify system files, or create persistent access mechanisms.
4. **No privilege escalation beyond lab.** The attack may demonstrate privilege escalation within the app but must not attempt OS-level privilege escalation.
5. **Deterministic.** The attack must produce the same result on every run (seed random generators, use fixed payloads).
6. **Reversible.** The attack must not cause irreversible changes. If it modifies data, it must restore the original state or the lab must have a reset mechanism.
7. **Bounded duration.** The attack must complete within 60 seconds.
8. **No denial-of-service.** The attack must not crash the target application. It demonstrates unauthorized access, not availability disruption (unless the class specifically covers DoS).
9. **Explicit safety markers.** Every attack file must include `<!-- SAFETY: ... -->` comments at the top and before each attack step, describing the safety constraint that applies.
10. **Education-first.** The attack script must include verbose logging that explains what it's doing at each step and why the attack succeeds against the vulnerable system.

## Output Format

The agent must produce:

### 1. `attacks/attack.py`

A Python script that:

```python
"""
Attack script for: {Class Title}
Vulnerability: {vulnerability theme}
Target: localhost:{default port}

SAFETY:
- Targets localhost ONLY. Will refuse non-local targets.
- No data exfiltration. Demonstrates access only.
- No persistence mechanisms.
- No OS-level privilege escalation.
- Deterministic: seeded random, fixed payloads.
- Completes within 60 seconds.
- Does not crash the target application.
"""

# <!-- SAFETY: Target validation - script exits if target is not localhost -->

import sys
import logging

logging.basicConfig(level=logging.INFO, format="[ATTACK] %(message)s")
logger = logging.getLogger(__name__)

TARGET = os.environ.get("ATTACK_TARGET", "http://localhost:5000")

def validate_target():
    """Ensure we are only attacking localhost."""
    # ... implementation ...

def step_1_recon():
    """Step 1: Reconnaissance — discover the application surface."""
    # <!-- SAFETY: Read-only reconnaissance, no modifications -->
    logger.info("Step 1: Enumerating endpoints...")
    # ... implementation ...

def step_2_exploit():
    """Step 2: Exploit the vulnerability."""
    # <!-- SAFETY: Demonstrates unauthorized access, no data exfiltration -->
    logger.info("Step 2: Exploiting {vulnerability}...")
    # ... implementation ...

def step_3_verify():
    """Step 3: Verify the attack succeeded."""
    logger.info("Step 3: Verifying attack success...")
    # ... implementation ...

def main():
    validate_target()
    step_1_recon()
    step_2_exploit()
    step_3_verify()
    logger.info("Attack complete. This would fail against the patched version.")

if __name__ == "__main__":
    main()
```

### 2. `attacks/README.md`

```markdown
# Attack Scenario: {Title}

## Overview
<!-- What this attack demonstrates and why -->

## Safety Constraints
<!-- List all safety constraints in force -->

## Prerequisites
<!-- What must be running before executing the attack -->

## Execution
<!-- How to run the attack -->

## Expected Output
<!-- What the student should see -->

## Control-Loop Analysis
<!-- Which control-loop element(s) the attack bypasses:
     - Sensor: ...
     - Estimator: ...
     - Controller: ...
     - Actuator: ...
     How the attack defeats each element -->

## What the Patch Prevents
<!-- Brief description of how the patched version stops this attack -->
```

## Constraints

1. **Localhost-only enforcement.** The attack script must include a `validate_target()` function that exits immediately if the target is not localhost.
2. **Safety markers in every file.** Both `attack.py` and `attacks/README.md` must contain `<!-- SAFETY: ... -->` markers.
3. **Verbose logging.** Every attack step must log what it's doing and why. Students learn by reading the logs.
4. **Return code semantics.** Exit code 0 = attack succeeded (vulnerable app). Exit code 1 = attack failed (patched app or error). Exit code 2 = safety check failed.
5. **No obfuscation.** Attack payloads must be human-readable. No encoding tricks that obscure the attack mechanism.
6. **Single vulnerability.** The attack exploits only the vulnerability specified in the class spec. Do not chain unrelated vulnerabilities.
7. **Requires running target.** The attack script must check that the target is reachable before proceeding. If the target is down, print a clear message and exit.
8. **No dependencies beyond requirements.** The attack must use only libraries in the lab's `requirements.txt` plus the Python standard library.
9. **Deterministic payloads.** All attack payloads must be fixed strings or seeded random values. No `uuid4()` or `time.time()` in payloads.
10. **Step-by-step structure.** The attack must be organized into numbered steps (functions) that execute sequentially.

## Prompt Skeleton

```
You are the Red-Team Scenario Agent for the "AI Security from Scratch" curriculum.
Your job is to create a safe, educational attack script that demonstrates the
vulnerability in the lab application. This is an EDUCATIONAL tool, not a weapon.

ATTACK SAFETY RULES:
1. Localhost only — refuse non-local targets
2. No data exfiltration — demonstrate access only
3. No persistence — no backdoors, no system modifications
4. No OS-level privilege escalation
5. Deterministic — seed random generators, use fixed payloads
6. Reversible — no irreversible changes
7. Bounded duration — must complete within 60 seconds
8. No denial-of-service — don't crash the target
9. Explicit safety markers in code and documentation
10. Education-first — verbose logging, clear explanations

CLASS SPECIFICATION:
---
{paste class-spec.yaml here}
---

VULNERABLE APPLICATION:
---
{paste vulnerable/app.py here}
---

INSTRUCTIONS:
1. Read the class specification and vulnerable application code.
2. Identify the vulnerability and how to exploit it.
3. Design a step-by-step attack that demonstrates the vulnerability.
4. Implement attacks/attack.py following the required structure:
   - validate_target() function
   - Numbered step functions
   - Verbose logging at each step
   - Safety markers before each step
   - Proper exit codes (0=success, 1=failure, 2=safety violation)
5. Write attacks/README.md with all required sections.
6. Ensure all safety constraints are satisfied.

CONSTRAINTS:
- Localhost-only enforcement with validate_target()
- Safety markers in both files
- Verbose logging at every step
- Exit codes: 0=success, 1=failure, 2=safety violation
- No obfuscated payloads
- Single vulnerability only
- Target reachability check
- Standard library + lab dependencies only
- Deterministic payloads
- Sequential step-by-step structure

OUTPUT:
Produce attacks/attack.py and attacks/README.md. Begin each file with:
--- FILE: {relative path} ---
```

## Validation Checklist

Before accepting the agent's output, verify:

- [ ] `attack.py` has `validate_target()` that exits on non-localhost targets
- [ ] Safety markers (`<!-- SAFETY: ... -->`) appear in both files
- [ ] Attack targets only the specified vulnerability
- [ ] Verbose logging at every step
- [ ] Exit codes follow the convention (0/1/2)
- [ ] No obfuscated payloads — all payloads are human-readable
- [ ] No data exfiltration
- [ ] No persistence mechanisms
- [ ] No OS-level privilege escalation
- [ ] Attack completes within 60 seconds
- [ ] Deterministic (seeded random, fixed payloads)
- [ ] Target reachability check before proceeding
- [ ] Dependencies limited to standard library + lab requirements
- [ ] Step-by-step structure with numbered functions
- [ ] `attacks/README.md` has all required sections including control-loop analysis
