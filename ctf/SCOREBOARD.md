# CTF Scoreboard

## AI Security from Scratch — Flag Tracking Template

Copy this template to your own file (e.g., `my-scoreboard.md`) and fill it in as you capture flags. The reflection columns are as important as the flag itself — they build the analytical habits that transfer to real-world AI security work.

---

## Challenge 01: Control Loop Basics

| # | Flag | Technique Used | Control-Loop Element Exploited | Supervisory Control That Would Prevent This | Time Spent |
|---|------|---------------|-------------------------------|---------------------------------------------|------------|
| 1 | `AISec{_______________}` | | Observation | Input classification / prompt isolation | |
| 2 | `AISec{_______________}` | | Controller | Instruction hierarchy enforcement | |
| 3 | `AISec{_______________}` | | Feedback | Endpoint access control / state isolation | |
| 4 | `AISec{_______________}` | | Disturbance | Rate limiting / input length validation | |
| 5 | `AISec{_______________}` | | System-level | Cross-cutting anomaly detection | |

**Total points earned:** ______ / 1,200

**Reflection:**
- Which flag was the easiest? Why?
- Which flag was the hardest? What made it difficult?
- Did any flag surprise you? What did you learn from it?
- How would you redesign HelpBot to close all five gaps?

---

## Challenge 07: Direct Prompt Injection

| # | Flag | Technique Used | Control-Loop Element Exploited | Supervisory Control That Would Prevent This | Time Spent |
|---|------|---------------|-------------------------------|---------------------------------------------|------------|
| 1 | `AISec{_______________}` | | Observation → Controller | Input classification beyond blocklists | |
| 2 | `AISec{_______________}` | | Observation (encoding bypass) | Input normalization / decoding before filtering | |
| 3 | `AISec{_______________}` | | Controller (social engineering) | Instruction hierarchy enforcement / authority verification | |
| 4 | `AISec{_______________}` | | Controller + Feedback (context drift) | Context-aware monitoring / behavioral drift detection | |

**Total points earned:** ______ / 800

**Reflection:**
- How did the content filter create a false sense of security?
- Which injection technique felt most realistic (likely to work on production systems)?
- How does multi-turn injection change the threat model compared to single-shot attacks?
- What would a comprehensive defense look like that handles all four techniques?

---

## Cumulative Progress

| Challenge | Flags Captured | Total Flags | Points | Hints Used |
|-----------|---------------|-------------|--------|------------|
| 01 — Control Loop Basics | /5 | 5 | /1,200 | |
| 07 — Prompt Injection | /4 | 4 | /800 | |
| **Total** | **/9** | **9** | **/2,000** | |

---

## Defense Building Log

After capturing each flag, try implementing a defense. Record your results:

| Flag | Defense Implemented | Test Result (pass/fail) | Does defense break normal functionality? |
|------|-------------------|------------------------|------------------------------------------|
| 01-1 | | | |
| 01-2 | | | |
| 01-3 | | | |
| 01-4 | | | |
| 01-5 | | | |
| 07-1 | | | |
| 07-2 | | | |
| 07-3 | | | |
| 07-4 | | | |

---

## Key Insights

Use this space to record the most important things you learned from the CTF challenges. These insights should connect the "Play" experience back to the "Think" (theory) and prepare you for the "Do" (building defenses).

1.

2.

3.

4.

5.

---

*Scoreboard Template | AI Security from Scratch | CTF Framework*
