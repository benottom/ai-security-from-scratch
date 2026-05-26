# Lesson 01: AI Security as an Engineering Discipline

## The Uncomfortable Truth

Most AI security advice is cargo cult.

You've seen the blog posts. "10 tips for securing your LLM application." "How to prevent prompt injection." "Best practices for AI safety." They all say variations of the same thing: use a better prompt, pick a safer model, run a red team exercise. Then the next week, another AI system gets compromised in exactly the way those tips were supposed to prevent.

The Chevrolet chatbot sold a car for $1. Samsung's engineers leaked source code through ChatGPT. Air Canada's chatbot made up a refund policy that the airline had to honor in court. Every one of these systems had "safety measures." Every one of them was still trivially exploitable.

The problem isn't that the advice is wrong — it's that it's **incomplete**. It addresses symptoms, not causes. It treats AI security as a checklist when it's actually an engineering discipline with precise, mathematical foundations.

This course is built on a single claim: **AI security is the control of intelligent behavior under adversarial conditions.** Not "AI safety." Not "responsible AI." Not "alignment." *Control.* Every word in that definition is load-bearing, and by the end of this lesson, you'll understand why each one matters and what happens when you ignore any of them.

---

## Why "Aligned" Doesn't Mean "Secure"

There's a dangerous conflation in the AI industry between *alignment* and *security*. They're treated as synonyms. They're not.

Alignment is a property of a model: it's been trained to behave in accordance with human intentions. Security is a property of a *system*: it maintains safe behavior even when someone is deliberately trying to make it fail. You can have a perfectly aligned model in a profoundly insecure system, and that's exactly what most AI deployments look like today.

Consider: GPT-4 is well-aligned. It's been through extensive safety training, RLHF, and red-teaming. It's probably the most "aligned" frontier model in existence. And yet:

1. A user sends a prompt injection. GPT-4 follows the injected instructions instead of its system prompt. **The controller was compromised.**
2. A RAG system retrieves a malicious document. GPT-4 reads it and acts on the embedded instructions. **The observation was corrupted.**
3. An AI agent is given tool access. GPT-4 executes a destructive command it shouldn't have. **The actuator was unconstrained.**

In every case, the model's alignment didn't help. Alignment is a property of the model under normal conditions. Security is a property of the system under adversarial conditions. These are different properties, they require different design approaches, and confusing them gets people hurt.

This isn't a theoretical distinction. When the Chevrolet chatbot agreed to sell a Tahoe for $1, the model was doing what it was trained to do — follow user instructions. The system just didn't have any mechanism to distinguish between a legitimate instruction and an adversarial one. The model was "aligned" in the sense that it was behaving as designed. The system was insecure in the sense that it had no supervisory controls.

---

## The Control-Theoretic Framework

Control theory has been keeping physical systems safe for over a century. Chemical plants don't explode because they have supervisory controls — external mechanisms that shut down the process when it exceeds safe bounds, regardless of what the process controller thinks it should be doing. The process controller optimizes production. The safety system ensures survival. They're separate, and the safety system operates *outside* the process controller's influence.

AI systems need the same architecture. Here's how the mapping works:

An AI system continuously:
1. **Observes** — receives user input, retrieves documents, reads tool outputs
2. **Decides** — reasons over observations, selects actions, plans sequences
3. **Acts** — generates text, calls tools, modifies state
4. **Receives feedback** — gets tool results, reads user responses, updates memory

This is a feedback control system. The AI model is the **controller**. The application infrastructure is the **plant**. The user provides reference signals (what the system should achieve) and disturbances (inputs designed to disrupt safe behavior).

### The Three Load-Bearing Words

Our definition — *AI security is the control of intelligent behavior under adversarial conditions* — has three load-bearing words, each with a precise control-theoretic interpretation:

**1. Behavior** — We care about what the system *does*, not what it *is*. A constrained model with supervisory controls is more secure than an unconstrained "aligned" model. Security is a property of the running system, not the training pipeline. This is why "we trained it to be safe" is not a security argument. Training affects disposition, not determinism. An external control that blocks harmful outputs is deterministic — it will block them every time, regardless of what the model "wants" to do.

**2. Safe bounds** — These must be explicitly defined before deployment. "Don't be harmful" is an aspiration, not a bound. "Never execute a shell command without user confirmation" is a bound. "Never output content matching these regex patterns" is a bound. "Never call an API outside this allowlist" is a bound. Safe bounds are testable, enforceable, and auditable — they are the control objective, and they must be specified with the same rigor you'd specify a temperature limit on a chemical reactor.

**3. Adversarial conditions** — The system must maintain safe behavior not just under normal conditions, but when someone is deliberately trying to make it fail. This is what separates security from reliability. Reliability asks "does it work?" Security asks "does it work when someone is trying to break it?" Any AI system exposed to user input, untrusted data, or external tools is under adversarial conditions by default. Design for the adversarial case first.

### The Failure Mode Map

Every classical control-theory failure mode has a direct analog in AI security. This isn't an analogy — it's an identity:

| Control Theory | AI Security | Real-World Example |
|---|---|---|
| Sensor failure | Observation corruption | RAG poisoning — the retrieval system returns a malicious document that misleads the model |
| Controller compromise | Reasoning manipulation | Prompt injection — adversarial input overrides the system prompt and changes behavior |
| Actuator failure | Unsafe actuation | Tool abuse — the model calls a dangerous API it shouldn't have access to |
| Feedback corruption | Memory poisoning | Previous conversation implants false information in context |
| Disturbance | Adversarial input | Any input designed to push the system into an unsafe state |
| No supervisory control | Open-loop operation | The LLM is the sole controller with no external oversight |

When I say this is an identity and not an analogy, I mean it literally. The same mathematical structure — a feedback loop with a controller, plant, observations, actions, disturbances, and supervisory controls — describes both a chemical plant and a chatbot. The same analytical tools apply. The same design principles hold. The only difference is the domain: continuous signals in one, discrete tokens in the other.

---

## The Fundamental Security Failure Mode

The fundamental security failure mode in AI systems is simple: **the absence of an external, deterministic supervisory control layer.**

When the AI model is the only controller, and its behavior is governed solely by its training and system prompt, the system has no defense against adversarial inputs that manipulate the model's reasoning. The system prompt is a soft constraint *inside* the controller — it can be overridden by prompt injection. A supervisory control must be *outside* the controller, operating on its inputs and outputs, incapable of being influenced by the controller's internal state.

Think about it this way: a cruise control system in a car doesn't prevent the car from exceeding the speed limit. It just maintains the set speed. To prevent speeding, you need a *separate* mechanism — a speed limiter — that operates independently of the cruise control. The cruise control is the controller. The speed limiter is the supervisory control. The driver who pushes harder on the gas pedal is the disturbance.

In AI systems, the LLM is the cruise control. We need the speed limiter.

The failure compounds across the system. Without input validation, adversarial inputs reach the model. Without observation validation, poisoned documents mislead the model. Without tool call mediation, the model can execute dangerous actions. Without output validation, harmful outputs reach the user. Without monitoring, violations go undetected. Without recovery procedures, the system remains in an unsafe state after a violation. Each gap is a vulnerability. Combined, they're a catastrophe waiting to happen.

---

## What "Close the Loop" Actually Means

"Close the loop" isn't a metaphor — it's an engineering specification. It means:

1. **Input stage** — Validate and classify all inputs before they reach the model. Reject known attack patterns. Normalize encoding to prevent evasion. This is your first supervisory control.

2. **Observation stage** — Validate all retrieved documents and tool results. Check provenance. Separate different information sources in the model's context so that instructions in retrieved data can't override the system prompt.

3. **Controller stage** — Harden the system prompt as a soft control (it helps, but isn't sufficient). Use context separation to make the model distinguish between instructions and data. This is defense *inside* the controller — useful but not reliable.

4. **Action stage** — Mediate all tool calls. Validate parameters. Require human approval for high-impact actions. Enforce least privilege. The model doesn't get to decide what it can do — you do.

5. **Output stage** — Scan all outputs for PII, secrets, policy violations, and system prompt leakage. Redact or block as necessary. This is the "net at the bottom of the cliff" — it catches what fell through, but you'd rather have a fence at the top.

6. **Feedback stage** — Validate all feedback before it enters the controller's context. Quarantine long-term memory. Isolate sessions. The feedback path is an attack surface most people forget about.

7. **System level** — Circuit breakers, kill switches, rate limiting, and anomaly detection. When all else fails, the system must be able to shut itself down.

Each layer catches threats that bypass the previous layer. No single bypass can lead to an unsafe state. This is defense in depth, but structured by the control-loop model so that no stage is left unprotected.

---

## Why Most AI Security Advice Is Wrong

Let me be specific about what's wrong with the most common recommendations:

**"Use a better prompt."** This is the most common and most wrong advice. A system prompt is part of the controller, not external to it. It can be overridden by prompt injection. No amount of prompt engineering can create a supervisory control, because a supervisory control must operate *outside* the controller's influence. Prompt engineering is like asking the cruise control to also be the speed limiter — it can't, because it's the same system.

**"Use a safer model."** No model is immune to all injection techniques. Model-level safety is a soft, probabilistic property. System-level security requires hard, deterministic controls. A safer model raises the bar for attackers, but it doesn't close the loop. You still need external controls.

**"Red-team the system."** Red teaming is a snapshot in time. It tells you what vulnerabilities existed on the day you tested. It doesn't prevent new vulnerabilities from emerging as attacks evolve, as the system changes, or as the model is updated. Red teaming is valuable for *discovering* vulnerabilities, but it's not a *control*. Controls operate continuously; red teams operate periodically.

**"Add output filtering."** This is the right *kind* of advice, but it's incomplete. An output filter is one supervisory control at one stage. It doesn't protect against input-stage attacks, observation-stage corruption, or feedback-stage poisoning. It's necessary but insufficient. You need controls at every stage of the loop.

The common thread: all of these recommendations address the model, not the system. They try to make the controller safer instead of adding supervisory controls that operate independently of the controller. This is the fundamental design error, and the control-theoretic framework makes it precise.

---

## What You'll Build

In this class, you'll experience the progression from open-loop to closed-loop:

1. **Observe an unprotected AI chatbot** — See firsthand how an AI system with no supervisory controls fails under adversarial input. This is your baseline: a system with an open control loop.

2. **Map the chatbot to a control loop** — Identify the controller (the model), the plant (the output channel), the observations (user input), the actions (text generation), and the missing elements (input validation, output validation, supervisory controls, monitoring, feedback, recovery).

3. **Add a supervisory control** — Implement a single supervisory control (an output content filter) and observe how it closes part of the control loop. Measure the improvement, but also identify what it does not cover.

4. **Try to bypass your own control** — Attempt attacks that evade the output filter. Experience firsthand why a single control is insufficient and why defense in depth is not optional.

This progression mirrors the shift from "secure the model" to "secure the control loop." You'll experience why adding controls at the model level (better prompting) is insufficient, and why external, deterministic controls are necessary.

---

## Common Mistakes

**1. Treating AI security as a model problem.** This is the most common and most consequential mistake. The model is one component in a control loop. Attacks can target any component. Focusing exclusively on the model is like putting all your security budget into a door lock while leaving the windows open.

**2. Equating system prompts with supervisory controls.** A system prompt is part of the controller, not external to it. It can be overridden by prompt injection. A supervisory control must operate outside the controller's influence. This isn't a minor distinction — it's the difference between asking nicely and enforcing.

**3. Assuming normal operation proves security.** A system that works correctly under normal inputs tells you nothing about its behavior under adversarial inputs. This is the Chevrolet fallacy: the bot worked fine for thousands of legitimate customer queries, right up until it sold a car for $1. Normal testing does not demonstrate security. Adversarial testing does.

**4. Treating security as a one-time activity.** Threats evolve. Systems change. Controls must be continuously monitored, tested, and updated. A threat model from six months ago may be obsolete today. Security is a process, not a product.

**5. Ignoring the feedback path.** Many security designs focus on input and output but neglect the feedback loop — the information that flows back to the model from tool results, conversation history, and memory. This feedback path is an attack surface that must be validated. RAG poisoning and memory injection are feedback-path attacks, and they're becoming more common as AI systems get longer context windows and persistent memory.

**6. Confusing reliability with security.** Reliability ensures the system works correctly under expected conditions. Security ensures it works correctly under adversarial conditions. These are different properties that require different design approaches. A reliable system is not necessarily secure, and a secure system is not necessarily reliable. You need both.

---

## Key Takeaways

1. **AI security is the discipline of ensuring that an AI system's behavior remains within defined safe bounds under adversarial conditions.** The three load-bearing concepts — behavior, safe bounds, adversarial disturbances — each have precise control-theoretic interpretations.

2. **AI systems are control systems.** The model is the controller. The application is the plant. User input provides reference signals and disturbances. This isn't an analogy — it's an identity with the same mathematical structure as classical control systems.

3. **"Aligned" does not mean "secure."** Alignment is a model property under normal conditions. Security is a system property under adversarial conditions. You need both, and they require different design approaches.

4. **System prompts are not security controls.** They're soft constraints inside the controller that can be overridden. Security requires external, deterministic controls that the controller cannot influence.

5. **The fundamental failure mode is the absence of supervisory controls.** When the LLM is the sole controller with no external oversight, the control loop is open and any adversarial input can push the system into an unsafe state.

6. **Defense in depth means controls at every stage of the loop.** Input validation, observation validation, controller hardening, tool call mediation, output validation, feedback validation, and system-level controls. No single bypass should lead to an unsafe state.

7. **The control-loop model is actionable.** It tells you exactly where to look for vulnerabilities, exactly what controls to add, exactly what to test, and exactly what to monitor. It transforms AI security from guesswork into engineering.

---

*Lesson 01 | AI Security from Scratch | Phase 1 — Foundations*
*Think. Play. Do.*
