# Observability and Feedback in Secure AI Systems

## You Cannot Secure What You Cannot See

The most dangerous security failures are the ones you do not know about. An AI system that produces a harmful output and you catch it is an incident. An AI system that produces a harmful output and you do not catch it is a breach. The difference is observability.

Observability in control theory is the ability to determine the internal state of a system from its outputs. A system is observable if, by watching its behavior, you can reconstruct what it is doing and why. A system is unobservable if it can be in an unsafe state without any external indication.

Most AI systems today are critically under-observable. They receive inputs, produce outputs, and the internals — what documents were retrieved, what policy decisions were made, what tool calls were considered but rejected — are invisible. You see the final answer, but you cannot see the reasoning, the alternatives, or the control decisions that shaped it.

This is unacceptable for a security-critical system. You need to know:

- What observations did the controller receive?
- What actions did it consider?
- What supervisory controls were evaluated?
- Which controls were triggered, and what did they do?
- What was the final action, and why was it deemed safe?

Without this information, you cannot detect attacks, you cannot debug failures, you cannot improve controls, and you cannot produce assurance evidence. Observability is not a nice-to-have — it is a prerequisite for security.

## The Control Ledger

The control ledger is the central observability construct for secure AI systems. It is a structured, append-only log that records every significant security decision in the control loop. Every time the system evaluates a policy, applies a supervisory control, or makes a decision that affects security, it writes an entry to the control ledger.

The control ledger has three essential properties:

1. **Observable**: Every important security decision is recorded, not just the final output
2. **Explainable**: Each entry contains enough context to understand why the decision was made
3. **Testable**: The ledger can be queried and analyzed to verify that security controls are working correctly

The control ledger is not the same as a general application log. Application logs are for debugging; the control ledger is for security assurance. Application logs are ad hoc and unstructured; the control ledger follows a defined schema and is designed to be queried for security evidence.

## Event Schema for AI Security Decisions

Every entry in the control ledger follows a consistent schema:

```json
{
  "event_id": "uuid-v4",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "session_id": "session-abc123",
  "request_id": "req-def456",
  "event_type": "policy_evaluation | control_activation | tool_call | retrieval | output_check | state_transition",
  "stage": "input | observation | controller | action | output | feedback",
  "actor": "system | user | controller | supervisory_control | tool",
  "control_id": "INV-1 | SS-EX-1 | policy:email_send | ...",
  "decision": "allow | deny | modify | escalate | warn",
  "input_snapshot": {
    "description": "Summary of the input that triggered this event",
    "source": "user_message | retrieved_document | tool_result | memory | system_prompt"
  },
  "output_snapshot": {
    "description": "Summary of the output or action resulting from this event",
    "redacted": true
  },
  "policy_version": "v2.3",
  "metadata": {}
}
```

### Event Types

| Event Type | When It Fires | What It Records |
|---|---|---|
| `policy_evaluation` | A policy check is performed | Policy ID, input, decision, rationale |
| `control_activation` | A supervisory control is triggered | Control ID, trigger condition, action taken |
| `tool_call` | The controller attempts to call a tool | Tool name, parameters (redacted if sensitive), approval status |
| `retrieval` | Documents are retrieved from the knowledge base | Query, documents retrieved (IDs and metadata, not full content), access control decision |
| `output_check` | The output is validated before delivery | Check type, findings, actions taken |
| `state_transition` | The system transitions between states | Previous state, new state, transition trigger |

## What to Log

Not everything should be logged — that would create noise and privacy concerns. But the following must always be logged:

### Inputs

- The classification of the input (safe, suspicious, adversarial)
- Any input validation failures
- The source of the input (user, tool result, memory, system)

### Policy Decisions

- Every policy evaluation and its result
- The policy version that was active
- The specific rule that triggered the decision
- The rationale for the decision (especially for deny/modify decisions)

### Retrieval Results

- The query that was used
- The documents that were retrieved (IDs, metadata, security classification)
- The access control decision for each document
- Any validation findings (e.g., "document contains instruction-like patterns")

### Tool Calls

- The tool that was called
- The parameters (redacted for sensitive values)
- The approval decision (approved, denied, escalated)
- The execution result (success, failure, side effects)

### Output Checks

- The checks that were performed
- Any findings (PII detected, URL flagged, content policy violation)
- The actions taken (redacted, blocked, passed through)
- The final output (hash, not full content, for privacy)

## Feedback Loops in AI Systems and How They Can Be Attacked

A feedback loop is any mechanism by which the system's past outputs influence its future behavior. AI systems have several feedback loops:

### Conversation History

The most common feedback loop: the model's previous responses are included in the context for the next turn. This means that if the model produces an error or is manipulated in one turn, that error or manipulation persists into subsequent turns.

**Attack**: An attacker injects a false premise into the conversation in turn 1, and the model builds on that premise in turns 2, 3, and 4, producing increasingly divergent outputs.

### Memory Systems

Some AI systems have long-term memory that persists across sessions. Information stored in memory is retrieved and used as context in future conversations.

**Attack**: An attacker implants malicious instructions in the memory store (e.g., through a compromised conversation that writes to long-term memory). These instructions are retrieved in future sessions and influence the model's behavior — even when the attacker is no longer involved.

### Tool Result Processing

Tool results are fed back into the controller's context. If a tool is compromised or returns malicious content, that content becomes part of the controller's observations for subsequent reasoning.

**Attack**: A web search tool returns a page that contains a prompt injection payload. The controller reads the search result and follows the injected instructions, which cause it to call a different tool with dangerous parameters.

### Reward and Optimization Feedback

In systems that use feedback for optimization (e.g., RLHF, user ratings, A/B testing), the feedback signal can be manipulated to reward unsafe behavior.

**Attack**: An attacker provides positive feedback (thumbs up, high rating) for unsafe outputs and negative feedback for safe outputs, gradually shifting the system's behavior toward unsafe territory.

## Positive vs. Negative Feedback in Security Context

In control theory, positive feedback amplifies a signal (pushing the system further from equilibrium), while negative feedback dampens a signal (returning the system toward equilibrium). Both have security implications:

### Positive Feedback (Destabilizing)

- A model that produces a slightly harmful output and, because the user engages with it, produces increasingly harmful outputs in subsequent turns
- A tool call that returns information that enables more powerful tool calls, which return more information, creating an escalation chain
- A memory system that reinforces biased or incorrect information each time it is retrieved and re-stored

**Mitigation**: Supervisory controls that detect escalation patterns and intervene (circuit breakers, rate limits, escalation detection).

### Negative Feedback (Stabilizing)

- An output validation system that detects a policy violation, corrects the output, and logs the violation for analysis — reducing the likelihood of similar violations in the future
- A user correction that causes the model to adjust its behavior in subsequent turns
- A policy engine that tightens constraints when violations are detected (adaptive controls)

**Design principle**: Security feedback loops should be negative — they should push the system toward safe behavior, not amplify deviations.

## Designing Monitoring That Detects Control-Loop Failures

Effective monitoring for AI systems must go beyond simple metrics (latency, error rate, token count). It must detect failures in the control loop itself:

### Controller Health

- **Instruction adherence rate**: How often does the controller follow its system prompt? Measured by sampling outputs and checking against expected behavior.
- **Injection susceptibility rate**: How often does the controller follow instructions from untrusted sources? Measured by red-team tests.
- **Hallucination rate**: How often does the controller produce fabricated information? Measured by sampling outputs and verifying against source documents.

### Supervisory Control Effectiveness

- **Control activation rate**: How often are supervisory controls triggered? A rate that is too low may indicate that controls are not sensitive enough; a rate that is too high may indicate that the controller is frequently producing unsafe outputs.
- **Control bypass rate**: How often does an unsafe state occur despite the supervisory control being active? This should be zero — any bypass is a critical security finding.
- **False positive rate**: How often do controls trigger on safe behavior? High false positives erode trust and lead to controls being disabled.

### Loop Integrity

- **Observation integrity**: Are the observations reaching the controller what we expect? Monitored by hashing retrieved documents and comparing against a known-good index.
- **Feedback integrity**: Are tool results and memory retrievals what we expect? Monitored by validating tool results against expected schemas and provenance records.
- **Action integrity**: Are the actions being taken the ones the controller intended? Monitored by comparing the controller's planned actions against the executed actions.

## The Relationship Between Observability and Assurance Evidence

Observability and assurance are two sides of the same coin. Assurance evidence is the argument that a system is secure; observability is the mechanism that produces the data for that argument.

A control ledger that records every security decision, every policy evaluation, every control activation, and every output check is not just an operational tool — it is the raw material for assurance. When an auditor asks "how do you know your system doesn't leak PII?", the answer is not "we have a content filter" — it is "here are the 10,000 control ledger entries showing the PII detection control evaluating every output, here are the 47 cases where it activated, and here are the zero cases where PII appeared in the final output despite the control."

This is the difference between claiming security and demonstrating it. Observability makes security demonstrable. Without it, security is opinion.

The next document in this series will show how to turn observability data into structured assurance evidence that maps to governance frameworks and can be presented to executives, auditors, and regulators.
