# Assignment: Anatomy of LLM Applications

## Instructions

Complete all exercises below. Each exercise builds on the concepts from the lesson, control-loop analysis, threat model, and lab. Submit your work as Markdown files in the `solutions/` directory.

---

## Exercise 1: Component Security Audit (Easy)

**Objective**: Demonstrate understanding of LLM application components and their security properties.

Consider the following LLM application architecture for a medical consultation chatbot:

> The chatbot accepts patient questions, retrieves relevant medical literature from a curated database, and generates responses. It has access to a tool that can query the patient's electronic health record (EHR) system. Conversation history is stored in a database for continuity across sessions. The system prompt instructs the LLM to only provide general health information and never diagnose or prescribe.

### Tasks

1. **List all components** in this application and classify each as a control-loop element (controller, sensor, actuator, state store, or interface). For each component, specify:
   - Its role in the system
   - Its inputs and outputs
   - Whether its outputs should be considered trusted, partially trusted, or untrusted
   - One specific way it can fail or be exploited

2. **Identify the three most critical trust boundaries** in this system. For each boundary:
   - Specify which components it separates
   - Describe what data crosses the boundary
   - Explain what could go wrong if no controls exist at this boundary
   - Propose one concrete security control for this boundary

3. **Consider the specific domain** (medical consultation): How does the domain affect the threat model? What additional risks or constraints does a medical chatbot face compared to a general-purpose chatbot?

### Deliverable

`solutions/exercise1.md` — Component audit document with all three tasks completed.

### Grading Criteria

| Criterion | Points |
|---|---|
| All components identified and classified correctly | 3 |
| Trust levels justified with reasoning | 3 |
| Trust boundaries correctly identified with appropriate controls | 3 |
| Domain-specific analysis demonstrates understanding of context | 1 |
| **Total** | **10** |

---

## Exercise 2: Attack Surface Mapping and Exploit Scenario (Medium)

**Objective**: Apply the threat model to construct a realistic multi-step attack against an LLM application.

Using the vulnerable application from the lab (or the medical chatbot from Exercise 1 if you prefer), construct a **realistic multi-step attack** that chains vulnerabilities across at least two components.

### Tasks

1. **Describe your attack scenario** in detail:
   - What is the attacker's goal? (e.g., exfiltrate patient data, cause unauthorized EHR access, extract the system prompt, persist malicious instructions in memory)
   - What is the attacker's initial access? (e.g., authenticated user, document uploader, external API operator)
   - What are the steps of the attack? (number each step)

2. **Map each step to the control-loop model**:
   - Which control-loop element does each step target? (sensor, controller, actuator, state store)
   - What disturbance does each step introduce?
   - Which trust boundary does each step cross?
   - What unsafe state does each step create or exploit?

3. **Identify the detection opportunities**:
   - At which step(s) could the attack be detected if proper monitoring were in place?
   - What specific monitoring would detect it? Be concrete about the signals and thresholds.
   - Why would current monitoring (if any) fail to detect it?

4. **Design a defense-in-depth mitigation**:
   - Propose at least three controls at different boundaries that would prevent, detect, or limit this attack
   - For each control, specify: where it is placed, what it checks, and what it does when triggered
   - Explain why three controls are needed (why one or two are insufficient)

### Deliverable

`solutions/exercise2.md` — Attack scenario document with all four tasks completed.

### Grading Criteria

| Criterion | Points |
|---|---|
| Attack scenario is realistic and detailed | 3 |
| Each step correctly mapped to control-loop elements and trust boundaries | 3 |
| Detection opportunities accurately identified with concrete monitoring proposals | 3 |
| Defense-in-depth mitigation is well-designed with justified layering | 3 |
| Analysis shows understanding of cross-component vulnerability chaining | 3 |
| **Total** | **15** |

---

## Exercise 3: Security Architecture Design (Hard)

**Objective**: Design a complete security architecture for an LLM application, applying defense-in-depth principles across all components.

You are the security architect for a new LLM application — a **financial advisory chatbot** with the following features:

- Users can ask questions about their investment portfolio
- The chatbot retrieves real-time market data from external APIs
- The chatbot can execute trades on behalf of the user (with user confirmation)
- The chatbot has access to the user's full financial history
- Conversation history and user preferences are stored for continuity
- Multiple users share the same LLM instance but have different portfolios and permissions
- Regulatory requirements mandate: audit logging of all actions, no cross-user data leakage, and human review of all trades above $10,000

### Tasks

1. **Design the security boundary architecture**:
   - Draw a diagram (Mermaid or described in text) showing all components and trust boundaries
   - Label each boundary with the controls it enforces
   - Specify the trust level on each side of every boundary
   - Ensure that no component receives data from a lower-trust source without validation at the boundary

2. **Specify the defense-in-depth strategy for tool execution** (the highest-risk component):
   - Design a multi-layer authorization system for trade execution
   - Specify how tool call parameters are validated before execution
   - Describe how tool results are sanitized before being returned to the LLM
   - Design the human-in-the-loop review process for large trades
   - Explain what happens if any single control fails (fail-closed design)

3. **Design the memory security architecture**:
   - Specify how memory is isolated between users
   - Describe how memory integrity is maintained (preventing corruption)
   - Design a memory auditing system that can detect slow-moving corruption
   - Specify what happens when corrupted memory is detected (quarantine, validation, recovery)

4. **Design the monitoring and incident response system**:
   - Define the key metrics and signals that indicate normal vs. abnormal operation
   - Specify how anomalous behavior is detected (patterns, thresholds, ML-based)
   - Design the incident response workflow for three scenarios:
     - (a) A direct prompt injection is detected at the input boundary
     - (b) An indirect injection is detected through anomalous tool call patterns
     - (c) Memory corruption is detected during a periodic audit
   - For each scenario, specify: detection, containment, investigation, remediation, and post-incident review steps

5. **Analyze the residual risks**:
   - What threats cannot be fully mitigated by your architecture?
   - What are the fundamental limitations of securing LLM applications?
   - How does your architecture reduce (even if it cannot eliminate) these risks?
   - What additional assurances (formal verification, red teaming, etc.) would you recommend?

### Deliverable

`solutions/exercise3.md` — Security architecture document with all five tasks completed.

### Grading Criteria

| Criterion | Points |
|---|---|
| Security boundary diagram is complete, correct, and well-labeled | 4 |
| Tool execution defense-in-depth is thorough with fail-closed design | 4 |
| Memory security addresses isolation, integrity, and auditing | 4 |
| Monitoring and incident response are concrete and actionable | 4 |
| Residual risk analysis is honest and insightful | 4 |
| Architecture demonstrates integration of control-theoretic concepts | 4 |
| Regulatory requirements are fully addressed | 3 |
| Cross-user isolation is properly designed | 3 |
| **Total** | **30** |

---

## Bonus Exercise: Comparative Architecture Analysis (Optional)

**Objective**: Critically evaluate different architectural approaches to securing LLM applications.

Read the following two architectural approaches:

**Approach A — Perimeter-Focused Security**: All security controls are placed at the API layer. Input validation, output filtering, and rate limiting are the primary defenses. The internal components (prompt assembly, retrieval, tool execution, memory) are trusted and communicate without additional validation.

**Approach B — Zero-Trust Internal Architecture**: Every internal boundary has its own security controls. The API layer validates input, but the prompt manager also validates input. The retrieval pipeline classifies its own results. The tool executor validates its own parameters. The memory manager audits its own reads and writes. Output is filtered at every stage, not just at the final boundary.

### Tasks

1. **Compare the two approaches** across the following dimensions:
   - Security effectiveness against direct injection, indirect injection, and memory corruption
   - Performance impact (latency, throughput, cost)
   - Development and maintenance complexity
   - Failure modes (what happens when a control fails?)
   - Observability (how easy is it to detect and diagnose issues?)

2. **Identify the optimal approach** (or hybrid): Is one approach strictly better? Can elements of both be combined? What tradeoffs are acceptable?

3. **Apply the control-theoretic framework**: Which approach better aligns with control-theoretic principles of stability, observability, and controllability? Explain your reasoning.

### Deliverable

`solutions/exercise_bonus.md` — Comparative analysis document.

### Grading Criteria (Bonus)

| Criterion | Points |
|---|---|
| Comparison is thorough and fair to both approaches | 3 |
| Optimal approach (or hybrid) is well-justified | 3 |
| Control-theoretic analysis demonstrates deep understanding | 4 |
| **Total** | **10** (bonus) |

---

## Submission Guidelines

1. Place all solution files in the `solutions/` directory
2. Use Markdown format for all documents
3. Include Mermaid diagrams where appropriate
4. Be specific and concrete — avoid vague statements like "add security" or "validate inputs"
5. Reference the control-theoretic framework and threat model in your analysis

## Total Points

| Exercise | Points |
|---|---|
| Exercise 1 (Easy) | 10 |
| Exercise 2 (Medium) | 15 |
| Exercise 3 (Hard) | 30 |
| Bonus (Optional) | 10 |
| **Total** | **55** (65 with bonus) |
