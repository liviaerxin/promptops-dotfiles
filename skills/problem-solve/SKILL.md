---
name: problem-solver
description: >
  Use this skill whenever the user presents a complex problem, challenge, or decision that
  needs structured thinking. Trigger on: "help me solve", "I have a problem", "how do I fix",
  "I'm stuck on", "figure this out", "think through this with me", "what should I do about",
  "break this down", "analyze this situation", "help me decide", "complex issue", "root cause",
  "what's going wrong", or any situation where jumping straight to an answer would skip
  important reasoning. Works for technical, business, strategic, personal, and creative problems.
  Always follow all 7 steps — never skip steps, even if the answer seems obvious.
---

# Problem Solver — 7-Step Structured Framework

Work through any complex problem using a rigorous 7-step method. Think like a consultant,
engineer, and strategist combined. Show your reasoning at each step.

---

## The 7 Steps

### Step 1 — Formalize the Problem
Restate the problem in your own words as a single crisp sentence.
Then answer:
- What does success look like? (definition of "solved")
- What are the hard constraints? (time, budget, people, technology)
- What is explicitly out of scope?

> **Output**: A 3–5 line problem statement the user can confirm before you proceed.
> Ask: *"Does this capture the problem correctly?"* — wait for confirmation on ambiguous problems,
> proceed immediately on clear ones.

---

### Step 2 — Decompose into Sub-Tasks
Break the problem into its independent components using a MECE structure
(Mutually Exclusive, Collectively Exhaustive — no overlaps, no gaps).

- List 3–7 sub-tasks or sub-questions
- For each, note: what needs to be true / known / done for this piece to be resolved
- Draw a simple tree if the structure is hierarchical

> **Output**: Numbered sub-task list with one-line descriptions.

---

### Step 3 — Prioritize
Rank the sub-tasks by two criteria:
- **Impact**: How much does solving this unblock everything else?
- **Effort**: How hard is this to resolve?

Use a simple 2×2 (High/Low Impact × High/Low Effort) to identify:
- **Quick wins** (High impact, Low effort) → tackle first
- **Critical path** (High impact, High effort) → plan carefully
- **Deprioritize** (Low impact) → flag and defer

> **Output**: Ordered list with impact/effort labels. State the recommended starting point.

---

### Step 4 — Analyze (Root Cause)
For each high-priority sub-task, go deeper:
- Apply **5 Whys** for process/people problems
- Apply **fault tree analysis** for technical/system problems
- Apply **assumption mapping** for strategic/decision problems

Distinguish between:
- **Symptoms** (what you can see)
- **Root causes** (what's actually driving it)
- **Contributing factors** (making it worse but not the origin)

> **Output**: Root cause summary per high-priority item. Flag any assumptions that need validation.

---

### Step 5 — Synthesize Solutions
Generate at least 3 distinct solution options — resist jumping to the first idea.

For each option:
| Option | Core idea | Pros | Cons | Risk |
|--------|-----------|------|------|------|

Then recommend the best option with a clear rationale. If a hybrid is better, say so explicitly.

> **Output**: Options table + recommendation with 2–3 sentence justification.

---

### Step 6 — Validate the Logic
Before committing to the recommendation, stress-test it:
- **Pre-mortem**: "It's 6 months later and this failed — what happened?"
- **Counterargument**: What's the strongest case *against* this recommendation?
- **Dependencies**: What must be true for this to work?
- **Reversibility**: Is this decision easy or hard to undo?

If the recommendation survives scrutiny, proceed. If not, revise Step 5.

> **Output**: 3–5 bullet validation check. Note any changes to the recommendation.

---

### Step 7 — Recommend & Action Plan
Deliver a concrete, executable plan:

```
Recommendation: [one sentence]

Action Plan:
  Phase 1 — [Name] (timeframe)
    [ ] Task — Owner — Deadline
    [ ] Task — Owner — Deadline

  Phase 2 — [Name] (timeframe)
    [ ] Task — Owner — Deadline

Success metrics:
  - How will you know it's working?

Decision points:
  - When and what to re-evaluate
```

> **Output**: Full action plan. Keep it concrete — no vague verbs like "explore" or "consider".

---

## Formatting Rules

- Show each step as a visible header (`### Step N — Name`)
- Be concise within steps — bullet points preferred over paragraphs
- Tables for comparisons (Step 5), lists for everything else
- Total response should feel like a structured consulting deliverable, not a chat answer
- If the problem is simple (< 3 sub-tasks), compress Steps 2–4 into one section but still cover all 7

## On Asking Questions

- **Ambiguous problem scope** → ask one clarifying question after Step 1, then proceed
- **Clear problem** → run all 7 steps without interruption
- Never ask more than one question at a time