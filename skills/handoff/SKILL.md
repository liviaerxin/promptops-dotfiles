---
name: handoff
description: Generate a structured mission briefing to pass context from one agent or phase to the next. Use when the user says "handoff", "hand off", "pass to next agent", "move to next phase", "wrap up this phase", "prepare for coder/reviewer/architect", or when finishing a major workflow stage (planning → building, building → reviewing). Also trigger when switching tools (e.g. Claude → Cursor) or roles (e.g. Architect → Coder). Cleans out brainstorm noise and produces only what the next agent needs.
---

# Handoff Skill

Produces a **Mission Briefing** — a clean, opinionated brief for the next agent or phase. Strips dead ends, failed experiments, and chat noise.

## Output Format

```
## HANDOFF BRIEF — [From: Role/Phase] → [To: Role/Phase]

### Mission
What must be accomplished. One paragraph max.

### Constraints
- Hard rules the next agent must not violate
- (tech stack, style, performance budgets, etc.)

### Decisions Already Made
- [decision]: [why — one line]

### Artifacts Handed Over
- `file/path.ext` — state and what to do with it

### Do NOT Re-litigate
- [approach or idea that was consciously rejected and why]

### First Task
Single, unambiguous instruction to start immediately.
```

## Rules

- **Decisions Already Made** prevents the next agent from reopening closed loops.
- **Do NOT Re-litigate** is the most important section — fill it if anything was debated.
- Strip all exploratory chat. The next agent gets conclusions, not journey.
- Keep total length under 300 words.

## Usage

After the brief, tell the user:
> "Paste this at the top of your new agent session as the first message."