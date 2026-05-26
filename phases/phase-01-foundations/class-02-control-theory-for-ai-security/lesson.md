# Lesson: Control Theory for AI Security

## Overview

This lesson provides the control-theoretic foundation that underpins the entire curriculum. We will define and explain the core concepts of control theory — feedback loops, controllers, plants, disturbances, reference signals, error signals, and supervisory control — and map each to its precise analog in AI system security. This is not a survey of control theory for its own sake; every concept is introduced because it directly enables the security engineering of AI systems.

The key argument is that supervisory control — a well-established concept in control theory — provides the right frame for AI safety and security. Just as a chemical plant has a process controller for production and a supervisory controller for safety, an AI system has a model for task performance and a supervisory layer for safety enforcement. Understanding this structure is essential for building secure AI systems.

---

## Why This Matters

AI systems are being given increasing autonomy: they retrieve information, make decisions, call tools, and take actions in the real world. As autonomy increases, the consequences of unsafe behavior escalate. A chatbot that produces harmful text is bad; an agent that executes harmful code is dangerous.

Control theory has spent over a century developing rigorous methods for ensuring that autonomous systems behave safely. These methods are based on precise mathematical definitions of stability, convergence, disturbance rejection, and supervisory override — exactly the properties we need in AI security. Ignoring this body of knowledge and reinventing AI security from scratch would be like ignoring physics when building a bridge.

The practical impact is immediate. When you understand that an AI system is a control loop, you can:
- **Identify** exactly where attacks enter (disturbances at each stage)
- **Design** exactly what controls are needed (supervisory layers at each stage)
- **Test** exactly what failure modes to look for (instability, divergence, saturation)
- **Monitor** exactly what signals indicate trouble (error growth, oscillation, saturation)
- **Recover** exactly how to return to a safe state (reset, throttle, isolate)

Without this framework, AI security is ad hoc — a collection of best practices and war stories. With it, AI security is engineering — a systematic, rigorous, testable discipline.

---

## Control-Theoretic Interpretation

### Core Concepts Mapped to AI Security

#### 1. The Plant (System Under Control)

In control theory, the plant is the system being controlled — the physical process whose behavior the controller regulates. In a chemical plant, the plant is the reactor vessel with its temperature, pressure, and flow rates. In AI security, the plant is the AI application infrastructure:

- The retrieval pipeline (vector databases, search indices)
- The tool interfaces (APIs, databases, file systems)
- The output channels (chat UI, email, file generation)
- The memory and state stores (conversation history, user profiles)

The plant has its own dynamics and its own failure modes. A tool that requires authentication is a safer plant than one that does not. A retrieval pipeline that validates document provenance is a safer plant than one that does not. Securing the plant is a prerequisite for securing the control loop.

#### 2. The Controller

The controller is the component that decides what actions to take based on observations of the plant's state. In AI security, the controller is the AI model and its surrounding orchestration logic — the system prompt, the reasoning framework, the tool selection logic, and the conversation management logic.

A key insight: the AI model is the *primary* controller, optimized for task performance (helpfulness, accuracy, fluency). It is NOT the supervisory controller, which is optimized for safety. These are different functions with different objectives, different time scales, and different failure modes — just as in any engineered control system.

#### 3. The Reference Signal

The reference signal is the desired state that the controller should drive the plant toward. In AI security, the reference signal is the intended safe behavior defined by the system's safety requirements. "Never output PII" is a reference signal. "Always confirm before executing financial transactions" is a reference signal. The reference signal is the control objective expressed as a measurable target.

#### 4. The Error Signal

The error signal is the difference between the reference (desired state) and the actual plant output. In AI security, the error signal is the deviation from safe behavior — how far the system's actual output is from the safety-compliant output defined by the reference.

A large error signal means the system is far from its safety objective. A growing error signal means the system is diverging — getting less safe over time. A stable error signal near zero means the system is maintaining its safety objective. Monitoring the error signal is the core of safety observability.

#### 5. Feedback

Feedback is the mechanism by which the controller learns about the effects of its actions. In a closed-loop system, the controller observes the plant's output, computes the error, and adjusts its actions to reduce the error. In AI security, feedback includes:
- Tool results that inform the model about what its actions achieved
- User responses that indicate whether the output was appropriate
- Monitoring signals that indicate whether safety constraints are being maintained

Without feedback, the system operates open-loop — the controller has no information about whether its actions achieved the objective. Open-loop operation is unsafe because disturbances cannot be detected or corrected.

#### 6. Disturbances

Disturbances are external signals that push the plant away from the desired state. In AI security, disturbances are adversarial inputs — prompt injections, poisoned documents, manipulated tool results, and any other input designed to make the system behave unsafely.

The critical distinction is between bounded and unbounded disturbances. A bounded disturbance has a known maximum magnitude; the controller can be designed to reject disturbances up to that magnitude. An unbounded disturbance has no known limit; no controller can guarantee safety against an unbounded disturbance. In practice, AI security disturbances are bounded by the context window, the tool capabilities, and the API constraints — which means control-theoretic disturbance rejection is feasible.

#### 7. Supervisory Control

Supervisory control is a higher-level controller that monitors the primary controller and overrides it when the system approaches or enters an unsafe state. The supervisory controller does not replace the primary controller — it constrains it. It operates at a different time scale, with different priorities, and with different failure modes.

The three essential properties of a supervisory control are:
1. **External to the controller** — It cannot be overridden by the controller it supervises
2. **Capable of override** — It can block, modify, or replace the controller's output
3. **Deterministic** — It enforces constraints every time, without exception

These properties are what distinguish a supervisory control from a system prompt. A system prompt is inside the controller, can be overridden, and is probabilistic. A supervisory control is outside the controller, cannot be overridden, and is deterministic.

### Open-Loop vs. Closed-Loop: Why the Difference Matters

An open-loop system has no feedback path. The controller acts on the plant without observing the result. If the plant's behavior deviates from the objective, the controller has no way to detect or correct the deviation.

A closed-loop system has a feedback path. The controller observes the plant's output, compares it to the reference, and adjusts its actions to reduce the error. Disturbances that push the system away from the objective are detected and corrected.

Most deployed AI systems are open-loop with respect to safety. The model generates output without any mechanism to verify that the output meets safety requirements. There is no error signal, no feedback, and no correction. Adding supervisory controls closes the loop: the output is observed, compared against safety requirements, and corrected if it violates them.

### Stability, Convergence, and Divergence

A stable control system converges to the reference signal despite disturbances. An unstable system diverges — the error grows over time instead of shrinking. In AI security:

- **Stable:** The system maintains safe behavior despite adversarial inputs. Supervisory controls detect and correct deviations.
- **Marginally stable:** The system oscillates between safe and unsafe behavior. Supervisory controls catch some violations but not others.
- **Unstable:** The system progressively loses safety constraints. Each successful attack makes subsequent attacks easier (e.g., multi-turn manipulation).

The goal of control-theoretic AI security is to design systems that are stable — that converge to safe behavior and maintain it even under disturbance. This requires proper feedback, adequate control authority, and well-tuned supervisory controls.

---

## Security Failure Mode

The failure mode is **control-theoretic instability under disturbance.** When the supervisory control layer is absent or inadequate, adversarial disturbances cause the system to diverge from its safety objective. The error signal grows, and there is no mechanism to arrest the growth.

In practice, this manifests as:
- **Divergent attacks:** Each successful injection makes the next one easier (positive feedback)
- **Saturation:** So many violations occur that the supervisory controls are overwhelmed
- **Oscillation:** The system alternates between safe and unsafe states, causing intermittent violations
- **Steady-state error:** The system consistently produces slightly unsafe outputs that are below detection thresholds

Each of these failure modes has a control-theoretic explanation and a control-theoretic remedy. Divergence requires negative feedback. Saturation requires adequate control authority. Oscillation requires proper damping. Steady-state error requires tighter control bounds.

---

## Defensive Design

Design the AI system as a stable closed-loop controller:

1. **Close the loop:** Add feedback paths that measure the system's actual safety state and feed it back to the supervisory controller.
2. **Ensure adequate control authority:** The supervisory controller must be able to override the primary controller. If it can only observe and log, it is not a controller — it is a monitor.
3. **Design for disturbance rejection:** Assume adversarial disturbances are the normal operating condition. Size the supervisory controls accordingly.
4. **Add damping:** Design the control response so that corrections do not cause oscillations (e.g., don't over-correct by blocking too aggressively, which causes false positives that erode trust).
5. **Implement supervisory hierarchy:** A local supervisor for per-request safety, and a global supervisor for system-level stability (circuit breakers, kill switches).
6. **Monitor the error signal:** Track the deviation from safe behavior over time. Growing error indicates instability; constant error indicates a control gap; shrinking error indicates convergence.

---

## What Learners Will Build

1. **An open-loop AI controller** — A simple chatbot with no feedback or supervision. Observe how it diverges under disturbance.
2. **A closed-loop version** — Add output observation and corrective action. Observe how feedback stabilizes the system.
3. **A supervised version** — Add a supervisory control layer with monitoring, override, and circuit breakers. Observe how the system maintains bounded error even under sustained adversarial pressure.

This progression demonstrates that each control-theoretic element — feedback, supervision, hierarchy — adds a specific, measurable improvement to the system's safety properties.

---

## Common Mistakes

1. **Confusing monitoring with control.** A system that logs violations but cannot act on them is not a control system — it is an observability system. Control requires the ability to act.
2. **Under-sizing the supervisory controller.** If the supervisory controller cannot handle the disturbance magnitude, it will saturate and the system will effectively be open-loop.
3. **Ignoring stability.** Adding controls without analyzing stability can create oscillatory behavior — the system swings between over-blocking and under-blocking.
4. **Placing controls inside the controller.** A safety constraint that is part of the model's context can be overridden. Supervisory controls must be external.
5. **Assuming a single feedback path is sufficient.** Real AI systems have multiple feedback paths (tool results, user input, memory). Each one must be validated.
6. **Neglecting the reference signal.** Without a clearly defined reference (what "safe" means in measurable terms), the error signal is undefined, and the control loop cannot operate.

---

## Key Takeaways

1. **Control theory provides precise definitions for AI security concepts.** Plant, controller, reference, error, feedback, disturbance, and supervisory control are not analogies — they are identities.
2. **Open-loop AI systems are inherently unsafe.** Without feedback, there is no mechanism to detect or correct deviations from safe behavior.
3. **Supervisory control is the right frame for AI safety.** The model is the primary controller (performance); the supervisory layer is the safety controller (constraint enforcement).
4. **Supervisory controls must be external, capable of override, and deterministic.** These three properties distinguish real controls from soft constraints.
5. **Stability is the key property.** A safe AI system must be stable — it must converge to safe behavior and maintain it under disturbance.
6. **The control hierarchy mirrors safety priorities.** Prevention > Detection > Response > Recovery, from most to least desirable, maps directly to the supervisory control hierarchy.
7. **Every concept is actionable.** Each control-theoretic element tells you exactly what to build, what to test, and what to monitor.

---

*Lesson 02 | AI Security from Scratch | Phase 1 — Foundations*
