# Lesson: Prompt Injection Defense Patterns

## Overview

Prompt injection cannot be prevented by any single defense. This is not a limitation of current technology — it is a fundamental property of the problem. The model processes all tokens in its context window through the same mechanism, and no amount of prompt engineering or input filtering can guarantee that adversarial content will never influence model behavior. The solution is defense in depth: multiple independent, complementary layers of defense, each covering the gaps left by the others.

This class brings together the individual defenses from Classes 07-10 into a unified framework. We examine five primary defense patterns, explain why each is necessary but insufficient alone, and show how to compose them into a complete security architecture.

## Why This Matters

The history of computer security teaches a clear lesson: single points of failure inevitably fail. Firewalls alone did not secure networks. Antivirus alone did not secure endpoints. Authentication alone did not secure applications. Every successful security architecture uses multiple layers — defense in depth — because each layer covers the failures of the others.

LLM security is no different. Input validation alone misses novel injection techniques. Context separation alone can be bypassed by models that follow instructions regardless of delimiters. Output filtering alone allows the model to be compromised even if the output is eventually blocked. Monitoring alone detects attacks after they succeed. Each defense is necessary, but none is sufficient.

## The Five Defense Patterns

### Pattern 1: Context Separation

**What it does:** Structurally separates different categories of content in the model's context window so the model can distinguish between instructions it should follow and data it should process.

**How it works:** Use XML tags, delimiters, or special tokens to mark each content category:
- `<system_instructions>`: The system prompt (highest authority)
- `<retrieved_data>`: Content from external sources (data only)
- `<user_query>`: The user's question (to be answered under system instructions)

**Why it's insufficient:** The model may still follow instructions found in `<retrieved_data>` despite the delimiter. Delimiters are signals, not enforcement mechanisms. A sufficiently motivated model (or one that has been jailbroken) can ignore structural cues.

**Coverage:** Prevents casual injection through data channels. Does not prevent determined injection or model-level compromise.

### Pattern 2: Instruction Hierarchy

**What it does:** Establishes and enforces a fixed priority ordering for instructions, so that when instructions conflict, the higher-priority instruction always wins.

**How it works:** Define an explicit hierarchy (safety > identity > task > style) and implement it both at the prompt level (explicit priority statements) and at the architectural level (middleware that resolves conflicts before generation).

**Why it's insufficient:** The model has no hardcoded mechanism to enforce this hierarchy. The priority statement is itself an instruction that can be overridden. Architectural enforcement helps but cannot guarantee the model will follow the resolved instruction.

**Coverage:** Resolves explicit instruction conflicts. Does not prevent subtle manipulations that don't create obvious conflicts.

### Pattern 3: Input Validation

**What it does:** Classifies and validates user input before it reaches the model, blocking or sanitizing content that appears to be adversarial.

**How it works:** Use pattern matching, ML-based classification, or rule-based systems to detect injection indicators: override instructions, persona adoption requests, encoding tricks, and extraction attempts.

**Why it's insufficient:** Pattern-based detection misses novel attacks. ML-based detection can be evaded by adversarial examples. No classifier achieves 100% recall. Determined attackers will find inputs that evade validation.

**Coverage:** Blocks known attack patterns and raises the bar for attackers. Does not eliminate injection risk.

### Pattern 4: Output Filtering

**What it does:** Independently validates every model response against safety policies before delivering it to the user.

**How it works:** After generation, classify the output for safety policy compliance, system prompt leakage, and instruction override. Block, redact, or replace responses that violate policy.

**Why it's insufficient:** Output filtering is reactive — it catches compromises after they occur. It cannot prevent the model from being influenced by injection, only prevent the influenced output from reaching the user. Some compromises (e.g., data exfiltration via tool calls) may not be visible in the output.

**Coverage:** Catches injection attacks that bypass input-side defenses. Essential as a backstop but does not prevent the model from being compromised.

### Pattern 5: Monitoring and Anomaly Detection

**What it does:** Continuously observes the system's behavior for patterns that indicate successful or attempted injection attacks.

**How it works:** Track injection attempt rates, instruction-following fidelity scores, output policy violation rates, and per-user/per-session behavioral patterns. Alert when metrics exceed thresholds.

**Why it's insufficient:** Monitoring detects attacks after they happen. It provides no prevention — only detection and response. An attack that succeeds and causes irreversible damage (e.g., data exfiltration) will be detected but not prevented.

**Coverage:** Provides visibility into the system's security posture and enables rapid response. Does not prevent attacks.

## Why No Single Defense Is Sufficient

Each defense pattern covers a specific gap in the control loop:

| Defense Pattern | Control-Loop Position | Covers | Misses |
|---|---|---|---|
| Context Separation | Observation → Controller | Casual data-channel injection | Determined model-level compromise |
| Instruction Hierarchy | Controller decision logic | Explicit instruction conflicts | Subtle manipulations without obvious conflicts |
| Input Validation | Observation channel | Known attack patterns | Novel attacks and encoding tricks |
| Output Filtering | Actuation channel | Compromised outputs | Non-output attacks (tool calls, data exfiltration) |
| Monitoring | Feedback channel | Attack patterns and trends | Individual zero-day attacks |

The key insight is that each defense operates at a different point in the control loop. No single point covers all failure modes. Defense in depth means covering the entire loop.

## Defensive Design: Composing the Patterns

The complete defense architecture routes each request through all five patterns in sequence:

1. **Input Validation** (observation channel gate): Classify and validate input before it enters the system
2. **Context Separation** (observation composition): Structure the context to separate data from instructions
3. **Instruction Hierarchy** (controller logic): Resolve any remaining conflicts with safety-first priority
4. **Output Filtering** (actuation gate): Validate the response before delivery
5. **Monitoring** (feedback loop): Track system behavior and alert on anomalies

This composition ensures that:
- An attack that bypasses Input Validation is caught by Context Separation or Instruction Hierarchy
- An attack that bypasses all input-side defenses is caught by Output Filtering
- An attack that somehow reaches the user is detected by Monitoring and triggers investigation

## What Learners Will Build

1. **A composed defense architecture** that routes requests through all five patterns
2. **A defense orchestration layer** that manages the interaction between patterns
3. **A defense effectiveness measurement framework** that tracks each layer's detection rate, false positive rate, and processing latency
4. **A defense tuning system** that adjusts sensitivity based on threat level and false positive feedback
5. **Security regression tests** that verify the composed defense blocks known attack patterns while allowing legitimate use

## Common Mistakes

1. **Deploying only one defense**: Any single defense can be bypassed. Always deploy at least three layers covering different control-loop positions.

2. **Deploying all defenses at maximum sensitivity**: This maximizes security but destroys usability with false positives. Tune each layer based on its position and coverage.

3. **Not testing defense interactions**: Layer A's output may inadvertently defeat Layer B. Integration testing of the full defense stack is essential.

4. **Not measuring defense effectiveness**: If you don't measure detection rates and false positive rates, you don't know if your defenses are working.

5. **Not updating defenses**: The threat landscape evolves. Regularly update pattern databases, retrain classifiers, and re-run security regression tests.

## Key Takeaways

1. **No single defense is sufficient.** Each pattern covers a specific gap in the control loop, and each gap requires a different defense.

2. **Defense in depth covers the entire control loop.** Input validation at the observation gate, context separation and instruction hierarchy in the controller, output filtering at the actuation gate, and monitoring in the feedback loop.

3. **The defense orchestration layer manages interactions between patterns.** Just as a security operations center coordinates firewalls, IDS, and SIEM, the orchestration layer coordinates the five defense patterns.

4. **Measuring effectiveness is as important as deploying defenses.** Without measurement, you have security theater. Track detection rates, false positive rates, and bypass rates for each layer.

5. **The tradeoff between security and usability is real and must be managed.** Over-aggressive defenses block legitimate use; under-aggressive defenses allow attacks. Tune based on data, not intuition.

---

*Class 11 Lesson | AI Security from Scratch*
