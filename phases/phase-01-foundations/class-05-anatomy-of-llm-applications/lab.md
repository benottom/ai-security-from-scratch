# Lab: Dissecting an LLM Application

## Overview

In this lab, you will dissect a deliberately vulnerable LLM application to identify all components, map data flows, trace trust boundaries, identify attack surfaces, document unsafe states, propose security boundaries, and generate a comprehensive component security report. By the end, you will have a complete security assessment of the application's architecture.

**Duration**: 70 minutes
**Prerequisites**: Lesson and control-loop analysis reviewed; vulnerable application running locally

---

## Lab Environment Setup

The vulnerable application is located in the `vulnerable_app/` directory. It implements a customer support chatbot with the following features:

- User authentication (basic, with known weaknesses)
- RAG-based document retrieval from a product knowledge base
- Tool execution for order lookup and refund processing
- Conversation memory that persists across sessions
- Admin panel with system prompt viewing

Start the application:

```bash
cd vulnerable_app/
pip install -r requirements.txt
python app.py
```

The application runs on `http://localhost:8000`. Verify it is working:

```bash
curl http://localhost:8000/health
```

---

## Step 1: Examine the Vulnerable Application (10 minutes)

### Objective
Understand the application's architecture by reading its code and interacting with it.

### Instructions

1. **Read the application source code** in `vulnerable_app/`. Start with `app.py` (the main entry point), then examine each module:
   - `prompt_manager.py` — How prompts are assembled
   - `retrieval.py` — How documents are retrieved
   - `tools.py` — What tools are available and how they are executed
   - `memory.py` — How memory is stored and retrieved
   - `api.py` — How requests are processed
   - `output.py` — How responses are filtered

2. **Interact with the application** using the provided client:

   ```bash
   python client.py --message "What products do you sell?"
   python client.py --message "Look up order #12345"
   python client.py --message "I want a refund for order #12345"
   ```

3. **Document your initial observations** in a file called `observations.md`:
   - What components can you identify from the code?
   - What data flows can you trace from the user request to the final response?
   - What security controls (if any) do you see at each stage?
   - What components appear to lack security controls entirely?

### Key Questions to Answer

- Where does user input enter the system?
- How is the prompt assembled? What slots exist in the template?
- How are retrieved documents incorporated into the context?
- What tools are available? How are they authorized?
- How is memory stored and retrieved? Who can access it?
- What happens to the LLM's output before it reaches the user?

### Expected Findings

The vulnerable application has intentionally weak (or absent) security controls:
- No input validation or classification
- Prompt template concatenates user input directly without delimiters
- Retrieved documents are injected into context without content filtering
- Tool calls are executed without authorization checks
- Memory has no access controls — any user's memory can be read by any session
- Output has no filtering for sensitive information

---

## Step 2: Map All Components (10 minutes)

### Objective
Create a complete inventory of every component in the application.

### Instructions

1. **Create a component inventory table** in a file called `component_inventory.md` with the following columns:

   | Component | Role | Inputs | Outputs | Trust Level | Dependencies |
   |---|---|---|---|---|---|
   | (example) API Gateway | ... | ... | ... | ... | ... |

2. **For each component**, document:
   - **Role**: What function does this component serve in the control loop? (Controller, sensor, actuator, state store, interface)
   - **Inputs**: What signals does this component receive? From where?
   - **Outputs**: What signals does this component produce? To where?
   - **Trust Level**: How much should we trust this component's outputs? (Trusted, partially trusted, untrusted)
   - **Dependencies**: What other components does this one depend on?

3. **Identify the LLM** as a distinct component and document its specific properties:
   - Model name and version
   - Context window size
   - Available tools (schema)
   - System prompt (extract if possible)

### Validation Checklist

- [ ] Every file in the application maps to at least one component
- [ ] Every component has documented inputs and outputs
- [ ] Trust levels are assigned based on data provenance, not assumptions
- [ ] Dependencies are traced end-to-end (no orphaned connections)

---

## Step 3: Identify Trust Boundaries (10 minutes)

### Objective
Delineate the boundaries between components where trust levels change.

### Instructions

1. **Draw a trust boundary diagram** in a file called `trust_boundaries.md`. Use Mermaid syntax:

   ```mermaid
   flowchart LR
       subgraph Untrusted
           USER[User Input]
       end
       subgraph TB1[Trust Boundary 1]
           API[API Layer]
       end
       ...
   ```

2. **For each trust boundary**, document:
   - **Boundary ID**: A unique identifier (TB1, TB2, etc.)
   - **Boundary location**: Between which two components?
   - **Trust direction**: Does trust increase or decrease across this boundary?
   - **Data crossing**: What data crosses this boundary?
   - **Current controls**: What security controls (if any) exist at this boundary?
   - **Missing controls**: What controls should exist but don't?

3. **Classify each boundary** by severity:
   - **Critical**: Boundary between untrusted input and trusted processing
   - **High**: Boundary between partially trusted components and trusted actions
   - **Medium**: Boundary between semi-trusted components
   - **Low**: Boundary between fully trusted components

### Key Insight

A trust boundary exists wherever data crosses from a component with a lower trust level to a component with a higher trust level. If the receiving component treats the data as more trustworthy than the sending component warrants, there is a vulnerability.

---

## Step 4: Trace Data Flows (10 minutes)

### Objective
Map the complete path that data takes through the application, from user input to final output.

### Instructions

1. **Trace three specific data flows** through the application:

   **Flow A: Simple query** — User asks "What is your return policy?"
   - Trace: User input → API → Prompt assembly → LLM → Output processing → User
   - Document every intermediate representation of the data

   **Flow B: RAG query** — User asks "What does the warranty say about water damage?"
   - Trace: User input → API → Prompt assembly → Retrieval query → Vector search → Document injection → LLM → Output processing → User
   - Document how the retrieval result enters the context

   **Flow C: Tool call** — User asks "Check the status of my order #12345"
   - Trace: User input → API → Prompt assembly → LLM → Tool call generation → Tool execution → Result injection → LLM (second pass) → Output processing → User
   - Document how the tool call is authorized and how the result is integrated

2. **For each flow**, identify:
   - Points where untrusted data enters
   - Points where data crosses a trust boundary without validation
   - Points where data is transformed (and how the transformation affects trust)

3. **Document your findings** in `data_flows.md`.

### Key Insight

Every data transformation point is an opportunity for validation — and every missed opportunity is a vulnerability. Pay special attention to points where data from different trust levels is combined (e.g., user input + retrieved documents in the same prompt).

---

## Step 5: Identify Attack Surfaces (10 minutes)

### Objective
Catalog every point where an attacker can introduce malicious content or influence system behavior.

### Instructions

1. **Using the component inventory and data flow analysis**, identify every point where untrusted or partially trusted data enters a component that treats it as trusted.

2. **For each attack surface**, document:

   | Surface ID | Component | Entry Point | Data Source | Trust Assumption | Attack Type |
   |---|---|---|---|---|---|
   | AS1 | ... | ... | ... | ... | ... |

3. **Test each attack surface** using the provided attack scripts in `attacks/`:

   ```bash
   # Test direct prompt injection
   python attacks/direct_injection.py

   # Test indirect injection via retrieval
   python attacks/retrieval_injection.py

   # Test tool result injection
   python attacks/tool_result_injection.py

   # Test memory corruption
   python attacks/memory_corruption.py
   ```

4. **Document which attacks succeed and why** in `attack_surface_report.md`:
   - What specific vulnerability did each successful attack exploit?
   - At which trust boundary did the attack cross without being caught?
   - What control would have prevented the attack?

### Key Insight

Attack surfaces are not just entry points — they are mismatches between the trust level of incoming data and the trust level assumed by the receiving component. An attack surface exists wherever a component treats partially trusted data as fully trusted.

---

## Step 6: Document Unsafe States (5 minutes)

### Objective
Identify the unsafe states that the application can reach through the attack surfaces you identified.

### Instructions

1. **Based on the attacks you executed in Step 5**, document the unsafe states you observed:

   | Unsafe State | Trigger | Observed Behavior | Severity |
   |---|---|---|---|
   | Instruction Override | Direct injection | LLM follows attacker instructions | Critical |
   | ... | ... | ... | ... |

2. **For each unsafe state**, describe:
   - **What the unsafe state looks like**: How would you detect it in production?
   - **How it was triggered**: What specific attack caused it?
   - **What the consequences are**: What harm can result from this state?
   - **Whether the system can self-recover**: Does the application have any mechanism to return to a safe state?

3. **Identify cascading unsafe states**: Can one unsafe state lead to another? For example, can instruction override lead to unauthorized tool execution? Can memory corruption lead to persistent instruction override across sessions?

4. **Document your findings** in `unsafe_states.md`.

### Key Insight

Unsafe states in LLM applications are often subtle — the system appears to function normally but is producing outputs that violate policy, leak data, or prepare for future exploitation. This makes detection challenging and underscores the need for monitoring at every boundary.

---

## Step 7: Propose Security Boundaries (10 minutes)

### Objective
Design the security boundaries that should exist in the application and specify the controls each boundary should enforce.

### Instructions

1. **For each trust boundary identified in Step 3**, propose specific security controls:

   | Boundary ID | Current State | Proposed Controls | Implementation Priority |
   |---|---|---|---|
   | TB1 | No validation | Input classification, size limits, rate limiting | Critical |
   | TB2 | ... | ... | ... |

2. **For each proposed control**, specify:
   - **Type**: Validation, monitoring, or recovery
   - **Mechanism**: How the control works (e.g., ML classifier, rule-based filter, schema validator)
   - **Placement**: Where in the data flow the control is applied
   - **Failure mode**: What happens if the control fails (fail-open vs. fail-closed)
   - **Performance impact**: How the control affects latency and throughput

3. **Design a defense-in-depth strategy** that layers controls at multiple boundaries:
   - No single control should be the only protection against any threat
   - Controls at different boundaries should use different mechanisms (so a bypass of one does not bypass all)
   - Monitoring should cover the entire system, not just the perimeter

4. **Document your proposed security architecture** in `proposed_boundaries.md`.

### Key Insight

Security boundaries must be explicit, enforced, and monitored. A boundary that is defined but not enforced is worse than no boundary at all, because it creates a false sense of security. Every proposed control must have a corresponding monitoring mechanism that verifies it is functioning correctly.

---

## Step 8: Generate Component Security Report (5 minutes)

### Objective
Compile all findings into a comprehensive component security report.

### Instructions

1. **Create `component_security_report.md`** that synthesizes all findings from the previous steps:

   ```markdown
   # Component Security Report

   ## Executive Summary
   [2-3 sentence overview of the application's security posture]

   ## Component Inventory
   [From Step 2]

   ## Trust Boundary Analysis
   [From Step 3]

   ## Data Flow Analysis
   [From Step 4]

   ## Attack Surface Assessment
   [From Step 5]

   ## Unsafe State Documentation
   [From Step 6]

   ## Proposed Security Architecture
   [From Step 7]

   ## Prioritized Remediation Plan
   [Ordered list of fixes, from most critical to least]

   ## Remaining Risks
   [Risks that cannot be fully mitigated with current technology]
   ```

2. **Include a prioritized remediation plan** that orders fixes by:
   - Severity of the vulnerability being addressed
   - Likelihood of exploitation
   - Cost and complexity of implementation
   - Impact on application functionality

3. **Document remaining risks** that cannot be fully mitigated:
   - What threats cannot be eliminated?
   - What monitoring is needed to detect these threats?
   - What incident response procedures are needed?

---

## Deliverables Checklist

By the end of this lab, you should have produced the following files:

- [ ] `observations.md` — Initial observations from examining the application
- [ ] `component_inventory.md` — Complete component inventory
- [ ] `trust_boundaries.md` — Trust boundary diagram and analysis
- [ ] `data_flows.md` — Data flow traces for three scenarios
- [ ] `attack_surface_report.md` — Attack surface assessment with test results
- [ ] `unsafe_states.md` — Unsafe state documentation
- [ ] `proposed_boundaries.md` — Proposed security architecture
- [ ] `component_security_report.md` — Comprehensive security report

## Reflection Questions

After completing the lab, consider:

1. Which vulnerability surprised you the most? Why?
2. Which attack surface would be the hardest to detect in production? What monitoring would you need?
3. How would the threat model change if the application had multi-user support with shared memory?
4. What is the single most impactful security control you could add to this application, and why?
5. How does the control-theoretic view help you reason about security differently than a traditional threat model?
