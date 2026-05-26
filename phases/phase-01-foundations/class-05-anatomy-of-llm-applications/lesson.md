# Lesson: Anatomy of LLM Applications

## 1. Overview of LLM Application Components

An LLM application is an assembled system of discrete components that work together to process user requests, generate responses, and interact with external systems. Understanding each component — its purpose, its inputs, its outputs, and its failure modes — is the foundation for securing the entire system.

### 1.1 Prompts and Prompt Templates

Prompts are the instructions and context that govern LLM behavior. In production applications, prompts are rarely static strings typed directly by users. Instead, they are **assembled from templates** that combine system instructions, user input, retrieved context, and conversation history into a single sequence of tokens fed to the model.

A prompt template typically contains:

- **System prompt**: Immutable instructions defining the LLM's role, capabilities, and constraints
- **User input slot**: A variable portion where user-supplied text is inserted
- **Context slot**: A variable portion where retrieved documents or tool results are injected
- **History slot**: A variable portion containing prior conversation turns
- **Formatting markers**: Delimiters and structural elements that separate these sections

The security implication is immediate: **every slot in a prompt template is an injection vector**. User input can contain instructions that override the system prompt. Retrieved documents can contain prompt injections embedded in text. Conversation history can accumulate adversarial content across turns. The template itself — the boundaries between sections — is the first and most critical trust boundary in the entire application.

When a prompt template concatenates these elements without proper escaping or delimiter enforcement, the LLM cannot reliably distinguish between instructions from the developer (the system prompt) and data from untrusted sources (user input, retrieval results). This ambiguity is the root cause of direct and indirect prompt injection attacks.

### 1.2 Context Management

Context management governs what information is available to the LLM at inference time and how that information is organized within the context window. This component controls:

- **Context window allocation**: How the fixed-size token budget is divided among system instructions, conversation history, retrieved documents, and generated output
- **Context prioritization**: Which information is retained when the context window is full — older turns, less relevant documents, or lower-priority instructions
- **Context isolation**: Whether different sources of context (user input vs. retrieved documents vs. tool results) are separated by clear boundaries or interleaved without distinction

The context window is a finite resource, and how it is managed has direct security consequences. If conversation history is prioritized over system instructions, an attacker can gradually fill the context with adversarial content that pushes safety instructions out of the window. If retrieved documents are not isolated from the instruction space, a poisoned document can inject commands that the LLM executes. If context truncation removes safety instructions while retaining adversarial content, the system becomes vulnerable precisely when it appears to be functioning normally.

### 1.3 Retrieval (RAG)

Retrieval-Augmented Generation (RAG) extends the LLM's knowledge by fetching relevant documents from an external knowledge base and injecting them into the prompt context. The retrieval pipeline typically includes:

- **Query generation**: The user's request (or a derived query) is used to search a document store
- **Embedding and search**: The query is embedded into a vector space, and semantically similar documents are retrieved from a vector database
- **Relevance scoring**: Retrieved documents are ranked by similarity to the query
- **Context injection**: Top-k documents are formatted and inserted into the prompt template

Retrieval is one of the most dangerous components in an LLM application from a security perspective because it introduces an **indirect attack vector**. An attacker who can influence the content of the retrieval corpus — by uploading malicious documents, by poisoning the vector index, or by manipulating the query to retrieve specific adversarial documents — can achieve prompt injection without ever directly interacting with the prompt template. The LLM treats retrieved documents as authoritative context, making it exceptionally difficult to distinguish legitimate retrieved information from adversarial instructions disguised as documents.

Furthermore, the retrieval component creates a feedback loop: the LLM's output may influence future retrieval queries, which means a successful injection can compound itself across turns by steering subsequent retrieval toward more adversarial content.

### 1.4 Tool Use (Function Calling)

Tool use — also called function calling, tool execution, or agent actions — allows the LLM to interact with external systems. When the LLM determines that it needs to perform an action beyond text generation (query a database, send an email, execute code, make an API call), it generates a structured tool-call request that the orchestration layer executes on its behalf.

The tool execution pipeline includes:

- **Tool definition**: A schema describing available tools, their parameters, and their expected outputs
- **Tool selection**: The LLM decides which tool to invoke based on the current context
- **Parameter generation**: The LLM generates the arguments for the selected tool
- **Execution**: The orchestration layer executes the tool with the provided parameters
- **Result integration**: The tool's output is returned to the LLM and incorporated into the next inference step

Tool use expands the LLM's action space from "generate text" to "take actions in the real world," which makes it simultaneously the most powerful and the most dangerous component. A compromised LLM that can execute tools can exfiltrate data, modify system state, interact with other users, and cause real-world harm. The tool execution boundary — the seam between the LLM's text output and the actual execution of an action — must be the most heavily guarded boundary in any LLM application.

Key security concerns include unauthorized tool invocation (the LLM calls a tool it should not), parameter manipulation (the LLM passes malicious arguments to a legitimate tool), result injection (a tool returns output that contains prompt injection), and privilege escalation (the LLM uses a low-privilege tool to gain access to higher-privilege operations).

### 1.5 Memory

Memory systems allow LLM applications to persist information across sessions and conversations. Memory can take several forms:

- **Short-term memory**: The current conversation context, maintained within the context window
- **Long-term memory**: Summaries or key facts extracted from conversations and stored in an external database for retrieval in future sessions
- **User profile memory**: Persistent information about a specific user's preferences, history, and permissions
- **Shared memory**: Information accessible across users, such as organizational knowledge bases

Memory introduces a unique security challenge: **corrupted memory persists and compounds**. If an attacker can inject malicious content into the memory store — through a carefully crafted conversation that causes the LLM to store adversarial instructions as "facts" — that corruption will affect all future interactions that draw from that memory. Unlike a single-turn prompt injection, memory corruption is persistent, cross-session, and potentially cross-user.

Memory also creates confidentiality risks: if the memory system does not properly enforce access controls, a user's private information stored in memory may be retrievable by other users or by the LLM in contexts where it should not be disclosed.

### 1.6 API Layer

The API layer is the external interface of the LLM application — the endpoints through which users (or other systems) submit requests and receive responses. This layer handles:

- **Authentication and authorization**: Verifying user identity and permissions
- **Rate limiting**: Controlling request frequency to prevent abuse
- **Input sanitization**: Pre-processing user input before it enters the LLM pipeline
- **Output filtering**: Post-processing LLM responses before they reach the user
- **Logging and auditing**: Recording requests, responses, and system actions

The API layer is the outermost boundary of the LLM application and often the only boundary that traditional security controls protect. However, it is insufficient as the sole security layer because many attacks exploit the semantic content of requests rather than their syntactic structure. A perfectly valid API request with proper authentication can still contain a prompt injection that exploits the LLM's behavior downstream.

---

## 2. How Each Component Is a Control-Loop Element

Viewing LLM application components through the lens of control theory reveals that each component serves a specific function in the control loop, and each function has corresponding failure modes.

**The LLM is the controller.** It receives observations (user input, context, tool results), processes them according to its internal model (weights + system prompt), and produces actions (text generation, tool calls). Like any controller, it can be corrupted by disturbances in its input signals — and unlike traditional controllers, its behavior is probabilistic and non-deterministic, making it harder to verify and predict.

**The prompt template is the reference signal.** The system prompt defines the desired operating behavior — what the controller should do. When the reference signal is overridden or diluted by disturbances (injected instructions), the controller produces outputs that deviate from the intended behavior.

**The retrieval system is a sensor.** It observes the external knowledge environment and feeds observations (retrieved documents) into the controller. Like any sensor, it can be spoofed — an attacker can poison the retrieval corpus to feed the controller false observations, causing it to make incorrect decisions.

**Tool execution is the actuator.** It converts the controller's output signals (tool calls) into physical actions (API calls, database queries, email sends). Like any actuator, it must be rate-limited, permission-checked, and monitored to prevent the controller from taking unsafe actions.

**Memory is the state store.** It maintains persistent state that influences future control decisions. Corrupted state leads to corrupted decisions — a fundamental control-theoretic principle.

**The API layer is the interface boundary.** It mediates between the external environment (users, other systems) and the internal control system. It is the first line of defense and the point where external disturbances enter the system.

---

## 3. Attack Surface at Each Boundary

Every boundary between components is an attack surface. Here we catalog the specific threats at each junction:

| Boundary | Attack Vector | Example |
|---|---|---|
| User → Prompt Template | Direct prompt injection | User input contains instructions that override system prompt |
| Retrieval → Context | Indirect prompt injection | Poisoned document contains hidden instructions |
| Context → LLM | Context confusion | Ambiguous delimiters cause LLM to treat data as instructions |
| LLM → Tool Executor | Unauthorized tool call | LLM generates tool call for restricted operation |
| Tool Result → Context | Tool-result injection | API response contains prompt injection payload |
| Memory → Context | Memory corruption | Stored adversarial content influences future interactions |
| LLM → Output | Data leakage | LLM reveals system prompt, retrieved documents, or other users' data |
| API → System | Traditional web attacks | Injection, authentication bypass, rate limit circumvention |

Each boundary requires its own set of controls: input validation at entry points, output filtering at exit points, authorization checks at action points, and integrity verification at storage points.

---

## 4. Why Defense-in-Depth Is Necessary

A single security control is never sufficient for an LLM application because attacks exploit the *interactions* between components, not individual components in isolation.

Consider indirect prompt injection through retrieval. Input validation at the API layer cannot prevent it because the injection payload enters through the retrieval system, not through user input. Output filtering at the API layer cannot prevent it because the LLM's behavior is already compromised — it may produce outputs that are individually benign but collectively harmful (e.g., calling tools in a sequence that exfiltrates data over multiple turns). The only effective defense is to validate and sanitize at *every* boundary: sanitize retrieved documents before injection, verify tool calls before execution, check LLM outputs for policy compliance before delivery, and monitor the entire system for anomalous behavior patterns.

Defense-in-depth for LLM applications means:

1. **Validate at every trust boundary** — Not just at the API layer, but at every junction between components
2. **Monitor continuously** — Not just inputs and outputs, but internal state changes, tool calls, and retrieval patterns
3. **Enforce least privilege** — Each component should have only the permissions it needs, and the LLM should never have unrestricted access to tools
4. **Assume compromise** — Design the system so that the compromise of any single component does not compromise the entire system
5. **Plan for recovery** — Have mechanisms to detect failures, contain damage, and restore safe operation

---

## 5. Common Architectural Mistakes

### 5.1 Trust Without Verification

The most common mistake is trusting LLM output without verification. When the LLM generates a tool call, the orchestration layer executes it without checking whether the call is authorized, whether the parameters are safe, or whether the action complies with policy. This is equivalent to allowing a controller to actuate any output without constraint — a fundamental violation of control-theoretic safety.

### 5.2 No Isolation Between Data and Instructions

Many LLM applications concatenate user input, retrieved documents, and system instructions into a single context without clear boundaries. The LLM cannot reliably distinguish instructions from data in this configuration, making prompt injection trivially easy. Proper isolation requires explicit delimiters, structural separation, and validation that data does not contain instruction-like content.

### 5.3 Unbounded Context and Memory

Applications that allow unbounded context growth — accumulating conversation history without summarization or truncation, storing all retrieved documents without relevance filtering — create a surface for context-window attacks. An attacker can fill the context with adversarial content that pushes safety instructions out of the window or overwhelms the LLM's ability to follow its original instructions.

### 5.4 Missing or Insufficient Logging

When LLM applications do not log internal operations — tool calls, retrieval queries, policy decisions — they create a blind spot that makes incident detection, forensic analysis, and continuous improvement impossible. You cannot secure what you cannot observe.

### 5.5 Monolithic Architecture

Applications that combine all components into a single process without clear interfaces or separation of concerns are impossible to secure because there are no boundaries at which to enforce controls. Each component should be independently deployable, independently testable, and independently securable.

---

## 6. Key Takeaways

1. **An LLM application is a control system**, and its security depends on understanding and hardening every component and every boundary in that system.
2. **Every slot in a prompt template is an injection vector.** Every variable portion of the prompt — user input, retrieval results, tool outputs, memory — is a potential entry point for adversarial content.
3. **Retrieval and memory are indirect attack surfaces** that bypass input validation at the API layer.
4. **Tool execution is the highest-consequence boundary** because it converts text output into real-world actions.
5. **Defense-in-depth is not optional** — no single control can secure an LLM application; you need layered controls at every boundary.
6. **Common architectural mistakes — trusting without verifying, failing to isolate data from instructions, unbounded context, insufficient logging, and monolithic design — create systemic vulnerabilities** that compound the inherent risks of LLM-based systems.
7. **Security boundaries must be explicit, enforced, and monitored.** Implicit trust between components is the root cause of most LLM application security failures.
