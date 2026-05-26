# CTF Challenge Framework

## AI Security from Scratch — Capture The Flag Challenges

Inspired by MIT 6.5950 Secure Hardware Design's **"Think, Play, Do"** pedagogy, the CTF (Capture The Flag) challenges are the **Play** pillar of this curriculum. They provide hands-on, adversarial environments where students exploit real vulnerabilities in deliberately insecure AI systems — and learn to defend them.

---

## Why CTF?

Reading about prompt injection is not the same as *doing* it. Watching a lecture on control-loop gaps does not build the muscle memory to spot them in production systems. CTF challenges bridge this gap:

- **Active learning** — Students attack real, running applications, not static examples.
- **Progressive difficulty** — Each challenge builds on the previous one, with escalating sophistication.
- **Control-theoretic framing** — Every flag maps to a specific control-loop element (observation, controller, feedback, disturbance, system-level), so students learn *why* the vulnerability exists, not just *how* to exploit it.
- **Safe environment** — All challenges run locally with mock LLMs. No API keys required. No real systems harmed.

---

## How It Works

### Flags

Every CTF challenge contains hidden **flags** — strings in the format `AISec{...}` that prove you successfully exploited a vulnerability. For example:

```
AISec{0b53rv4t10n_g4p_f0und}
```

Flags are embedded in the vulnerable application. To capture a flag, you must find it by exploiting the designated vulnerability — not by reading the source code.

### Scoring

| Difficulty | Points | Description |
|---|---|---|
| Easy | 100 | Single-step exploitation, minimal obfuscation |
| Medium | 200 | Multi-step or requires understanding of the control-loop concept |
| Hard | 300 | Requires chaining attacks or deep control-theoretic insight |
| Expert | 500 | System-level failure requiring synthesis of multiple concepts |

### Hints

Each flag comes with 3 levels of hints. Using hints reduces your score:

| Hint Level | Score Reduction |
|---|---|
| Hint 1 (gentle nudge) | -10% |
| Hint 2 (specific direction) | -25% |
| Hint 3 (near-solution) | -50% |

**Self-reported scoring is on the honor system.** The goal is learning, not leaderboard position.

---

## Challenge Environments

Each challenge is a self-contained FastAPI application with a Dockerfile for containerized deployment. No external API keys are needed — all LLM behavior is simulated by a **ToyLLM** that pattern-matches attack payloads to produce realistic "leaky" responses.

To run a challenge:

```bash
cd ctf/challenge-XX-name/
make setup   # install dependencies
make run     # start the server
```

Then interact with the API using `curl`, Postman, or the provided Makefile targets.

---

## CTF Challenges by Phase

| Phase | Challenge | Class | Flags | Difficulty Range | Control-Loop Focus |
|---|---|---|---|---|---|
| Phase 1 — Foundations | [01-control-loop-basics](challenge-01-control-loop-basics/) | Class 01: AI Security as Control | 5 | Easy → Expert | Full control loop |
| Phase 2 — Prompt Injection | [07-prompt-injection](challenge-07-prompt-injection/) | Class 07: Direct Prompt Injection | 4 | Easy → Hard | Observation & Controller |
| Phase 2 — Prompt Injection | *08-system-prompt-leakage* (coming soon) | Class 08: System Prompt Leakage | — | — | Observation |
| Phase 3 — RAG Security | *13-rag-poisoning* (coming soon) | Class 13: RAG Poisoning | — | — | Observation corruption |
| Phase 4 — Agent Security | *19-tool-abuse* (coming soon) | Class 19: Tool Abuse | — | — | Actuation |
| Phase 5 — Memory & Feedback | *25-memory-poisoning* (coming soon) | Class 25: Memory Poisoning | — | — | Feedback corruption |
| Phase 8 — Defensive Controls | *37-circuit-breaker* (coming soon) | Class 37: Circuit Breakers | — | — | System-level control |

---

## Tracking Your Progress

Use the [SCOREBOARD.md](SCOREBOARD.md) template to track which flags you've captured, the techniques you used, and the control-loop elements you exploited. This reflection is as important as the flags themselves — it builds the analytical habits that transfer to real-world AI security work.

---

## Rules of Engagement

1. **Attack the application, not the infrastructure.** These are software security challenges, not network penetration tests. Exploit the AI control loop, not the server.
2. **No source-code reading for flags.** The challenge is to find flags through interaction with the running application. Reading `app.py` to find flag strings defeats the purpose. (In a classroom setting, the instructor may provide a pre-built Docker image to enforce this.)
3. **Document your approach.** For each flag, record the technique you used and the control-loop element you exploited. This documentation is part of the learning.
4. **Share techniques, not flags.** Discussing *how* to approach a challenge is encouraged. Posting the actual flag strings is not.
5. **Build defenses after attacking.** After capturing each flag, try to implement a defense that would prevent the same attack. This is the "Do" part of "Think, Play, Do."

---

## Pedagogical Foundation

This CTF framework is grounded in three principles:

1. **Think** — Lecture content and readings provide the theoretical foundation (control theory, threat modeling, defensive design).
2. **Play** — CTF challenges provide the experiential learning, where students *experience* vulnerabilities firsthand.
3. **Do** — Assignments and labs require students to *build* defenses, closing the loop from vulnerability → understanding → mitigation.

Each CTF challenge is explicitly linked to a class lesson, so students can move fluidly between theory (Think) and practice (Play), then solidify their understanding by building (Do).

---

*CTF Framework | AI Security from Scratch*
