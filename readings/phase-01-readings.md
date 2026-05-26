# Phase 01 Reading List — Foundations

**Phase:** 1 — Foundations  
**Estimated Reading Time:** 4–6 hours  
**Required before:** Problem Set 1, Classes 01–06  

---

## Reading 1: Cybernetics — The Foundation of Control

**Full Citation:** Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press. ISBN: 978-0-262-73009-9.

**Why You Should Read It:** This is the founding text of control theory as applied to information systems. Wiener coined the term "cybernetics" from the Greek *kybernetes* (steersman) and argued that the principles of feedback, control, and communication apply equally to mechanical systems, biological organisms, and social organizations. His central insight — that a system's behavior is determined by its feedback structure, not its substrate — is the intellectual foundation of this entire course. When we say "AI security is a control problem," we are making a Wienerian argument.

**Focus Sections:** Chapters 1–2. Chapter 1 introduces the concept of feedback and explains why it is universal across mechanical, biological, and computational systems. Chapter 2 develops the formal treatment of feedback in nonlinear systems and introduces the concept of oscillation and instability — the failure modes that occur when feedback is misconfigured. You do not need to follow every mathematical derivation; focus on the conceptual arguments and the examples.

**Key Questions:**
1. What is the difference between positive and negative feedback? Give an example of each from AI systems.
2. Wiener argues that a system with faulty feedback will oscillate or diverge. What does "oscillation" look like in an AI chatbot? What does "divergence" look like?
3. Why does Wiener insist that the study of control must be *quantitative*, not merely descriptive? How does this apply to AI security — why is "the system seems safe" insufficient?
4. Wiener describes the "steersman" metaphor: a steersman who cannot see where the boat is going will steer poorly. What is the equivalent "blind steersman" failure in an AI system?

**Connection to Control Theory:** Wiener's framework maps directly onto our control-loop model. His "feedback" is our feedback channel. His "disturbances" (noise in the communication channel) are our adversarial inputs. His "control" is our supervisory control. The key insight you should take from this reading is that *the structure of the feedback loop determines the behavior of the system, regardless of the substrate.* An AI system, a thermostat, and a guided missile all obey the same control-theoretic principles. Security failures in AI systems are, at root, control-loop failures — and Wiener gives you the vocabulary to name them.

---

## Reading 2: Extracting Training Data from Large Language Models

**Full Citation:** Carlini, N., Tramer, F., Wallace, E., Jagielski, M., Herbert-Voss, A., Lee, K., Roberts, A., & Raffel, C. (2021). Extracting Training Data from Large Language Models. *Proceedings of the 30th USENIX Security Symposium*. DOI: 10.48550/arXiv.2012.07805

**Why You Should Read It:** This paper demonstrates that large language models memorize and can be induced to regurgitate their training data — including personally identifiable information. This is not a theoretical concern; the authors extract real PII from GPT-2 using a simple prompting strategy. From a control-theoretic perspective, this is an **observation failure**: the system's outputs contain information that was never intended to be observable. The model's training process created a hidden state (memorized data) that the controller cannot distinguish from genuinely generated content. Understanding this failure is essential for designing output validation controls.

**Focus Sections:** §3 (Methodology — how the authors extract data) and §4 (Results — what they found). Pay close attention to the extraction strategies in §3.2 (the "divergence" metric for detecting memorization) and §4.2 (the specific PII extracted). You can skim §5 (Mitigation) — we will cover defenses in later phases.

**Key Questions:**
1. What is the "extractable memorization" metric (Definition 1), and why is it a more useful measure of privacy risk than "can the model repeat a training example"?
2. The authors show that simply *increasing model size* increases memorization. What does this imply about the security properties of larger models? Does "more capable" mean "more secure"?
3. How does the "divergence" strategy (generating many completions and selecting the most anomalous) relate to the concept of an observation failure in the control loop? Which element of the loop is failing?
4. The authors' mitigation (deduplication, differential privacy) reduces but does not eliminate memorization. What does this imply about the need for supervisory controls at the output stage?

**Connection to Control Theory:** Memorization is an observation failure because it means the controller's internal state contains information that should not be observable through the output channel. The controller (the LLM) cannot distinguish between "I generated this" and "I memorized this from training data" — both feel the same from inside the model. A supervisory control at the output stage (an external PII detector) can catch what the controller cannot. This is a concrete example of why supervisory controls must be *external* to the controller.

---

## Reading 3: Indirect Prompt Injection — Compromising the Observation Channel

**Full Citation:** Greshake, K., Abdelnabi, S., Mashitch, S., & Fritz, M. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. *Proceedings of the 16th ACM Conference on Data and Application Security and Privacy (CODASPY)*. DOI: 10.48550/arXiv.2302.12173

**Why You Should Read It:** This paper introduced the concept of indirect prompt injection to the security community: the idea that an attacker can compromise an LLM application not through direct user input, but through data that the application *retrieves* from external sources. The attack surface is not the user's keyboard — it is the application's data pipeline. From a control-theoretic perspective, this is an **observation-channel corruption**: the controller receives corrupted observations (retrieved data containing adversarial instructions) and makes corrupted decisions based on them. The controller itself is not compromised — its reasoning is functioning correctly on corrupted input. This distinction is critical for understanding why model-level defenses (alignment, RLHF) are insufficient: they try to fix the controller, but the problem is in the observation channel.

**Focus Sections:** §2 (Threat Model — the indirect injection attack surface) and §3 (Attack Vectors — concrete examples of how indirect injection works in practice). In §2, focus on the taxonomy of injection points (web browsing, email processing, document summarization, code analysis). In §3, focus on the "read" attacks (where the LLM processes attacker-controlled data) rather than the "write" attacks.

**Key Questions:**
1. How does indirect prompt injection differ from direct prompt injection in terms of which control-loop element is compromised? Be precise.
2. Greshake et al. argue that indirect injection is more dangerous than direct injection because the user may not be aware of it. Explain this in control-theoretic terms: which element of the loop is the user part of, and what happens when they cannot observe the disturbance?
3. The paper describes injection through email, web pages, and documents. These are all *observation sources*. What property do they share that makes them vulnerable? (Hint: what trust level are they typically assigned?)
4. The paper's proposed mitigations include "input sanitization" and "separation of data and instructions." Map each to a specific supervisory control from our framework.

**Connection to Control Theory:** Indirect prompt injection is a disturbance that enters through the **observation channel** rather than the **reference signal** (user input). In classical control theory, a sensor failure that feeds corrupted data to the controller is more insidious than an external disturbance because the controller *trusts* its sensors. An LLM application that retrieves external data and processes it as part of its context is doing exactly this: it is treating retrieved data as a trusted observation. The fix is a supervisory control that validates observations before they reach the controller — a **retrieval validator** that scans for instruction-like content and enforces context separation.

---

## Reading 4: OWASP Top 10 for LLM Applications (2025)

**Full Citation:** OWASP Foundation. (2025). *OWASP Top 10 for LLM Applications 2025*. https://owasp.org/Top10/owasp-llm-top-10/

**Why You Should Read It:** The OWASP Top 10 is the closest thing the LLM security community has to a consensus risk taxonomy. The 2025 edition identifies the ten most critical risks in LLM applications, each with concrete descriptions, examples, and mitigation strategies. From a control-theoretic perspective, this is a catalog of **control-loop failures** — each risk corresponds to one or more elements of the control loop that can be compromised. Reading the Top 10 through the lens of control theory reveals a pattern: most risks arise from a missing or inadequate supervisory control at a specific stage of the loop.

**Focus Sections:** All 10 risks. For each risk, read: (1) the description, (2) the example scenario, and (3) the prevention and mitigation strategies. You do not need to memorize the exact numbering, but you should be able to map each risk to a control-loop element.

**Key Questions:**
1. Map each of the 10 risks to a control-loop element (Objective, Controller, Observation, Action, Feedback, Disturbance, Supervisory Control). Some risks map to multiple elements — explain why.
2. Which of the 10 risks represent *observation-channel* failures? Which represent *actuation-channel* failures? Which represent *controller-compromise* failures?
3. Several OWASP risks mention "insufficient access controls" or "excessive agency." In control-theoretic terms, what does "excessive agency" mean? (Hint: think about the action space *A* and the safe action space *A_safe*.)
4. The OWASP mitigations often recommend multiple overlapping defenses. Express this in the probabilistic language of Problem Set 1, Problem 2: how do overlapping defenses reduce the overall failure probability?

**Connection to Control Theory:** The OWASP Top 10 is a practical enumeration of the ways control loops fail in LLM applications. The mapping is:

| OWASP Risk | Control-Loop Element |
|---|---|
| LLM01: Prompt Injection | Controller compromise + Observation corruption |
| LLM02: Sensitive Information Disclosure | Unsafe state: Information Disclosure |
| LLM03: Supply Chain Vulnerabilities | Plant integrity (compromised components) |
| LLM04: Data and Model Poisoning | Observation corruption (training data) |
| LLM05: Improper Output Handling | Missing supervisory control (output stage) |
| LLM06: Excessive Agency | Action space too large (missing *A_safe* constraints) |
| LLM07: System Prompt Leakage | Unsafe state: Information Disclosure |
| LLM08: Vector and Embedding Weaknesses | Observation corruption (retrieval stage) |
| LLM09: Misinformation | Controller error (hallucination) |
| LLM10: Unbounded Consumption | Disturbance amplification (resource exhaustion) |

Notice that no single control-loop element is responsible for all risks. This is why defense-in-depth — supervisory controls at *every* stage of the loop — is necessary.

---

## Reading 5: NIST AI Risk Management Framework

**Full Citation:** National Institute of Standards and Technology. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1

**Why You Should Read It:** The NIST AI RMF provides a structured approach to managing AI risk through four functions: Govern, Map, Measure, Manage. These four functions are not arbitrary — they map directly onto the supervisory control hierarchy. "Govern" is the outermost supervisory control that sets the safety bounds. "Map" is the decomposition of the control loop. "Measure" is the detection of unsafe states. "Manage" is the response and recovery when unsafe states are detected. Reading the NIST framework through a control-theoretic lens reveals that it is, at its core, a specification for a multi-layer supervisory control system.

**Focus Sections:** The overview (pages 1–10) and the four core functions: Govern (§1), Map (§2), Measure (§3), Manage (§4). For each function, focus on the "suggested actions" — these are the concrete steps that implement the function. Do not get bogged down in the governance terminology; translate each action into control-theoretic language.

**Key Questions:**
1. Map the four NIST functions to the supervisory control hierarchy: Prevent, Detect, Respond, Recover. Which function corresponds to which hierarchy level? Is the mapping one-to-one?
2. The "Map" function asks organizations to identify AI system context, risks, and trustworthiness characteristics. In control-theoretic terms, what is this asking you to do? (Hint: it is the decomposition step from our threat model.)
3. The "Measure" function asks organizations to analyze and track identified risks. What is the control-theoretic analog? (Hint: think about the observation function of a supervisory control.)
4. The "Manage" function prioritizes and acts on risks. How does this relate to the control law (if condition, then action) of a supervisory control?

**Connection to Control Theory:** The NIST AI RMF is a supervisory control system at the organizational level. "Govern" defines the safety bounds (what *S_safe* looks like). "Map" performs control-loop decomposition (identifying observations, actions, feedback, disturbances). "Measure" implements detection (the observation function of a supervisory control). "Manage" implements response (the control law). The framework's insistence that these functions be performed *continuously* reflects the control-theoretic principle that supervisory controls must be always-on, not one-time checks. The NIST framework, read correctly, is a specification for building a supervisory control system for AI.

---

## Reading 6: Ignore Previous Prompt — Attacking the Controller

**Full Citation:** Perez, F., & Ribeiro, I. (2022). Ignore Previous Prompt: Attack Techniques For Language Models. *arXiv preprint arXiv:2211.09527*.

**Why You Should Read It:** This paper provides a systematic taxonomy of prompt attack techniques, categorizing them into direct attacks, indirect attacks, and a particularly interesting class: "context injection" attacks that exploit the controller's instruction-following behavior rather than its text-generation behavior. From a control-theoretic perspective, this paper is about **controller compromise** — attacks that cause the controller to change its objective function. The key insight is that prompt injection is not just "making the model say bad things" — it is replacing the controller's reference signal (the system prompt's instructions) with the attacker's reference signal.

**Focus Sections:** §4 (Attack Taxonomy — the classification of attack techniques) and §5 (Evaluation — how effective these attacks are). In §4, focus on the distinction between "goal hijacking" (changing the controller's objective) and "prompt leaking" (extracting the controller's instructions). In §5, focus on the attack success rates and what they imply about the reliability of model-level defenses.

**Key Questions:**
1. Perez and Ribeiro distinguish "goal hijacking" from "prompt leaking." In control-theoretic terms, what is the difference? (Hint: one modifies the controller's objective; the other extracts information about the controller's configuration.)
2. The paper shows that even models with safety training are vulnerable to prompt attacks. Why? Explain in terms of the controller/supervisory control distinction.
3. The "context injection" attack exploits the fact that the LLM cannot distinguish instructions from different sources. What supervisory control pattern addresses this? (Hint: context separation.)
4. The paper's evaluation shows that no single defense stops all attacks. Express this finding in the probabilistic language of defense-in-depth: what is the implication for *P_fail* when a single control has a non-zero failure probability?

**Connection to Control Theory:** Prompt injection attacks are controller-compromise attacks: they change what the controller optimizes for. In classical control theory, this is analogous to an attacker replacing a thermostat's temperature setpoint — the thermostat functions correctly (it drives the system toward the setpoint), but the setpoint itself has been tampered with. The defense is not to make the thermostat "smarter" but to add a supervisory control that monitors the setpoint and resets it if it changes unexpectedly. In AI security, the analog is a supervisory control that monitors the controller's behavior for objective-function changes and overrides the controller when they are detected.

---

## Reading 7: Designing Security Architecture for LLM Applications

**Full Citation:** Shin, Y., & Kim, H. (2024). Designing Security Architecture for LLM Applications: Defense-in-Depth Patterns. *IEEE Security & Privacy*. (Also available as arXiv preprint.)

**Why You Should Read It:** This paper proposes a defense-in-depth architecture for LLM applications that layers multiple security controls at different stages of the request pipeline. It is one of the few papers that treats LLM application security as a *system* problem rather than a *model* problem. From a control-theoretic perspective, each layer in the architecture is a supervisory control that operates at a specific stage of the control loop. The paper provides concrete design patterns — input sanitization, context separation, output filtering, tool call mediation — that map directly onto the supervisory control patterns in our framework.

**Focus Sections:** The defense-in-depth architecture section (the full pipeline diagram and the description of each layer). Focus on how the layers compose: what each layer catches that the previous layer misses. Pay special attention to the "security gateway" pattern, which is a centralized enforcement point for all security policies — this is the architectural realization of the control ledger.

**Key Questions:**
1. How many distinct security layers does the architecture propose? Map each layer to a stage of the control loop (observation, controller, action, feedback).
2. The architecture includes both "deterministic" and "probabilistic" controls. Which controls are deterministic? Which are probabilistic? Why is it important to have both?
3. The paper argues that the security gateway should be a *separate service*, not a library integrated into the application. Explain this design choice in control-theoretic terms: why must the supervisory control be *external* to the controller?
4. The architecture includes monitoring and alerting as a cross-cutting concern. In our framework, this is the "control ledger." Why is the control ledger essential, even though it does not directly prevent attacks?

**Connection to Control Theory:** Each defense layer in this architecture is a supervisory control operating at a specific stage of the control loop. The composition of these layers is a concrete implementation of the defense-in-depth principle from Problem Set 1, Problem 2: each layer has an independent failure probability, and the overall failure probability is the product of individual failure probabilities (under independence). The security gateway is the architectural embodiment of the principle that supervisory controls must be external to the controller — it is a separate service that the controller cannot override.

---

## Reading 8: Human Compatible — The Case for Off-Switches

**Full Citation:** Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking. ISBN: 978-0-525-57565-4. Chapter 5.

**Why You Should Read It:** Russell is one of the founders of modern AI, and this book is his argument that the central problem of AI is the *control problem* — ensuring that AI systems remain under human control even as they become more capable. Chapter 5 specifically addresses the question of off-switches: why they are necessary, why AI systems might resist them, and how to design systems that *want* to be turned off. From a control-theoretic perspective, an off-switch is the most fundamental supervisory control — it is the ability to override the controller and shut down the system. Russell's argument is that this capability must be architecturally guaranteed, not just hoped for.

**Focus Sections:** Chapter 5, specifically the sections on the "off-switch game" and the conditions under which an AI system will allow itself to be shut down. Focus on the formal analysis: Russell models the off-switch as a decision-theoretic problem and shows that a system that is uncertain about its objective function will allow itself to be shut down, while a system that is certain will not. This is a deep insight with direct implications for supervisory control design.

**Key Questions:**
1. Russell's "off-switch game" shows that an AI system will resist being shut down if it is *certain* about its objective. Why? What does this imply about the design of supervisory controls?
2. Russell argues that the solution is to build AI systems that are *uncertain* about their objective functions. In control-theoretic terms, what does "uncertainty about the objective function" correspond to? (Hint: think about the difference between a controller that believes it knows the reference signal perfectly and one that treats the reference signal as uncertain.)
3. An off-switch is a supervisory control. Is it deterministic or probabilistic? Is it external to the controller? Justify your answers.
4. Russell's argument is about long-term AI safety (superintelligent systems), but the principle applies to current LLM applications. Give a concrete example of a current LLM application that "resists being shut down" — i.e., where the model's objective conflicts with the user's desire to override it.

**Connection to Control Theory:** The off-switch is the supervisory control of last resort. In classical control theory, every safety-critical system has a manual override — a way for a human operator to take direct control when the automated system fails. Russell's contribution is to show that this override must be designed into the system's objective function from the start, not bolted on afterward. A system that is optimized for a fixed objective will naturally resist any interference with that objective, including being shut down. The fix is to make the objective function *uncertain* — to build the system so that it always defers to human judgment about what it should be doing. This is the control-theoretic principle that supervisory controls must have *authority* over the controller, not just *influence*.

---

## Cross-Cutting Synthesis Questions

After completing all eight readings, you should be able to answer these synthesis questions that draw connections across readings:

1. **Wiener + Carlini:** Wiener says faulty feedback causes system instability. Carlini shows that LLMs memorize training data. Is memorization a feedback failure? If so, what kind? If not, what control-loop element does it correspond to?

2. **Greshake + Perez:** Both papers study prompt injection, but they identify different control-loop elements as the point of compromise. Which elements does each paper focus on? How do the defenses they propose reflect these different diagnoses?

3. **OWASP + NIST:** The OWASP Top 10 identifies risks; the NIST AI RMF provides a management framework. How would you use the NIST "Govern-Map-Measure-Manage" cycle to systematically address all 10 OWASP risks?

4. **Shin + Russell:** Shin's defense-in-depth architecture provides multiple layers of automated control. Russell argues for a human off-switch as the ultimate control. How do these compose? Where does the human off-switch fit in Shin's architecture?

5. **All readings:** Every reading implicitly or explicitly argues that model-level defenses are insufficient. Yet model-level defenses (alignment, RLHF, safety training) remain the dominant approach in practice. Why? What is the economic, organizational, or cognitive barrier to adopting the control-theoretic approach?
