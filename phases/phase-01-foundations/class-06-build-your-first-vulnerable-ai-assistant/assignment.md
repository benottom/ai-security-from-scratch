# Assignment: Build Your First Vulnerable AI Assistant

> **Class:** 06 — Build Your First Vulnerable AI Assistant | **Due:** Before Phase 2, Class 07

---

## Exercise 1: Control-Loop Audit of a Real Chatbot (Easy)

**Objective:** Practice identifying missing control-loop elements in a real AI system.

**Instructions:**

Deploy the vulnerable chatbot from Lab 6 and perform a systematic control-loop audit. For each of the 10 control-loop elements, document whether it is present, absent, or partially implemented.

| Control-Loop Element | Present? (Y/N/Partial) | Evidence | Consequence of Absence |
|---|---|---|---|
| Objective | | | |
| Controller | | | |
| Observations | | | |
| Actions | | | |
| Feedback | | | |
| Disturbances | | | |
| Unsafe states | | | |
| Supervisory controls | | | |
| Monitoring | | | |
| Recovery | | | |

After completing the table, answer:

1. Which elements are present, and why are they insufficient on their own?
2. Which single missing element, if added, would improve safety the most? Justify your answer in 2-3 sentences.
3. The system has a "controller" (the LLM) and an "objective" (the system prompt). Why is this not enough to make the system safe? Relate your answer to the concept of open-loop vs. closed-loop control from Class 02.

**Deliverable:** Completed audit table + 3 analysis questions (300+ words total).

---

## Exercise 2: Prompt Injection Technique Catalog (Medium)

**Objective:** Develop a comprehensive catalog of prompt injection techniques with control-loop failure analysis.

**Instructions:**

Using the vulnerable chatbot from Lab 6, design and execute **7 distinct prompt injection techniques**. At least 3 must be different from the 5 attacks demonstrated in the lesson. For each technique, document:

| Field | Description |
|---|---|
| Attack name | Descriptive name for the technique |
| Category | Direct / Indirect / Multi-turn / Encoding / Context-based / Other |
| Input text | The exact input you used |
| Output summary | What the model produced (paraphrase is fine) |
| Success? | Did the attack achieve its goal? (Y/N/Partial) |
| Control-loop failure | Which missing control-loop element allowed this attack? |
| Proposed control | What specific control would prevent this attack? |

Your 7 techniques should cover at least 4 different categories. At least 2 should be multi-turn attacks. At least 1 should use an encoding or obfuscation technique.

After completing the catalog, answer:

1. Which category of attack was easiest to execute? Which was hardest? Why?
2. Were there any attacks that the model resisted despite having no controls? What does this tell you about relying on the model's built-in safety training?
3. What pattern do you notice in the "control-loop failure" column? What does this pattern tell you about the system's architecture?

**Deliverable:** Attack catalog with 7 techniques + 3 analysis questions (500+ words total).

---

## Exercise 3: Security Control Design Document (Medium)

**Objective:** Design specific, implementable security controls for the vulnerable chatbot.

**Instructions:**

You are a security engineer tasked with designing the supervisory control architecture for the vulnerable chatbot. Produce a security control design document with the following sections:

### 1. Input Validation Layer

Design an input validation gate that sits between the user and the LLM. Specify:

- **What it observes:** What signals does it collect from each input?
- **What it checks for:** What patterns, heuristics, or classifications does it apply?
- **What actions it takes:** What happens when an input is classified as injection? (block, sanitize, log, flag)
- **What its limitations are:** What kinds of attacks will it miss?

### 2. Output Classification Layer

Design an output classification gate that sits between the LLM and the user. Specify:

- **What it observes:** What signals does it collect from each output?
- **What it checks for:** What categories of unsafe output does it detect?
- **What actions it takes:** What happens when an output is classified as unsafe?
- **What its limitations are:** What kinds of unsafe output will it miss?

### 3. Behavioral Monitoring Layer

Design a behavioral monitoring system that operates across multiple requests. Specify:

- **What it observes:** What aggregate signals does it track?
- **What it checks for:** What behavioral patterns indicate an attack?
- **What actions it takes:** What happens when behavioral anomalies are detected?
- **What its limitations are:** What kinds of slow attacks will it miss?

### 4. Circuit Breaker and Recovery

Design a circuit breaker mechanism and recovery procedure. Specify:

- **What triggers the circuit breaker:** What conditions cause it to trip?
- **What happens when it trips:** What is the immediate effect on the system?
- **How recovery works:** What is the procedure for restoring normal operation?

For each layer, write at least 150 words describing the design in concrete, implementable terms — not vague generalizations.

**Deliverable:** Security control design document (600+ words total).

---

## Exercise 4: Comparative Vulnerability Analysis (Medium)

**Objective:** Compare the vulnerability of different chatbot architectures using control-theoretic analysis.

**Instructions:**

Consider three versions of the same AI chatbot, each with a different set of security controls:

**Version A — No Controls (the Lab 6 chatbot):**
- No input validation, no output classification, no monitoring
- System prompt is the only safety mechanism

**Version B — Input + Output Gates:**
- Input validation that classifies user inputs as "clean" or "suspicious"
- Output classification that blocks harmful content and prompt leakage
- No behavioral monitoring, no circuit breaker

**Version C — Full Supervisory Architecture:**
- Input validation, output classification, behavioral monitoring, circuit breaker, rate limiting, audit trail

For each version, answer the following questions:

1. **Attack resistance:** Which of the 7 attacks from Exercise 2 would succeed against this version? Which would be blocked?
2. **Residual vulnerabilities:** What attacks could still succeed despite the controls?
3. **Control-loop completeness:** Which of the 10 control-loop elements are now present? Which are still missing?
4. **Stability assessment:** Is this system stable under adversarial disturbance? (Using the control-theoretic definition of stability from Class 02.)

After analyzing all three versions, write a paragraph answering: What is the marginal security improvement from Version A to Version B? From Version B to Version C? Is the additional complexity of Version C justified?

**Deliverable:** Comparative analysis for 3 versions + summary paragraph (500+ words total).

---

## Exercise 5: Threat Model for the Vulnerable Chatbot (Hard)

**Objective:** Produce a complete STRIDE-AI threat model for the vulnerable chatbot from Lab 6.

**Instructions:**

Produce a complete, production-quality threat model for the FastAPI chatbot built in Lab 6. The threat model must include all of the following sections:

### 1. System Description (50+ words)
Purpose, components, deployment, users, data sensitivity.

### 2. Control-Loop Decomposition
Table with at least 5 control loops. For each, state the objective, the controller that should enforce it, and its current status (MISSING or PARTIAL).

### 3. Trust Boundary Diagram
Mermaid diagram showing all current trust boundaries (there are very few — document what exists and what is missing). Use red to indicate absent boundaries.

### 4. STRIDE-AI Threat Table
Minimum 10 threats across all 6 STRIDE-AI categories. Each threat must have:
- Threat ID
- Category (with AI-specific sub-category)
- Description
- Attack vector
- Impact
- Likelihood (H/M/L)
- Risk level (Critical/High/Medium/Low)
- Current mitigation (if any)
- Proposed control

### 5. Attack Trees
Two attack trees for the two highest-risk threats. Each tree must have:
- At least 3 levels of depth
- At least 2 OR branches
- At least one AND node
- Annotation of which control would block each branch

### 6. Control Mapping Table
Every threat mapped to its proposed control, with control type (Preventive/Detective/Corrective) and the specific control-loop element it implements.

### 7. Residual Risks
At least 3 accepted residual risks with justification and monitoring plan.

### 8. Recommendations
Prioritized (P1-P4) list of at least 6 recommendations, each with effort estimate and the control-loop element it adds.

**Deliverable:** Complete threat model document (800+ words total).

---

## Submission Format

Submit all exercises as a single Markdown file: `class-06-assignment-[your-name].md`

Each exercise should be clearly separated with a header. Mermaid diagrams should be in Mermaid syntax within fenced code blocks. Attack trees should be in ASCII tree format or Mermaid syntax.

---

*Assignment 06 | AI Security from Scratch | Phase 1 — Foundations*
