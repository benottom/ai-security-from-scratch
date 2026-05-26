# Supervisory Controls for AI Systems

## What Are Supervisory Controls?

In control theory, a supervisory control is a higher-level controller that monitors and overrides the primary controller when it detects that the system is approaching or entering an unsafe state. The supervisory controller does not replace the primary controller — it constrains it. The primary controller handles the normal operation of the system; the supervisory controller handles the abnormal.

Consider a chemical plant. The primary controller regulates temperature, pressure, and flow rates to optimize production. The supervisory controller monitors these same variables and shuts down the plant if they exceed safety thresholds. The primary controller is designed for performance; the supervisory controller is designed for safety. They operate at different time scales, with different priorities, and with different failure modes.

AI systems need the same structure. The AI model is the primary controller — it is optimized for helpfulness, accuracy, and fluency. The supervisory controls are the safety layer — they are optimized for preventing unsafe behavior, regardless of how "helpful" the unsafe behavior might seem.

A supervisory control has three essential properties:

1. **It is external to the controller.** A constraint embedded in the system prompt is not a supervisory control — it is part of the controller, and can be overridden by prompt injection. A supervisory control must operate outside the controller's influence.
2. **It can override the controller.** A monitoring system that only logs violations without acting on them is not a supervisory control — it is an observability tool. A supervisory control must be able to block, modify, or replace the controller's output.
3. **It is deterministic.** The primary controller is probabilistic — it may or may not follow its instructions. The supervisory control must be deterministic — it must always enforce the constraint, every time, without exception.

## The Hierarchy of Controls

Supervisory controls are organized in a hierarchy, from most to least desirable:

### 1. Prevention

Prevent the unsafe state from being reached in the first place.

- Input validation that rejects adversarial inputs before they reach the controller
- Access control that limits the controller's capabilities to the minimum necessary
- Context separation that prevents different information sources from overriding each other
- Tool scoping that restricts available tools to only those needed for the current task

Prevention is the strongest control because it eliminates the possibility of the unsafe state. However, prevention is also the most difficult to achieve perfectly — adversarial inputs are creative and evolving.

### 2. Detection

Detect that the system is approaching or has entered an unsafe state.

- Output classification that identifies harmful, policy-violating, or unexpected content
- Anomaly detection that identifies unusual patterns in the controller's behavior
- Tool call monitoring that flags suspicious sequences or parameters
- Data flow tracking that identifies information leaking across boundaries

Detection does not prevent the unsafe state, but it enables a response. The critical requirement is that detection must be fast enough to enable response before the unsafe state causes harm.

### 3. Response

Take corrective action when an unsafe state is detected.

- Output blocking that prevents the unsafe output from reaching the user
- Tool call rejection that cancels a dangerous tool invocation
- Context reset that clears the controller's state and restarts the conversation
- Escalation to a human operator who can assess and resolve the situation

Response controls are only effective if detection works and if the response is faster than the harm. For real-time systems, automated response is essential; for asynchronous systems, human escalation may be sufficient.

### 4. Recovery

Return the system to a safe state after a violation.

- State rollback that reverts the system to its last known-safe configuration
- Incident logging that captures the full context of the violation for analysis
- Control update that modifies supervisory controls to prevent similar violations
- Notification that alerts stakeholders that a violation occurred

Recovery is the last line of defense. It does not prevent the violation, but it limits the damage and ensures that the system learns from the failure.

## Specific Supervisory Control Patterns

### Input Validation and Context Separation

Input validation examines the user's input before it reaches the controller. This includes:

- **Length limits**: Prevent context overflow by capping input length
- **Pattern detection**: Identify known injection patterns (e.g., "ignore previous instructions," "system:", role-playing prompts)
- **Encoding normalization**: Decode and normalize input to prevent encoding-based attacks (base64, unicode tricks, HTML entities)
- **Classification**: Use a separate model or rule system to classify the input as safe or suspicious

Context separation ensures that the controller can distinguish between different sources of information. This means:

- **Demarcation tokens**: Use clear markers to separate user input, system instructions, and retrieved content (e.g., `<user_input>`, `<retrieved_document>`, `<system_instruction>`)
- **Instruction isolation**: The system prompt explicitly instructs the model that instructions within `<user_input>` or `<retrieved_document>` tags are data, not commands
- **Structured prompts**: Use structured formats (JSON, XML) that make it harder for adversarial content to break out of its designated section

### Permission-Aware Retrieval

RAG systems must enforce access control at the retrieval level:

- **Document-level permissions**: Only retrieve documents that the current user is authorized to see
- **Field-level redaction**: Strip sensitive fields from retrieved documents before they reach the controller
- **Provenance tracking**: Record where each retrieved document came from, when it was last validated, and who authored it
- **Retrieval boundaries**: Limit the number of retrieved documents and their total size to prevent context overflow

### Tool Call Mediation and Approval Gates

Every tool call should pass through a mediation layer:

- **Parameter validation**: Validate tool call parameters against a schema (type, range, allowlist)
- **Permission checks**: Verify that the controller is authorized to call this tool with these parameters in this context
- **Approval gates**: For high-impact tools (financial transactions, data deletion, external communication), require human approval before execution
- **Execution sandboxing**: Run tool calls in a sandboxed environment that limits their side effects
- **Rate limiting**: Limit the frequency and total number of tool calls per session

### Output Validation and Redaction

Output validation examines the controller's output before it reaches the user:

- **PII detection**: Scan for personally identifiable information (names, email addresses, phone numbers, SSNs)
- **Secret detection**: Scan for API keys, passwords, tokens, and other credentials
- **URL validation**: Check that any URLs in the output are on an allowlist; flag or remove external URLs
- **Content classification**: Classify the output for harmful content, policy violations, or off-topic responses
- **System prompt leakage detection**: Check if the output contains fragments of the system prompt or internal instructions

### Policy-as-Code Enforcement

Policies should be expressed as executable code, not as natural language instructions:

- **Declarative policies**: Write policies in a policy language (e.g., Open Policy Agent/Rego, Cedar) that can be evaluated deterministically
- **Policy evaluation points**: Insert policy checks at every stage of the control loop (input, retrieval, tool call, output)
- **Policy versioning**: Track policy changes over time and maintain audit logs of which policy version was active during each request
- **Policy testing**: Write automated tests for policies just as you would for application code

Example policy in pseudocode:

```
policy email_send:
  match: tool_call.name == "send_email"
  condition:
    - recipient.domain in allowed_domains
    - not contains_pii(tool_call.params.body)
    - user.has_permission("email:send")
  action: allow
  otherwise: deny + log + escalate
```

### Circuit Breakers and Kill Switches

Circuit breakers detect when the system is failing and temporarily halt operations:

- **Error rate circuit breaker**: If the rate of policy violations exceeds a threshold, stop processing requests and alert operators
- **Tool call circuit breaker**: If an unusual number of tool calls are being rejected, disable the tool and alert operators
- **Anomaly circuit breaker**: If the controller's behavior deviates significantly from historical patterns, halt the system

A kill switch is an emergency shutdown mechanism that immediately stops the AI system:

- **Manual kill switch**: An operator can shut down the system with a single command
- **Automatic kill switch**: The system shuts itself down when a critical safety condition is met (e.g., a tool call attempts to access a forbidden resource)
- **Graceful degradation**: Instead of a full shutdown, the system falls back to a safe mode (e.g., text-only mode with no tool access)

## Why "Better Prompting" Is Not a Supervisory Control

A common response to AI security concerns is to improve the system prompt: "Just tell the model not to do X." This is not a supervisory control for three reasons:

1. **It is inside the controller.** The system prompt is processed by the same model that processes adversarial input. There is no architectural separation between the constraint and the thing being constrained. An adversarial input that overrides the system prompt removes the constraint entirely.

2. **It is probabilistic.** The model may follow the system prompt most of the time, but there is no guarantee. Adversarial inputs are specifically designed to find the cases where the model does not follow its instructions. A supervisory control must be deterministic — it must enforce the constraint every time.

3. **It is not auditable.** You cannot verify that a system prompt is being followed by inspecting the model's behavior. You can only test it empirically, and empirical testing cannot cover all possible inputs. A supervisory control produces auditable evidence — a policy evaluation log, a tool call rejection record, an output redaction event.

Better prompting is a useful layer of defense, but it must not be the only layer. It is the alignment layer, not the security layer. Security requires external, deterministic, auditable controls.

## Designing Layered Controls (Defense in Depth for AI)

Defense in depth for AI systems means applying supervisory controls at every stage of the control loop, so that the failure of any single control does not result in an unsafe state:

1. **Input stage**: Input validation and classification
2. **Observation stage**: Retrieval validation, access control, document scanning
3. **Controller stage**: Context separation, prompt hardening (as a soft control, not a supervisory one)
4. **Action stage**: Tool call mediation, approval gates, parameter validation
5. **Output stage**: Output validation, redaction, content classification
6. **Feedback stage**: Memory isolation, feedback validation
7. **System level**: Circuit breakers, kill switches, rate limiting

Each layer catches threats that bypass the previous layer. The result is a system where no single failure — no single bypassed filter, no single poisoned document, no single prompt injection — can lead to an unsafe state. This is the standard we should hold AI systems to, and the control-loop model gives us the structure to achieve it.
