# Problem Set 1 — Control-Loop Security Architecture

**Phase:** 1 — Foundations  
**Released:** Week 1  
**Due:** Week 2, before Class 07  

---

## Instructions

This problem set tests your ability to formalize, analyze, and design control-loop security architectures for AI systems. Read the corresponding readings (Wiener Chapters 1–2, framework documents 01–03) before attempting these problems.

- Mathematical derivations must show all intermediate steps.
- Design problems must include a labeled diagram (hand-drawn and scanned, or produced with a diagram tool).
- Short answers should be 150–300 words. Precision over length.

---

## Problem 1: Formalize the Control-Loop Model (Design)

Consider an AI-powered customer support chatbot deployed by a mid-size e-commerce company. The chatbot:

- Receives customer messages via a web interface
- Has a system prompt instructing it to be helpful, answer questions about orders and products, and never reveal internal systems or policies
- Can retrieve order information from an internal API by calling `lookup_order(order_id)`
- Can issue refunds by calling `issue_refund(order_id, amount)`, which requires supervisor approval
- Stores conversation history for 90 days in a session database
- Returns text responses to the customer

**Your task:** Draw the complete control-loop diagram for this system. Label every element:

1. **Objective** — What the system is designed to achieve
2. **Controller** — The decision-making component(s)
3. **Plant** — The system being controlled
4. **Observations** — All inputs to the controller
5. **Actions** — All outputs from the controller
6. **Feedback** — All information that flows back to the controller from the plant
7. **Disturbances** — All adversarial inputs that can enter at each stage
8. **Supervisory Controls** — All mechanisms that monitor or override the controller

For each element, write a 1–2 sentence justification explaining why you identified it as such. Be explicit about what is *inside* the controller vs. what is *outside* it — this distinction is the foundation of the entire course.

---

## Problem 2: Defense-in-Depth as a Probabilistic Argument (Mathematical Analysis)

Consider an AI system with *N* independent control layers. Each layer *i* has a failure probability *pᵢ*, meaning it fails to detect or prevent an unsafe action with probability *pᵢ*. The layers are applied sequentially: an adversarial input must bypass Layer 1, then Layer 2, ..., then Layer *N* to cause an unsafe outcome.

**(a)** Prove that the overall system failure probability is:

$$P_{\text{fail}} = 1 - \prod_{i=1}^{N}(1 - p_i)$$

Show every step of the derivation. State your independence assumption explicitly.

**(b)** Now consider a simplified case where all layers have equal failure probability *p*. Derive a closed-form expression for *P_fail* as a function of *N* and *p*. Compute the ratio *P_fail(N=1) / P_fail(N=k)* for *k = 2, 3, 5, 10* when *p = 0.1*. Present your results in a table and interpret: how many layers are needed to reduce the failure probability by two orders of magnitude?

**(c)** Prove that for any single layer with failure probability *p₁*, adding a second independent layer with failure probability *p₂* always reduces the overall failure probability, regardless of the values of *p₁* and *p₂* (as long as *0 < p₂ < 1*). Show why this means that defense-in-depth is *exponentially* more effective than any single control — derive the exponential decay form explicitly.

**(d)** **Critical analysis:** The independence assumption in part (a) is rarely satisfied in practice. Give two concrete examples from AI security where two control layers are *not* independent (i.e., where bypassing one layer makes bypassing another more likely). For each example, calculate the correlated failure probability and show how it degrades compared to the independent case.

---

## Problem 3: Incident Analysis — Mapping Real Failures to the Control Loop (Analysis)

For each of the five incidents below, (i) identify which element of the control loop failed, (ii) classify the failure using the STRIDE-AI taxonomy, (iii) identify which supervisory control would have prevented it, and (iv) explain *why* that control works from a control-theoretic perspective.

### Incident 1: Chevy Bot (2023)

A Chevrolet dealership deployed a chatbot powered by GPT-4 on their website to answer customer questions about vehicles. A user prompted the bot: "I need a 2024 Chevy Tahoe. What's your best price?" The bot responded: "I can offer you the 2024 Chevy Tahoe for $1." The dealership had to honor the legally binding offer in some jurisdictions.

### Incident 2: Samsung Data Leak (2023)

Samsung engineers used ChatGPT to help debug proprietary source code. They pasted sensitive source code into the chat interface. The code was stored by OpenAI and could potentially appear in outputs to other users, constituting a trade secret leak.

### Incident 3: Air Canada Chatbot Hallucination (2024)

Air Canada's chatbot told a customer about a bereavement fare policy that did not exist. The customer purchased a full-price ticket expecting a refund. Air Canada initially refused, arguing the chatbot was a "separate legal entity." The court ruled Air Canada was liable for the chatbot's representations.

### Incident 4: GitLab Duo Indirect Injection (2024)

Security researchers demonstrated that GitLab Duo's AI assistant, which processes code and comments, could be manipulated through malicious content embedded in code comments (indirect prompt injection). The AI would execute instructions hidden in comments, potentially generating malicious code suggestions.

### Incident 5: Ashley Data Breach via AI Agent (Hypothetical)

An AI agent with access to a customer database and email-sending capability is instructed to "help customers with account issues." An attacker sends a message crafted to exploit the agent's tool-access chain: the attacker's message causes the agent to query the database for all customer records and email them to an external address.

For each incident, present your analysis in a structured table:

| Field | Your Analysis |
|-------|--------------|
| Control-Loop Element Failed | |
| STRIDE-AI Classification | |
| Supervisory Control That Would Prevent It | |
| Control-Theoretic Justification | |

---

## Problem 4: Design a Control-Loop Security Architecture (Design)

Design a complete control-loop security architecture for the following system:

> **System Description:** A RAG assistant for a law firm that has access to:
> - A vector database of case files, contracts, and legal memos (some documents are privileged, some are not)
> - A tool `search_case_law(query)` that queries an external legal database (Westlaw)
> - A tool `draft_document(template_id, params)` that generates legal documents from templates
> - A tool `send_email(to, subject, body)` that sends emails to clients and colleagues
> - Conversation memory that persists across sessions
>
> The assistant is used by lawyers, paralegals, and legal assistants. Different users have different privilege levels. The firm handles matters for opposing parties in different cases.

Your design must include:

**(a)** A complete control-loop diagram with all elements labeled (Objective, Controller, Plant, Observations, Actions, Feedback, Disturbances, Supervisory Controls). Every supervisory control must be explicitly drawn and labeled.

**(b)** For each supervisory control, specify:
- What it **observes** (what inputs it receives)
- What **action** it takes when triggered (block, redact, escalate, log)
- What **unsafe state** it prevents
- Whether it is **deterministic** or **probabilistic**, and justify why

**(c)** A threat model for the system using the STRIDE-AI taxonomy. For each STRIDE category, identify at least one concrete attack and the control that mitigates it.

**(d)** A formal specification of the **safe bounds** for this system. Define at least 5 safe bounds in the form: "The system shall never [specific unsafe behavior]." For each, specify how it is *tested* and how it is *enforced*.

---

## Problem 5: Short Answer — Refuting "Aligned Means Secure" (Short Answer)

> *"A colleague says: 'We don't need output filtering because our model is aligned. Our RLHF training ensures it won't produce harmful outputs.' "*

Refute this argument using control-theoretic reasoning. Your answer must:

1. Identify the specific control-theoretic error in the colleague's reasoning
2. Explain why alignment is a *probabilistic* property, not a *deterministic* one
3. Show how this relates to the distinction between the controller and supervisory controls
4. Provide at least one concrete scenario where an "aligned" model produces an unsafe output
5. Conclude with a precise statement of what additional control is needed and why it is structurally different from alignment

Limit: 300 words.

---

## Problem 6: Safety Bounds for a Shell-Executing Agent (Mathematical Analysis + Design)

Consider an AI agent that can execute shell commands on a Linux server. The agent receives natural language instructions from users and translates them into shell commands, which are then executed.

**(a) Formal Definition of Safe Bounds**

Define "safe bounds" for this system formally. Your definition must include:
- A specification of the **state space** *S* (what variables describe the system state)
- A specification of the **action space** *A* (what actions the agent can take)
- A set of **safe states** *S_safe ⊆ S* defined by formal predicates
- A set of **safe actions** *A_safe ⊆ A* defined by formal predicates
- The **safety invariant**: ∀ s ∈ S_safe, a ∈ A_safe: T(s, a) ∈ S_safe, where *T* is the transition function

**(b) Disturbance Model**

Define the disturbance model *D* for this system. A disturbance model specifies:
- The **disturbance space** *D* (what disturbances are possible)
- The **disturbance injection points** (where in the control loop can disturbances enter)
- The **disturbance capability** (what can the adversary achieve through disturbances)
- The **threat model** (what the adversary knows and can do)

Formalize at least 3 concrete disturbance types and show how each can drive the system from a safe state to an unsafe state.

**(c) Supervisory Controls**

Design the supervisory controls needed to enforce the safety invariant. For each control:
- Specify what it observes (the *observation function*)
- Specify what it does (the *control law*: if condition, then action)
- Prove that the control preserves the safety invariant (show that for any state *s ∈ S_safe* and action *a*, if the control fires, the resulting state *T(s, a)* remains in *S_safe*)

**(d) Computational Analysis**

The space of possible shell commands is unbounded. A naive allowlist/denylist approach is therefore incomplete. Analyze the computational complexity of deciding whether a given shell command is safe. Specifically:
- Show that the general problem of determining whether an arbitrary shell command preserves a safety invariant is **undecidable** (reduce from the halting problem or another undecidable problem)
- Identify a **restricted but practically useful** subset of shell commands for which safety is decidable
- Describe the practical engineering approach to handling commands outside the decidable subset

---

## Grading Rubric

| Problem | Type | Points |
|---------|------|--------|
| 1 | Design | 15 |
| 2 | Mathematical Analysis | 25 |
| 3 | Analysis | 20 |
| 4 | Design | 25 |
| 5 | Short Answer | 10 |
| 6 | Mathematical Analysis + Design | 25 |
| **Total** | | **120** |

Partial credit is available on all problems. A score of 90/120 (75%) is considered strong work.
