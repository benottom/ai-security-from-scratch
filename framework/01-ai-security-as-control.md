# AI Security as the Control of Intelligent Behavior Under Adversarial Conditions

## A Definition

**AI security is the discipline of ensuring that an AI system's behavior remains within defined safe bounds, even when the system is subjected to adversarial disturbances.**

This definition has three load-bearing words:

1. **Behavior**: We care about what the system *does*, not what it *is*. A model that can theoretically produce harmful output but is constrained by supervisory controls from ever doing so is more secure than a model that is "aligned" but unconstrained. Security is a property of the running system, not the training pipeline.

2. **Safe bounds**: These must be explicitly defined before the system is deployed. "Don't be harmful" is not a safe bound; it is an aspiration. "Never execute a shell command without user confirmation" is a safe bound. "Never include PII in outputs" is a safe bound. Safe bounds are testable, enforceable, and auditable.

3. **Adversarial disturbances**: The system must maintain safe behavior not just under normal conditions, but when someone is deliberately trying to make it fail. This is the key insight that separates security from reliability. Reliability asks "does it work correctly?" Security asks "does it work correctly when someone is trying to break it?"

## AI Systems as Decision-Making Control Systems

An AI system is not a static artifact — it is a dynamic decision-making system that continuously:

1. **Observes** its environment (receives user input, retrieves documents, reads tool outputs)
2. **Decides** what to do (reasons over observations, selects actions, plans sequences)
3. **Acts** (generates text, calls tools, modifies state)
4. **Receives feedback** (gets tool results, reads user responses, updates memory)

This is precisely the structure of a control system. The AI model is the controller. The rest of the application — the retrieval pipeline, the tool interface, the memory store — is the plant (the system being controlled). The user and the environment provide reference signals (what the system should achieve) and disturbances (inputs designed to disrupt safe behavior).

In classical control theory, a controller's job is to drive the plant toward a desired state despite disturbances. The controller takes measurements, computes control signals, and applies them to the plant. If the measurements are wrong, the controller will make wrong decisions. If the control signals are corrupted, the plant will not do what the controller intended. If the plant's behavior is not what was expected, the feedback loop breaks.

Every one of these failure modes has a direct analog in AI security:

| Control Theory | AI Security | Example |
|---|---|---|
| Sensor failure | Observation corruption | RAG poisoning — the retrieval system returns a malicious document that misleads the model |
| Controller compromise | Reasoning manipulation | Prompt injection — an adversarial input overrides the system prompt and changes the model's behavior |
| Actuator failure | Unsafe actuation | Tool abuse — the model calls a dangerous API that it should not have access to |
| Feedback corruption | Memory poisoning | A previous conversation implants false information in the model's context, causing it to misbehave in future turns |
| Disturbance | Adversarial input | Any input designed to push the system into an unsafe state |

## Controller, Plant, and Disturbance in the AI Context

### The Controller

The controller is the AI model and its surrounding orchestration logic. This includes:

- The base model (e.g., GPT-4, Claude, Llama)
- The system prompt that defines the controller's objective and constraints
- The reasoning framework (chain-of-thought, ReAct, planning)
- The tool selection logic
- The conversation management logic

A compromised controller is the most dangerous failure mode because it affects every downstream decision. If an attacker can override the system prompt through prompt injection, they control the entire loop. This is why supervisory controls must exist *outside* the controller — they must be in a position to override it, not be part of it.

### The Plant

The plant is everything the controller acts upon:

- The retrieval pipeline (vector databases, search indices, document stores)
- The tool interfaces (APIs, databases, file systems, shell commands)
- The output channels (chat UI, email, file generation)
- The memory and state stores (conversation history, user profiles, long-term memory)

The plant has its own security properties. A tool that requires authentication is more secure than one that does. A retrieval pipeline that validates document provenance is more secure than one that does not. The security of the plant constrains the security of the entire system — no amount of controller cleverness can compensate for a plant that allows unrestricted execution.

### Disturbances

In control theory, a disturbance is any signal that pushes the system away from its desired state. In AI security, disturbances are adversarial inputs designed to make the system behave unsafely. These include:

- **Direct prompt injection**: User input contains instructions that override the system prompt
- **Indirect prompt injection**: Third-party content (retrieved documents, tool results, web pages) contains hidden instructions
- **Data poisoning**: The knowledge base contains malicious documents designed to mislead the model
- **Context overflow**: The input is designed to exceed the model's context window, causing it to lose track of its instructions
- **Social engineering**: The input manipulates the model through psychological tactics rather than technical exploits

The critical insight is this: **adversarial conditions are the normal operating environment.** Any AI system that is exposed to user input, retrieves data from untrusted sources, or interacts with external tools is under adversarial conditions by default. Designing for the happy path and adding security as an afterthought is the fundamental error.

## Concrete Examples

### Chatbot as Controller

A customer service chatbot is a controller that:
- Observes user messages
- Decides how to respond based on its training and system prompt
- Acts by generating text
- Receives feedback when the user sends another message

The disturbance is a user trying to extract the system prompt or make the bot say something inappropriate. The unsafe state is the bot revealing internal information or producing offensive content. The supervisory control is an output content filter. But if the filter is the only control, it is a single point of failure. A control-loop approach adds: input classification, conversation-level anomaly detection, and escalation to a human when the conversation enters uncertain territory.

### RAG as Observation System

A RAG system is a controller that:
- Observes user messages AND retrieved documents
- Decides how to answer based on the combined context
- Acts by generating text (and potentially calling tools)
- Receives feedback from tool results and user follow-ups

The critical new attack surface is the observation system. If the retrieval pipeline returns a malicious document — perhaps one injected by an attacker who gained write access to the knowledge base, or one that was crafted to match certain queries and contain hidden instructions — the controller will reason over corrupted observations and potentially produce compromised outputs. The supervisory control must include retrieval validation: checking document provenance, scanning retrieved content for instruction-like patterns, and separating retrieved content from the system prompt in the model's context.

### Agent as Actuator

An agent is a controller that:
- Observes user messages, retrieved information, and tool results
- Decides which tools to call and with what parameters
- Acts by invoking tools (APIs, code execution, file operations)
- Receives feedback from tool return values

The action space is now vast. A text-only chatbot can produce harmful text; an agent can delete files, send emails, execute arbitrary code, and make financial transactions. The supervisory controls must be commensurately stronger: tool call approval gates, parameter validation, execution sandboxing, and real-time monitoring of tool call patterns.

## The Shift: From "Secure the Model" to "Secure the Control Loop"

The dominant approach to AI security today is model-centric: make the model more aligned, more robust, more resistant to adversarial inputs. This is valuable but insufficient. A perfectly aligned model in an insecure control loop is still vulnerable — the attack simply targets the observation, feedback, or actuation stages instead of the model itself.

The control-loop approach is system-centric: secure every stage of the loop, add supervisory controls at every stage, monitor the entire loop, and design recovery procedures for when controls fail. This does not replace model alignment — it complements it. Alignment reduces the probability of unsafe behavior; supervisory controls bound the impact when unsafe behavior occurs despite alignment.

This is the same evolution that network security went through: from "secure the server" to "secure the network" to "secure the system." AI security needs to make the same jump, and control theory provides the conceptual framework to do it.
