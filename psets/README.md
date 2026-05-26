# Problem Sets

## The MIT Tradition

At MIT, problem sets are not homework — they are the primary vehicle for learning. A well-designed problem set does not ask you to regurgitate what you read; it asks you to *apply* it under conditions you have not seen before. The best problem sets are those where the solution is not obvious from the reading, but becomes obvious once you have genuinely understood the reading.

This tradition stretches back to the earliest days of MIT's curriculum. In 6.036 (Introduction to Machine Learning), problem sets require students to derive gradient updates from first principles, not plug them into a library. In 6.5950 (Secure Hardware Design), problem sets require students to identify timing side channels in real circuit designs, not memorize a taxonomy. In every case, the problem set is the crucible where understanding is forged.

We follow this tradition.

## Structure

Problem sets are released weekly, one per phase. Each problem set contains three types of problems:

1. **Mathematical Analysis** — Derivations, proofs, and calculations that build rigorous foundations. These are not exercises in symbol-pushing; they require you to connect mathematical structures to the physical systems they model.

2. **Design Problems** — Open-ended architecture and design challenges. You are given a real or realistic AI system and asked to design security controls for it. There is no single correct answer — there are answers that are more or less defensible, more or less complete, more or less principled.

3. **Short-Answer Questions** — Concise arguments that test conceptual understanding. A good short answer is not long; it is precise. It identifies the key insight, applies it, and stops.

## Submission and Collaboration

- Problem sets are due one week after release, before the start of the next class.
- Collaboration is encouraged; copying is not. You may discuss problems with peers, but you must write up your solutions independently and credit your collaborators.
- Solutions must be typed (LaTeX preferred; Markdown accepted). Hand-drawn diagrams must be scanned and embedded.

## Grading Philosophy

We grade for understanding, not correctness. A solution that reaches the wrong answer through sound reasoning will receive more credit than a solution that reaches the right answer through unsound reasoning. A solution that identifies an interesting edge case and addresses it will receive more credit than a solution that ignores it.

The grading rubric for each problem emphasizes:

| Criterion | Weight |
|-----------|--------|
| Correctness of approach | 40% |
| Completeness of analysis | 25% |
| Clarity of presentation | 20% |
| Handling of edge cases | 15% |

## Problem Set Schedule

| PSet | Phase | Title | Release | Due |
|------|-------|-------|---------|-----|
| 01 | Foundations | Control-Loop Security Architecture | Week 1 | Week 2 |
| 02 | Prompt Injection | Injection as Control-Loop Failure | Week 3 | Week 4 |
| 03 | RAG Security | Observation-Channel Security | Week 5 | Week 6 |
| 04 | Agent & Tool Security | Actuation-Channel Security | Week 7 | Week 8 |
| 05 | Memory & Feedback | Feedback-Channel Security | Week 9 | Week 10 |
| 06 | Data & Privacy | Data-Flow Security | Week 11 | Week 12 |
| 07 | Model & Supply Chain | Supply-Chain Security | Week 13 | Week 14 |
| 08 | Defensive Controls | Composing Layered Defenses | Week 15 | Week 16 |
| 09 | Security Testing | Validation & Verification | Week 17 | Week 18 |
| 10 | Observability & IR | Monitoring the Control Loop | Week 19 | Week 20 |
| 11 | Governance & Assurance | Building the Assurance Case | Week 21 | Week 22 |
| 12 | Capstone | End-to-End Secure AI System | Week 23 | Week 24 |

## Available Problem Sets

- [**PSet 01 — Foundations: Control-Loop Security Architecture**](./pset-01-foundations/) — Formalize the control-loop model, prove defense-in-depth properties, analyze real incidents, design a security architecture.
