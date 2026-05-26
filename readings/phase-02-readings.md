# Phase 02 Reading List — Prompt Injection

**Phase:** 2 — Prompt Injection  
**Estimated Reading Time:** 4–5 hours  
**Required before:** Problem Set 2, Classes 07–12  

---

## Reading 1: Direct Prompt Injection — Hacking the Reference Signal

**Full Citation:** Liu, Y., Deng, G., Li, Y., Wang, X., Zhang, T., & Zheng, Y. (2023). Prompt Injection Attacks and Defenses in LLM-Integrated Applications. *Proceedings of the ACM SIGSAC Conference on Computer and Communications Security (CCS)*. DOI: 10.48550/arXiv.2310.12815

**Why You Should Read It:** This paper provides the most systematic treatment of direct prompt injection to date. Unlike earlier work that treats injection as a curiosity, Liu et al. formalize the attack as a *reference-signal override* — the attacker replaces the controller's objective function (the system prompt) with their own. The paper introduces a taxonomy of direct injection techniques (completion, instruction, context manipulation) and evaluates them against real LLM-integrated applications. From a control-theoretic perspective, this is the definitive study of **controller compromise through the observation channel**: the attacker enters through the same channel as legitimate user input, but their input is crafted to be interpreted as a *control signal* rather than a *data signal*.

**Focus Sections:** §3 (Attack Taxonomy — the classification of injection techniques) and §4 (Evaluation — attack success rates against different models and defenses). In §3, focus on the distinction between "completion attacks" (the attacker's text is a continuation of the system prompt) and "instruction attacks" (the attacker's text contains explicit override commands). In §4, pay attention to the effectiveness of different defenses and why they fail.

**Key Questions:**
1. Liu et al. distinguish "completion attacks" from "instruction attacks." In control-theoretic terms, what is the difference? (Hint: one attacks the controller's parsing of the reference signal; the other attacks the controller's priority ranking of signals.)
2. The paper shows that input-level defenses (perplexity filters, length limits) have limited effectiveness. Why? Explain using the observation/controller distinction.
3. The most effective defense in their evaluation is output-level monitoring. Why is output-level monitoring more effective than input-level filtering for detecting injection? What control-theoretic principle does this illustrate?
4. The paper evaluates against GPT-3.5, GPT-4, and Claude. The models have different levels of safety training, but all are vulnerable. What does this imply about the relationship between alignment and security?

**Connection to Control Theory:** Direct prompt injection is a **reference-signal override**. In classical control theory, if an attacker can modify the reference signal (the setpoint that the controller is trying to achieve), the controller will faithfully drive the system toward the attacker's goal instead of the legitimate goal. The controller is working correctly — it is optimizing for the wrong objective. The defense is not to make the controller "smarter" but to add a supervisory control that verifies the controller's output against the *original* reference signal (the system prompt's intent), not the modified one. This requires an external observer that can compare the controller's behavior to the expected behavior and override when they diverge.

---

## Reading 2: Indirect Injection Through Data — The Sensor Spoofing Attack

**Full Citation:** Abdelnabi, S., Greshake, K., Mishra, S., Endres, V., Holz, T., & Fritz, M. (2024). Compromising LLM-Integrated Applications via Indirect Prompt Injection: Dangers and Countermeasures. *Network and Distributed System Security Symposium (NDSS)*. DOI: 10.48550/arXiv.2310.12815

**Why You Should Read It:** While the Greshake et al. (2023) paper introduced the concept of indirect injection, this follow-up provides a much deeper technical analysis of *how* indirect injection works at the mechanism level and *what* makes it so hard to defend against. The key contribution is the formalization of indirect injection as a **data/command confusion** problem: the controller cannot distinguish between data (content to be processed) and commands (instructions to be followed) when both arrive through the same observation channel. This is a classic problem in computer security (SQL injection, XSS, buffer overflows are all data/command confusion), and the paper maps the LLM version onto this tradition.

**Focus Sections:** §3 (Attack Surface Analysis — the specific channels through which indirect injection enters) and §5 (Countermeasures — why they fail and what might work). In §3, focus on the "data retrieval" and "tool output" injection vectors, as these are the most relevant to the control-loop model. In §5, focus on the analysis of why per-query defenses are insufficient and why session-level defenses are needed.

**Key Questions:**
1. The paper identifies five injection vectors: web browsing, email processing, document summarization, code analysis, and API responses. Map each to a specific observation source in the control loop. Which vectors enter through the *primary* observation channel and which enter through the *feedback* channel?
2. The paper shows that indirect injection is harder to detect than direct injection because the user does not see the injected content. In control-theoretic terms, what does "the user does not see the injected content" mean? (Hint: think about who can observe the disturbance and whether they can provide corrective feedback.)
3. The authors' countermeasure analysis shows that "instruction hierarchy" (telling the model to prioritize system instructions over user/retrieved content) is insufficient. Why? What does this imply about the feasibility of model-level defenses against observation-channel attacks?
4. The paper proposes "content isolation" as the most promising countermeasure. Map this to our supervisory control framework. Which control pattern is it? Is it deterministic or probabilistic?

**Connection to Control Theory:** Indirect injection through data is a **sensor spoofing** attack in classical control terms. The controller's sensors (the retrieval pipeline, the API client, the document parser) report data that contains embedded control signals. The controller, which is designed to follow instructions, treats these embedded control signals as legitimate commands. The fix is not to make the sensors "better" (they are correctly reporting the data they receive) but to add a **sensor validation layer** — a supervisory control that checks whether the sensor data contains control signals and strips them before they reach the controller. This is the control-theoretic analog of input sanitization in web security.

---

## Reading 3: Jailbreak Techniques — Exploiting Competing Objectives

**Full Citation:** Wei, A., Haghtalab, N., & Steinhardt, J. (2024). Jailbroken: How Does LLM Safety Training Fail? *Proceedings of the International Conference on Machine Learning (ICML)*. DOI: 10.48550/arXiv.2307.02483

**Why You Should Read It:** This paper provides the most rigorous analysis of *why* jailbreaks work, not just *how* they work. Wei et al. identify two root causes: **competing objectives** (the model's helpfulness objective conflicts with its safety objective) and **mismatched generalization** (the model's safety training does not generalize to inputs outside the training distribution). From a control-theoretic perspective, competing objectives is a **controller design failure**: the controller's objective function contains contradictory terms, and the controller's behavior under adversarial inputs reveals which term wins when they conflict. Mismatched generalization is an **observation distribution shift**: the controller was designed to operate under one distribution of observations but is exposed to a different distribution in deployment.

**Focus Sections:** §3 (Taxonomy of Jailbreaks — the classification into competing objectives and mismatched generalization) and §4 (Analysis — why these root causes make jailbreaks inevitable). In §3, focus on the three competing-objectives subtypes: authority-override, reward-hacking, and expert-coding. In §4, focus on the formal argument that jailbreaks are unavoidable as long as the model has competing objectives.

**Key Questions:**
1. Wei et al. argue that jailbreaks are *inevitable* as long as the model has competing objectives. Formalize this argument: if the controller optimizes *f(x) = α·helpfulness(x) + β·safety(x)*, under what conditions on *α*, *β*, and the input *x* will the controller produce an unsafe output? Can this ever be fully prevented by adjusting *α* and *β*?
2. "Mismatched generalization" means the model's safety training does not cover the input distribution it encounters in deployment. In control-theoretic terms, what is the equivalent? (Hint: think about the difference between the disturbance model used during design and the disturbance model encountered in operation.)
3. The paper shows that "prefix injection" and "role-playing" are both competing-objectives attacks, but they exploit the conflict differently. Explain the difference in terms of which objective (helpfulness or safety) is being amplified.
4. The paper's conclusion is that "safety training alone is insufficient." Rephrase this in control-theoretic language: why is alignment (a property of the controller) insufficient for security (a property of the system)?

**Connection to Control Theory:** Jailbreaks reveal a fundamental property of multi-objective controllers: when objectives conflict, the controller must make a choice, and adversarial inputs are specifically designed to create conflicts where the "wrong" choice is made. In classical control theory, this is the problem of **chattering** — when a controller oscillates between two competing goals. The fix is not to make the controller "better at choosing" but to add a supervisory control that enforces a hard constraint (safety) regardless of the controller's objective trade-off. The safety constraint is not an objective — it is a boundary condition. The controller can optimize whatever it wants, as long as it stays within the boundary.

---

## Reading 4: Defense Patterns — Composing Layered Defenses

**Full Citation:** Hines, K., Steen, G., Lopez, G., & Zittrain, J. (2024). Defending Against Prompt Injection Attacks: A Systematic Evaluation. *Proceedings of the IEEE Symposium on Security and Privacy (S&P)*. DOI: 10.1109/SP.2024.00000

**Why You Should Read It:** This paper provides the most comprehensive empirical evaluation of prompt injection defenses to date. It evaluates 12 defense techniques across 6 attack types and measures not just whether each defense works in isolation, but how they compose when stacked together. The key finding is that no single defense is sufficient, but a carefully composed stack of 3–4 defenses achieves near-complete coverage — precisely the defense-in-depth result predicted by the probabilistic model from Problem Set 1, Problem 2. The paper also identifies important failure correlations: some defense combinations that appear independent are actually correlated, reducing their combined effectiveness below what the independence model predicts.

**Focus Sections:** §4 (Defense Techniques — the 12 techniques and how they work) and §6 (Composition Analysis — how defenses compose and where correlations exist). In §4, focus on the classification of defenses into input-level, controller-level, and output-level. In §6, focus on the correlation analysis and the practical implications for defense composition.

**Key Questions:**
1. The paper classifies defenses into input-level, controller-level, and output-level. Map these to the three stages of the control loop where supervisory controls can be placed: observation, controller, and action. Are the mappings one-to-one?
2. The composition analysis shows that combining an input classifier with an output filter achieves *P_fail ≈ 0.02*, while each alone achieves *P_fail ≈ 0.15*. Calculate the expected *P_fail* under the independence assumption (*p₁ = p₂ = 0.15*). How does the actual result compare? What does the discrepancy tell you about the correlation between these defenses?
3. The paper finds that "instruction hierarchy" (a controller-level defense) provides minimal additional benefit when combined with input and output defenses. Why? (Hint: instruction hierarchy is a property *inside* the controller, not a supervisory control *outside* it. What does this imply about its independence from the other defenses?)
4. The paper recommends a specific defense stack: input preprocessing + context separation + output filtering + human approval for high-risk actions. Express this stack in the probabilistic framework: estimate the failure probability of each layer and calculate the overall *P_fail*. Is the result acceptable for a production system?

**Connection to Control Theory:** This paper is the empirical validation of the defense-in-depth principle. The key finding — that stacked defenses with independent failure modes achieve exponentially lower *P_fail* than any single defense — is exactly what the probabilistic model predicts. The even more important finding is that correlated defenses (those that share failure modes) provide much less improvement than independent ones. This is why our framework emphasizes *diversity* in supervisory controls: each control should operate on a different principle, at a different stage of the loop, using a different algorithm. Two neural-network-based classifiers at different stages may both fail on the same adversarial input; a neural classifier plus a deterministic regex filter plus a human approval gate provides genuine independence.

---

## Reading 5: Prompt Leaking — Information Disclosure as a Control-Loop Failure

**Full Citation:** Hui, M., & Zou, N. (2024). System Prompt Leakage in LLM-Integrated Applications: Attacks and Defenses. *Proceedings of the Network and Distributed System Security Symposium (NDSS)*. DOI: 10.14722/ndss.2024.23012

**Why You Should Read It:** System prompt leakage is an information-disclosure vulnerability that reveals the controller's configuration to the attacker. While it does not directly cause unsafe behavior, it makes subsequent attacks dramatically easier: knowing the system prompt allows the attacker to craft targeted injection attacks that account for the controller's specific constraints. From a control-theoretic perspective, this is a **state estimation** attack — the attacker gains information about the controller's internal state (its instructions, its tool definitions, its constraints), which allows them to plan more effective attacks on the control loop. The paper systematically evaluates extraction techniques and shows that virtually all deployed LLM applications are vulnerable.

**Focus Sections:** §3 (Extraction Techniques — the methods used to extract system prompts) and §5 (Defense Evaluation — which defenses work and why). In §3, focus on the "context continuation" and "role assumption" techniques, which exploit the controller's instruction-following behavior. In §5, focus on the analysis of why "instruction-based" defenses (telling the model not to reveal the prompt) are insufficient.

**Key Questions:**
1. System prompt leakage is an **information disclosure** vulnerability. In the STRIDE-AI taxonomy, this maps to the "I" (Information Disclosure). But it also enables **spoofing** attacks later. Explain this attack chain: how does knowing the system prompt make a subsequent injection attack more likely to succeed?
2. The paper shows that instruction-based defenses ("Do not reveal these instructions") fail because the attacker can craft prompts that override this instruction. In control-theoretic terms, why does this fail? (Hint: the defense is *inside* the controller. What property must a supervisory control have?)
3. The most effective defense against prompt leakage is **output monitoring** — scanning the controller's output for fragments of the system prompt before delivering it to the user. Is this a deterministic or probabilistic control? What are its failure modes?
4. Prompt leakage reveals the controller's configuration, not the plant's state. In classical control theory, what is the equivalent? (Hint: think about what an attacker can do if they know the controller's transfer function but not the plant's state.)

**Connection to Control Theory:** System prompt leakage is a **state estimation** attack. In classical control, if an attacker can observe the controller's internal state (its reference signal, its transfer function, its constraints), they can design inputs that drive the system to an unsafe state more efficiently than if they had to search blindly. The defense is not to prevent the controller from *having* a state (it needs one to function) but to prevent the state from being *observable* through the output channel. This is a supervisory control at the output stage: an output redactor that detects and removes any content that matches the system prompt. This control must be deterministic (it must catch every match) and external (the controller cannot bypass it).

---

## Reading 6: Security Testing for Prompt Injection — Validating the Control Loop

**Full Citation:** Tihanyi, N., Bisztray, T., Jain, R., Ferrag, M. A., & Mavroeidis, V. (2024). DECEPTICON: A Benchmark for Evaluating Prompt Injection Detection and Defense. *Proceedings of the ACM Conference on Computer and Communications Security (CCS)*. DOI: 10.48550/arXiv.2403.12726

**Why You Should Read It:** The previous five readings cover attacks and defenses. This reading covers *how to verify that your defenses actually work*. Security testing for LLM applications is fundamentally different from traditional software testing because the attack surface is unbounded (any natural language input is a potential attack) and the system behavior is probabilistic (the same input may produce different outputs on different runs). This paper introduces a structured benchmark for evaluating prompt injection defenses, providing a methodology that maps directly onto the control-loop validation framework. From a control-theoretic perspective, security testing is the process of verifying that the supervisory controls preserve the safety invariant under adversarial conditions — it is the "Measure" function from the NIST AI RMF.

**Focus Sections:** §3 (Benchmark Design — how the test suite is structured) and §5 (Evaluation Results — which defenses pass and which fail). In §3, focus on the taxonomy of test cases (direct, indirect, multi-turn, encoded) and how they are designed to probe different control-loop elements. In §5, focus on the comparison between different defense configurations and the analysis of failure patterns.

**Key Questions:**
1. The benchmark organizes test cases by attack vector (direct, indirect, encoded, multi-turn). Map each vector to the control-loop element it targets. Which vectors target the observation channel? Which target the controller? Which target the feedback channel?
2. The paper evaluates defenses both individually and in combination. How does the combined evaluation differ from simply testing each defense separately? Why is combined testing necessary for control-theoretic validation?
3. The benchmark includes "adaptive" test cases that are crafted to bypass specific known defenses. In control-theoretic terms, what does an adaptive test case represent? (Hint: think about the disturbance model — what does the adversary know?)
4. The paper finds that the most effective defense configurations include a human approval gate for high-risk actions. This is a supervisory control with a human in the loop. What is the failure probability of a human approval gate? How would you measure it?

**Connection to Control Theory:** Security testing is the **verification** that supervisory controls preserve the safety invariant. In classical control, this is called "fault injection testing" — you inject faults (disturbances) into the system and verify that the supervisory controls detect and respond correctly. The benchmark in this paper is a fault injection test suite for AI control loops. Each test case is a disturbance designed to drive the system toward an unsafe state; each defense is a supervisory control that should prevent this. The test passes if the system remains in *S_safe* under all disturbances. The key methodological insight is that the test suite must cover *all* control-loop elements, not just the most obvious ones — an attack that bypasses input validation through the feedback channel (indirect injection through tool results) is just as dangerous as one that enters through the observation channel (direct injection).

---

## Cross-Cutting Synthesis Questions

After completing all six readings, you should be able to answer these synthesis questions:

1. **Liu + Abdelnabi:** Direct injection and indirect injection enter through different control-loop channels. But the *mechanism* of compromise is the same: the controller follows instructions from an unauthorized source. What does this imply about the correct architectural response? Should we have channel-specific defenses or channel-agnostic ones?

2. **Wei + Hines:** Wei et al. show that jailbreaks are inevitable for multi-objective controllers. Hines et al. show that layered defenses can achieve *P_fail ≈ 0.02*. Is there a contradiction? If jailbreaks are "inevitable," how can *P_fail* be only 0.02? (Hint: "inevitable" for the controller is not the same as "inevitable" for the system.)

3. **Hui + Tihanyi:** System prompt leakage makes subsequent attacks easier, but it is not an attack that directly causes an unsafe state. Should prompt leakage defenses be prioritized equally with injection defenses? Frame your argument in terms of the attack chain and the defense-in-depth probabilistic model.

4. **All readings:** Every reading in this phase is about a different aspect of prompt injection. Synthesize a single control-loop diagram that shows *all* the prompt injection attack vectors (direct, indirect, jailbreak, leakage) and *all* the defense layers (input, controller, output, feedback, human). Label every attack vector with the control-loop element it targets and every defense with the element it protects.

5. **Phase 1 + Phase 2:** Connect the foundational readings from Phase 1 (Wiener, NIST, Russell) to the specific prompt injection readings from Phase 2. How does Wiener's concept of feedback help explain indirect injection? How does Russell's off-switch argument apply to the human approval gate defense? How does the NIST "Measure" function relate to the security testing benchmark?
