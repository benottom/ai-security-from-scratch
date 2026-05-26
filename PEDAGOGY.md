# Pedagogy: Think. Play. Do.

This course follows MIT 6.5950's three-pillar pedagogy — the same structure used to teach hardware security at MIT, adapted for AI security.

---

## The Three Pillars

### 🧠 Think — Lectures & Lessons

Each class opens with a **lesson** that develops the conceptual framework. Lessons are opinionated — they take positions, argue against common wisdom, and explain *why* the conventional approach is wrong. We don't hedge. We don't present every viewpoint equally. We present the control-theoretic viewpoint and show why it works.

Lessons include:
- **Concept Checks** — Quick questions between sections to verify understanding before moving on
- **Common Mistakes** — The specific errors that 90% of practitioners make, and why they're wrong
- **War Stories** — Real incidents analyzed through the control-theoretic lens (Chevrolet bot, Samsung leak, Air Canada ruling)

**Deliverable:** Each lesson ends with 5-7 key takeaways that are testable assertions, not vague aspirations.

### 🎮 Play — Notebooks & CTF Challenges

Every class has an **interactive Jupyter Notebook** where you run code, break things, and learn by doing. Notebooks use a simulated LLM so they work without API keys — but the attack behaviors match what real LLMs do in production.

In addition, each phase has a **CTF (Capture The Flag) challenge** modeled after MIT 6.5950's recitation format. CTFs are competitive, fun, and pedagogically precise — each flag teaches a specific control-loop concept.

CTF structure:
| Element | Detail |
|---|---|
| Flags | `AISec{...}` format, 4-5 per challenge |
| Scoring | 100 (Easy) → 200 (Medium) → 300 (Hard) → 500 (Expert) |
| Hints | 3 levels per flag, each reduces score by 25% |
| Reflection | Each flag requires identifying the control-loop element exploited |

**Deliverable:** Captured flags + control-loop analysis of how each exploit worked.

### 🔧 Do — Labs & Problem Sets

Labs follow the **Build → Attack → Defend → Test → Monitor → Assure** workflow on real, running systems. No simulations of attacks — you build the vulnerable app, you attack it, you watch it fail, you add the defense, you verify the fix.

Problem sets (psets) follow the MIT tradition:
- **Mathematical analysis** — Prove that defense-in-depth is exponentially more effective. Formalize safety bounds. Prove undecidability results.
- **Design problems** — Design a complete security architecture for a given AI system, specifying every control point and its implementation.
- **Short-answer questions** — Refute common misconceptions using control-theoretic reasoning. 300 words minimum.

**Deliverable:** Working code + evidence package + written analysis.

---

## Course Materials Structure

```
class-XX-topic/
├── README.md           # Overview + learning objectives
├── lesson.md           # 🧠 THINK: Conceptual framework
├── notebook.ipynb      # 🎮 PLAY: Interactive Jupyter notebook
├── lab.md              # 🔧 DO: Build/attack/defend lab
├── assignment.md       # Take-home design/analysis problem
├── control-loop-analysis.md  # Control-theoretic analysis template
└── threat-model.md     # STRIDE-AI threat model template
```

Plus cross-cutting materials:

```
ctf/                    # CTF challenges per phase
psets/                  # Problem sets with solutions
readings/               # Curated reading lists with focus questions
```

---

## Why This Structure Works

The three-pillar model addresses a specific failure mode in technical education: **the illusion of understanding.** Reading a lesson and nodding along feels like learning, but it's not. You understand a concept when you can apply it to a novel situation, predict what will happen, and explain why.

- **Think** gives you the framework (you can name the concepts)
- **Play** gives you the experience (you've seen the concepts in action)
- **Do** gives you the skill (you can apply the concepts independently)

Without Play, Think is abstract. Without Do, Play is shallow. Without Think, Do is blind. All three are necessary.

This is why MIT 6.5950's students learn hardware security by *actually attacking real CPUs* — not by reading about attacks. And it's why our students learn AI security by *actually attacking real AI systems* — not by reading about attacks.

---

## Assessment Philosophy

| Component | Weight | Purpose |
|---|---|---|
| CTF Challenges | 20% | Can you exploit control-loop gaps? |
| Problem Sets | 30% | Can you reason formally about security? |
| Labs | 40% | Can you build and defend real systems? |
| Reading Reflections | 10% | Can you connect theory to practice? |

Grading emphasizes **understanding over correctness**. A wrong answer with clear reasoning is worth more than a right answer with no justification. A partial defense that demonstrates understanding of the control-loop model is worth more than a complete defense that doesn't.

---

## Comparison with Traditional AI Security Courses

| Aspect | Traditional | This Course |
|---|---|---|
| Framework | Ad hoc checklists | Control-theoretic model |
| Hands-on | Read about attacks | Build → Attack → Defend → Test |
| Interaction | Watch lectures | Run notebooks + CTF challenges |
| Assessment | Multiple choice | Build real defenses + mathematical proofs |
| Output | "I know about prompt injection" | "I can build a system that resists prompt injection" |
| Theory | "Best practices" | Formal control theory + provable bounds |

---

## For Instructors

If you're using this material to teach, here's how to run each class:

1. **Before class:** Assign the reading list and the lesson (Think)
2. **In class (60 min):** Walk through the notebook together (Play), pausing for concept checks
3. **After class:** Students complete the lab and problem set independently (Do)
4. **Weekly:** Run a CTF session (30-60 min) for the current phase

The CTF sessions work best as group activities — students team up and compete. The collaborative debugging, the shared "aha" moments when a flag is captured, and the competitive motivation all enhance learning. This is why MIT 6.5950 uses the CTF format for recitations.

---

## For Self-Learners

If you're working through this alone:

1. Read the lesson first. Don't skip the concept checks.
2. Run the notebook. Modify the code. Try your own attacks.
3. Do the lab. It will take 1-2 hours per class.
4. Attempt the problem set. Check against the solutions.
5. Tackle the CTF challenges for fun and deeper understanding.

The CTF challenges are the closest thing to a "game" in this course. Treat them that way — experiment, be creative, and don't look at hints until you've tried for at least 15 minutes.

---

*AI Security from Scratch | Pedagogy*
*Think. Play. Do.*
