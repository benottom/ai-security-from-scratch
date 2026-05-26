# Assignment: AI Security as an Engineering Discipline

> **Class:** 01 — AI Security as an Engineering Discipline | **Due:** Before Class 02

---

## Exercise 1: Control-Theory Analogy Mapping (Easy)

**Objective:** Demonstrate understanding of the mapping between control-theory concepts and AI security.

**Instructions:**

Complete the following table by providing a specific AI security example for each control-theory concept. Each example must be concrete and realistic — not generic.

| Control-Theory Concept | Definition | AI Security Example |
|---|---|---|
| Sensor failure | The measurement system provides incorrect data to the controller | |
| Controller compromise | The decision-making component is influenced by an attacker | |
| Actuator failure | The output mechanism executes an unintended action | |
| Feedback corruption | The return path carries manipulated information | |
| Disturbance rejection | The system maintains its objective despite external perturbation | |

For each example, write 2-3 sentences explaining:
1. What specifically happens in the AI system
2. What the unsafe state would be
3. What supervisory control could prevent it

**Deliverable:** Completed table with explanations (200+ words total).

---

## Exercise 2: Open-Loop vs. Closed-Loop Analysis (Medium)

**Objective:** Analyze the difference between an AI system operating as an open-loop controller versus a closed-loop controller with respect to safety.

**Instructions:**

Consider a customer support chatbot for a bank. The chatbot answers questions about account balances, recent transactions, and bank services. It has access to a tool that can look up account information.

**Part A: Open-Loop Analysis**

Describe the chatbot's operation as an open-loop system (no supervisory controls). Identify:
1. The safety objective(s)
2. What disturbances could occur
3. What unsafe states could result
4. Why the system cannot detect or recover from violations

**Part B: Closed-Loop Design**

Design a closed-loop version of the same chatbot. Specify:
1. What observations the supervisory controller would need
2. What actions the supervisory controller could take
3. The feedback mechanism that would close the loop
4. How the system would detect and recover from violations

**Part C: Comparison**

Write a 150+ word analysis comparing the two designs. Address: Why is the open-loop design unsafe even if the model is "well-aligned"? What specific failure modes does the closed-loop design prevent that the open-loop design cannot?

**Deliverable:** Written analysis (400+ words total across all three parts).

---

## Exercise 3: "Secure the Model" vs. "Secure the Control Loop" Debate (Medium)

**Objective:** Articulate why model-level security is necessary but insufficient, and why system-level security is required.

**Instructions:**

A colleague argues: "We don't need all these supervisory controls. We just need to use a better model — one that's more aligned and more resistant to prompt injection. GPT-5 will solve this."

Write a structured rebuttal (300+ words) that:

1. **Acknowledges the partial truth** — Explain why model alignment and robustness are valuable and should be pursued.
2. **Identifies the fundamental limitation** — Explain why even a perfectly aligned model is insufficient when deployed in an insecure control loop. Use at least two concrete examples of attacks that bypass the model entirely (e.g., targeting the observation pipeline or the actuation pipeline).
3. **Argues for the control-loop approach** — Explain why supervisory controls are necessary regardless of model quality. Use the control-theoretic concept of disturbance rejection to support your argument.
4. **Proposes a synthesis** — Describe how model alignment and supervisory controls work together in a layered defense. Explain why neither alone is sufficient but together they provide robust security.

Your rebuttal should demonstrate understanding of control theory concepts without requiring the reader to be a control theory expert.

**Deliverable:** Written rebuttal (300+ words).

---

## Exercise 4: Design a Supervisory Control for a Specific Threat (Hard)

**Objective:** Apply the control-loop model to design a specific supervisory control for a concrete threat.

**Instructions:**

You are building an AI assistant that helps employees search internal company documents using RAG. The system retrieves documents from a vector database and uses an LLM to answer questions based on the retrieved content.

**Threat:** An attacker with write access to the document store (e.g., a compromised employee account) inserts a document that contains hidden instructions. When a user asks a question that triggers retrieval of this document, the hidden instructions override the system prompt and cause the assistant to exfiltrate data.

Design a supervisory control to mitigate this threat. Your design must include:

1. **Control objective** — What specific safety property must be maintained?
2. **Observation** — What does the supervisory control need to observe? Where in the pipeline does it observe?
3. **Decision logic** — How does it determine whether the observation indicates a threat? Be specific about the detection criteria.
4. **Action** — What does it do when a threat is detected? What does it do when no threat is detected?
5. **Feedback** — How does the control learn from its decisions to improve over time?
6. **Limitations** — What attacks does this control NOT prevent? What are its blind spots?

Draw a simple diagram (ASCII or describe in text) showing where the supervisory control sits in the control loop.

**Deliverable:** Complete supervisory control design with diagram (400+ words).

---

## Exercise 5: Threat Model an AI System You Use (Hard)

**Objective:** Apply the control-loop threat model to a real-world AI system.

**Instructions:**

Choose an AI system you interact with regularly (e.g., GitHub Copilot, ChatGPT with browsing, an AI-powered email assistant, a customer service chatbot). Apply the control-loop threat model to it:

1. **System description** — What does the system do? What components does it have?
2. **Control-loop decomposition** — Identify the controller, observations, actions, feedback, and disturbances.
3. **Trust boundaries** — Where are the trust boundaries? What crosses them?
4. **Top 3 threats** — Using the control-loop threat taxonomy (controller compromise, observation corruption, unsafe actuation, feedback manipulation, disturbance amplification), identify the three most significant threats.
5. **Missing controls** — Based on publicly available information, what supervisory controls appear to be in place? What appears to be missing?
6. **Recommendations** — What supervisory controls would you add? Prioritize them.

**Deliverable:** Written threat model analysis (500+ words).

---

## Submission Format

Submit all exercises as a single Markdown file: `class-01-assignment-[your-name].md`

Each exercise should be clearly separated with a header. Code examples should be in fenced code blocks. Diagrams should be in ASCII art or Mermaid syntax.

---

*Assignment 01 | AI Security from Scratch | Phase 1 — Foundations*
