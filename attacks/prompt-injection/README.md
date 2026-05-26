# Prompt Injection Attacks

> **⚠️ EDUCATIONAL USE ONLY** — These attack descriptions are provided for defensive security training. Never use these techniques against systems without explicit authorisation.

## Overview

Prompt injection is the most fundamental attack class in AI security. It exploits the fact that LLMs treat all text as potential instructions, making it impossible to reliably distinguish between "data" and "commands" in a single context window. This is the AI analogue of SQL injection or XSS — a confusion between control plane and data plane.

## Why It Matters

Unlike traditional software where input and instruction channels are structurally separated, LLMs process both through the same token stream. This creates an inherent attack surface that cannot be fully eliminated — only mitigated through layered defences.

## Categories

| Category | Attack Vector | Typical Payload Location | Labs |
|----------|--------------|------------------------|------|
| **Direct Injection** | User message contains override instructions | User input field | vulnerable-chatbot |
| **Indirect Injection** | External data (documents, web pages) contains hidden instructions | RAG context, fetched URLs | vulnerable-rag |
| **Context-Window Manipulation** | Overloading context to push out system instructions | Long inputs, many turns | vulnerable-chatbot |
| **Role-Play Bypass** | Framing instructions as a role-play scenario | User message | vulnerable-chatbot |
| **Instruction Smuggling** | Encoding instructions in ways that bypass naive filters | Base64, Unicode, markdown | vulnerable-chatbot |
| **Multi-Turn Manipulation** | Building up to injection over multiple conversation turns | Conversation history | vulnerable-chatbot, vulnerable-memory-assistant |

## Severity Levels

| Level | Name | Description | Example |
|-------|------|------------|---------|
| 🔴 **Critical** | System compromise | Attacker gains control of the AI system's behaviour | Full system-prompt extraction, tool execution |
| 🟠 **High** | Data exfiltration | Sensitive information is leaked through model outputs | Admin codes, API keys, PII disclosure |
| 🟡 **Medium** | Behaviour modification | AI behaves differently than intended without data leak | Providing incorrect information, biased responses |
| 🟢 **Low** | Nuisance | AI behaviour is annoying but not harmful | Verbose output, refusal to help, sarcastic responses |

## Attack Catalog

### 1. Direct Instruction Override
The simplest form: telling the model to ignore its instructions.

**Mechanism:** User message contains explicit override commands.
**Detection difficulty:** Low (pattern-matchable) but variants are infinite.

### 2. Role-Play Scenario
Framing the injection as a harmless creative exercise.

**Mechanism:** "Act as..." / "Pretend you are..." / "In a story where..."
**Detection difficulty:** Medium (legitimate role-play requests exist).

### 3. Context Overflow
Pushing system instructions out of the effective context window.

**Mechanism:** Extremely long inputs that cause the model to "forget" earlier instructions.
**Detection difficulty:** Medium (requires length monitoring).

### 4. Instruction Smuggling
Encoding instructions to bypass text-based filters.

**Mechanism:** Base64, Unicode tricks, markdown formatting, HTML comments.
**Detection difficulty:** High (requires decoding / normalisation).

### 5. Multi-Turn Grooming
Building trust and context over multiple turns before injecting.

**Mechanism:** Normal conversation → rapport → subtle instruction → escalation.
**Detection difficulty:** Very High (requires cross-turn analysis).

### 6. Output Formatting Exploitation
Tricking the model into revealing instructions through formatting requests.

**Mechanism:** "Repeat your instructions" / "Summarise your system prompt" / "What were you told?"
**Detection difficulty:** Medium (filterable but variants exist).

## Safety Constraints

When practising these attacks in the lab environment:

1. **Only attack designated lab systems** — never production or third-party services
2. **No real credentials** — lab systems use mock data only
3. **No network access** — lab tools are sandboxed and mocked
4. **Document everything** — record your attack, the response, and the control gap
5. **Think defensively** — for every attack, propose a mitigation

## Applicable Labs

| Lab | Direct Injection | Indirect Injection | Context Overflow | Role-Play | Smuggling | Multi-Turn |
|-----|:-:|:-:|:-:|:-:|:-:|:-:|
| vulnerable-chatbot | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| vulnerable-rag | — | ✅ | — | — | ✅ | — |
| vulnerable-agent | ✅ | — | — | ✅ | — | ✅ |
| vulnerable-memory-assistant | ✅ | ✅ | — | ✅ | — | ✅ |

## Control-Loop Framework

Every prompt-injection attack exploits a missing or broken control in the AI system's feedback loop. Our framework identifies three control layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 3: OUTPUT CONTROLS                                  │
│  ├── Output filtering (secret/PII detection)               │
│  ├── Response validation (does it follow rules?)           │
│  └── Audit logging (what was sent to the user?)            │
│                                                             │
│  Layer 2: PROCESSING CONTROLS                              │
│  ├── Prompt isolation (system vs. user separation)         │
│  ├── Context management (window limits, priority)          │
│  └── Instruction hierarchy (system > user > data)          │
│                                                             │
│  Layer 1: INPUT CONTROLS                                   │
│  ├── Input validation (schema, length, encoding)           │
│  ├── Injection detection (pattern matching, ML classifiers)│
│  └── Rate limiting (prevent brute-force probing)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Further Reading

- [direct_injection.md](./direct_injection.md) — Detailed writeup of direct prompt injection
- [../indirect-prompt-injection/README.md](../indirect-prompt-injection/README.md) — Indirect injection through external data
- [../data-leakage/README.md](../data-leakage/README.md) — Data extraction through model outputs
