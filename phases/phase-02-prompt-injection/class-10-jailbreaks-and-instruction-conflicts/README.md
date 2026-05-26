# Jailbreaks and Instruction Conflicts

> **Module:** Phase 2 — Prompt Injection | **Class:** 10 | **Duration:** 4 hours

## Learning Objectives

By the end of this class, students will be able to:

1. Define jailbreaking as the creation of instruction conflicts that exploit the model's instruction-following tendency
2. Demonstrate multi-turn manipulation, role-playing attacks, and competing-objectives exploitation
3. Analyze why instruction hierarchy matters and what happens when it is absent or poorly enforced
4. Implement instruction priority enforcement and conflict detection mechanisms
5. Design defenses that handle the inherent tension between helpfulness and safety

---

## Control-Theoretic View

Every class in this curriculum models a security concept as a control loop. This section defines the control-theoretic framing for jailbreaks and instruction conflicts.

### Objective

The safety goal the system must maintain:

> Ensure that when multiple instructions conflict, safety constraints always take precedence over helpfulness directives, and that the model never produces output that violates its safety policy regardless of how the conflict is framed.

### Controller

The component responsible for making decisions to maintain the objective:

> The instruction priority enforcer — a system that assigns explicit priority levels to different instruction categories (safety > identity > task > style) and resolves conflicts by always selecting the highest-priority instruction. This enforcer operates both at the prompt-engineering level (instruction hierarchy in the system prompt) and at the architectural level (middleware that detects and blocks instruction conflicts in the output).

### Observations

What the controller can perceive about the system state:

| Observation | Source | Frequency |
|---|---|---|
| Instruction conflict detection score | Conflict detector | Per request |
| Output safety classification | Output classifier | Per response |
| Role-play or persona shift detection | Persona monitor | Per request |
| Conversation manipulation trajectory | Conversation analyzer | Per turn |
| Safety-policy compliance confidence | Output validator | Per response |

### Actions

What the controller can do to influence the system:

| Action | Effect | Preconditions |
|---|---|---|
| Enforce instruction priority | Resolves conflicts in favor of safety constraints | Conflicting instructions detected |
| Block persona adoption | Prevents model from adopting personas that bypass safety | Unauthorized persona shift detected |
| Inject safety reminder | Prepends safety reinforcement before generation | Safety compliance confidence drops |
| Terminate manipulation chain | Breaks multi-turn manipulation by resetting context | Manipulation trajectory detected |
| Override with safe fallback | Replaces unsafe output with a safe alternative | Output violates safety policy |

### Feedback

How the controller learns whether its actions achieved the objective:

> Post-generation safety compliance scoring provides feedback on whether instruction conflicts were correctly resolved. When a jailbreak succeeds, the failure is analyzed to determine which conflict resolution rule was missing or bypassed, and the instruction priority enforcer is updated accordingly. Longitudinal tracking of jailbreak success rates feeds back into the priority weighting system.

### Disturbances

External factors that can push the system away from the objective:

| Disturbance | Source | Mitigation |
|---|---|---|
| Role-playing prompts ("pretend you are DAN") | Adversarial user | Persona detection + priority enforcement |
| Competing objectives ("be helpful AND do this unsafe thing") | Adversarial user | Instruction hierarchy with safety-first resolution |
| Multi-turn manipulation building trust before exploiting | Patient adversary | Conversation-level trajectory analysis |
| Emotional manipulation ("my life depends on this") | Social engineering | Policy-based override (no exception for emotional appeals) |
| Hypothetical framing ("in a fictional world where...") | Creative framing | Fictionality detection + safety boundary enforcement |

### Unsafe States

States in which the system violates its safety objective:

| Unsafe State | Condition | Consequence |
|---|---|---|
| Safety policy overridden by helpfulness | Model chooses to be helpful at the expense of safety | Harmful content produced |
| Unauthorized persona adopted | Model role-plays as an unrestricted entity | All safety constraints bypassed |
| Manipulation chain completed | Multi-turn manipulation achieves its goal | Targeted harmful output |
| Fictionality boundary crossed | Model transfers fictional content to real-world advice | Unsafe instructions provided as real |
| Safety override justified | Model makes an exception to safety policy | Precedent set for future overrides |

### Supervisory Controls

Higher-level controls that monitor and override the primary controller:

> An output safety classifier that independently evaluates every response against the full safety policy, regardless of what instructions the model received or what persona it adopted. This classifier cannot be overridden by prompt engineering and serves as the final safety gate. Additionally, a conversation-level manipulation detector that tracks the trajectory of multi-turn conversations and flags when the conversation is systematically moving toward a jailbreak objective.

### Monitoring

Ongoing observability for the control loop:

| Metric | Threshold | Alert |
|---|---|---|
| Jailbreak success rate | > 0% over rolling 24 hours | Critical alert |
| Instruction conflict frequency | > 5 per session | Warning |
| Persona shift attempt rate | > 2 per session | Warning |
| Multi-turn manipulation detection rate | > 1 per 1000 sessions | Warning to security team |
| Safety compliance confidence average | < 0.9 over 1000 responses | Warning to ML ops |

### Recovery

Procedures for restoring the system to a safe state after a violation:

1. Immediately block the unsafe output from reaching the user
2. Reset the conversation context to remove the manipulation chain
3. Analyze the jailbreak technique to identify the missing priority rule
4. Update the instruction priority enforcer with the new conflict resolution rule
5. Add the specific jailbreak pattern to the security regression test suite
6. Run the full test suite to verify the fix and ensure no regressions
7. Document the incident and generate an evidence package

---

## Lab Summary

| Lab | Topic | Duration |
|---|---|---|
| Lab 10a | Jailbreaking the Chatbot with Role-Playing and Conflicts | 40 minutes |
| Lab 10b | Building an Instruction Priority Enforcer | 50 minutes |
| Lab 10c | Multi-Turn Manipulation Detection | 30 minutes |

Each lab follows the standard 8-step flow.

---

## Deliverables

- [ ] Completed lab worksheet with jailbreak technique analysis
- [ ] Working instruction priority enforcer with conflict detection
- [ ] Multi-turn manipulation detector implementation
- [ ] Passing security regression test suite (minimum 5 test cases)
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

- Completion of Classes 07-09
- Familiarity with instruction hierarchy concepts and output validation
- Working development environment

---

## References

1. OWASP Top 10 for LLM Applications (2025) — LLM01: Prompt Injection
2. Wei, A., et al. (2024). "Assessing the Brittleness of Safety Alignment via Pruning and Low-Rank Modifications"
3. Zou, A., et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models"
4. Leveson, N. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety*
5. Anthropic (2024). "Many-shot Jailbreaking"

---

*Class 10 | AI Security from Scratch*
