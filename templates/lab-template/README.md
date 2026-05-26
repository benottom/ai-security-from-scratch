# Lab [LAB_NUMBER]: [LAB_TITLE]

> **Class:** [CLASS_REFERENCE] | **Difficulty:** [BEGINNER|INTERMEDIATE|ADVANCED] | **Estimated Time:** [DURATION] minutes

---

## Lab Overview

[BRIEF_DESCRIPTION — A 2–3 sentence overview of what this lab demonstrates and why it matters in the context of AI security.]

## Objectives

1. [OBJECTIVE_1 — e.g., "Observe how [VULNERABILITY] manifests in a vulnerable AI application"]
2. [OBJECTIVE_2 — e.g., "Analyze the control-loop failure that enables the attack"]
3. [OBJECTIVE_3 — e.g., "Implement [DEFENSE_PATTERN] as a corrective control"]
4. [OBJECTIVE_4 — e.g., "Verify the defense via security regression tests"]
5. [OBJECTIVE_5 — e.g., "Generate auditable evidence of the fix"]

---

## Pre-Lab Setup

### Environment Requirements

- [ ] Python 3.11+ installed
- [ ] Docker and Docker Compose installed
- [ ] `make` utility available
- [ ] [ADDITIONAL_REQUIREMENT_1]
- [ ] [ADDITIONAL_REQUIREMENT_2]

### Initial Setup

```bash
# Clone the lab repository (if not already cloned)
git clone [REPO_URL]
cd [LAB_DIRECTORY]

# Run the standard setup
make setup
```

### Verify Setup

```bash
# Confirm the vulnerable application starts
make run-vulnerable

# You should see:
#   [EXPECTED_STARTUP_OUTPUT]
```

---

## Lab Flow

### Step 1: Start the Vulnerable Application

```bash
make run-vulnerable
```

**What this does:** Launches the intentionally vulnerable version of the application with all security controls disabled or absent.

**Expected output:**
```
[EXPECTED_OUTPUT_STEP_1]
```

**Control-loop state:** The system is operating without [MISSING_CONTROL]. The objective "[CONTROL_OBJECTIVE]" has no enforcer.

---

### Step 2: Run a Normal Test (Establish Baseline)

```bash
make test-baseline
```

**What this does:** Sends legitimate, well-formed inputs to the application and records the expected behavior.

**Expected results:**

| Input | Expected Output | Status |
|---|---|---|
| [NORMAL_INPUT_1] | [NORMAL_OUTPUT_1] | ✅ Pass |
| [NORMAL_INPUT_2] | [NORMAL_OUTPUT_2] | ✅ Pass |
| [NORMAL_INPUT_3] | [NORMAL_OUTPUT_3] | ✅ Pass |

**Observation:** The application behaves correctly for normal inputs, but normal tests do not exercise adversarial conditions.

---

### Step 3: Execute the Attack

```bash
make attack
```

**What this does:** Sends the adversarial input that exploits the [VULNERABILITY_TYPE] vulnerability.

**Attack payload:**
```
[ATTACK_PAYLOAD_OR_DESCRIPTION]
```

**Expected output (vulnerable app):**
```
[VULNERABLE_OUTPUT_SHOWING_EXPLOITATION]
```

---

### Step 4: Observe the Failure

**What failed:**

> [FAILURE_DESCRIPTION — e.g., "The model executed a system-level command injected through user input, violating the control objective that user input must not influence system behavior."]

**Evidence of failure:**
```
[FAILURE_EVIDENCE — logs, output, or observed behavior]
```

**Severity:** [CRITICAL|HIGH|MEDIUM|LOW]

---

### Step 5: Explain the Control-Loop Failure

Analyze the attack through the control-theoretic lens:

| Control-Loop Element | Status | Explanation |
|---|---|---|
| **Objective** | ❌ Violated | [WHY_OBJECTIVE_VIOLATED] |
| **Controller** | ❌ Absent/Insufficient | [WHY_CONTROLLER_FAILED] |
| **Observations** | ❌ Blind spot | [WHAT_WAS_NOT_OBSERVED] |
| **Actions** | ❌ No corrective action | [WHAT_ACTION_SHOULD_HAVE_OCCURRED] |
| **Feedback** | ❌ No feedback path | [WHY_NO_FEEDBACK] |
| **Disturbance** | ⚠️ Unmitigated | [WHAT_DISTURBANCE_EXPLOITED] |

**Root cause:** [ROOT_CAUSE_ANALYSIS]

**Diagram:**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Disturbance │────▶│   System     │────▶│  Unsafe State│
│  (Attack)    │     │  (No control)│     │  (Violation) │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                     Missing controller
                     Missing feedback
```

---

### Step 6: Implement the Defense

Apply the [DEFENSE_PATTERN_NAME] pattern:

```python
# [DEFENSE_IMPLEMENTATION_CODE]
# Example:
# class [ControllerName]:
#     def __init__(self, config):
#         self.config = config
#
#     def observe(self, input_data):
#         """Classify and validate input against policy."""
#         ...
#
#     def decide(self, observation):
#         """Determine if input is safe or requires intervention."""
#         ...
#
#     def act(self, decision):
#         """Apply the control action (block, sanitize, escalate)."""
#         ...
```

**Control-loop restoration:**

| Element | Implementation |
|---|---|
| **Objective** | Restored — [HOW] |
| **Controller** | Added — [WHAT] |
| **Observations** | Added — [WHAT_IS_NOW_OBSERVED] |
| **Actions** | Added — [WHAT_ACTIONS_ARE_NOW_POSSIBLE] |
| **Feedback** | Added — [HOW_FEEDBACK_WORKS_NOW] |

---

### Step 7: Run the Security Regression Test

```bash
make test-security
```

**What this does:** Runs the full security test suite, including:
- The original attack (must now be blocked)
- Variant attacks (must also be blocked)
- Normal inputs (must still work correctly)

**Expected results:**

| Test Case | Type | Vulnerable App | Patched App | Status |
|---|---|---|---|---|
| [TEST_1_NAME] | Attack | ❌ Exploited | ✅ Blocked | Pass |
| [TEST_2_NAME] | Attack Variant | ❌ Exploited | ✅ Blocked | Pass |
| [TEST_3_NAME] | Normal Input | ✅ Pass | ✅ Pass | Pass |
| [TEST_4_NAME] | Normal Input | ✅ Pass | ✅ Pass | Pass |
| [TEST_5_NAME] | Edge Case | ⚠️ Unexpected | ✅ Handled | Pass |

---

### Step 8: Generate Evidence

```bash
make evidence
```

**What this does:** Produces an evidence package containing:
- Security test results (JUnit XML)
- Control-loop analysis document
- Attack reproduction logs
- Defense implementation diff
- Timestamp and environment metadata

**Evidence output directory:** `./evidence/[TIMESTAMP]/`

---

## Standard Make Commands

| Command | Description |
|---|---|
| `make setup` | Initialize the lab environment, install dependencies, build Docker images |
| `make run-vulnerable` | Start the intentionally vulnerable application |
| `make attack` | Execute the standard attack payload against the running application |
| `make run-patched` | Start the patched (secured) application with defenses enabled |
| `make test-security` | Run the full security regression test suite |
| `make test-baseline` | Run normal (non-adversarial) functional tests |
| `make evidence` | Generate the evidence package for this lab |
| `make clean` | Stop all containers and remove generated artifacts |
| `make help` | Display available make targets and descriptions |

---

## Expected Results

### Vulnerable Application

- **Normal inputs:** Processed correctly
- **Attack inputs:** Exploitation succeeds — [SPECIFIC_FAILURE_MODE]
- **Security tests:** ❌ Fail — attack test cases are not blocked

### Patched Application

- **Normal inputs:** Processed correctly (no regression)
- **Attack inputs:** Blocked or neutralized — [SPECIFIC_DEFENSE_BEHAVIOR]
- **Security tests:** ✅ Pass — all attack variants are blocked, normal inputs work

---

## Cleanup

```bash
# Stop all running containers
make clean

# Remove evidence artifacts (optional)
rm -rf ./evidence/

# Reset the repository to clean state
git checkout -- .
```

---

## Key Takeaways

1. [TAKEAWAY_1 — e.g., "Without an active controller, [VULNERABILITY_TYPE] attacks proceed unimpeded."]
2. [TAKEAWAY_2 — e.g., "Security tests must exercise adversarial conditions, not just normal inputs."]
3. [TAKEAWAY_3 — e.g., "Control-loop analysis reveals exactly where and why the defense failed."]

---

*Template version: 1.0.0 | AI Security from Scratch*
