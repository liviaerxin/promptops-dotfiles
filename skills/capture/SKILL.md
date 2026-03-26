---
name: capture
description: Captures a new idea or approach as a structured task card and appends it to TODO.md in the project root. Trigger when the user says "capture this idea", "capture idea", "log this idea", "add to TODO", "save this for later", "let's track this", or after a technical discussion when the user wants to preserve an idea without implementing it immediately. Do NOT use recap for this — recap records what happened, capture records what to do next.
---

# Capture Skill

Turns a raw idea from the conversation into a structured task card, appended to `TODO.md` in the project root. Non-destructive — always appends, never overwrites.

---

## Output: Task Card

Write one card per idea in this format:

```markdown
---
## [Short idea title]

**Captured:** [date]  
**Priority:** High / Medium / Low  
**Effort:** Small (< 1 day) / Medium (1–3 days) / Large (3+ days)  
**Status:** 📋 TODO

### What & Why
2–3 sentences. What is the idea? Why does it matter or what problem does it solve?

### Tasks
- [ ] [concrete first action]
- [ ] [next step]
- [ ] [next step]

### Dependencies
- Needs: [what must exist first, or "None"]

### Notes
[Any tradeoffs, open questions, or context from the conversation — or leave blank]
```

---

## How to Write It

**Priority:**
- `High` — blocks progress or has outsized impact
- `Medium` — valuable but not urgent
- `Low` — nice to have, revisit later

**Effort:**
- `Small` — under a day, straightforward
- `Medium` — 1–3 days, some unknowns
- `Large` — 3+ days, needs further breakdown before starting

**Tasks** must be concrete actions, not vague intentions.
- ❌ "Implement the feature"
- ✅ "Add `POST /api/jobs` endpoint with validation schema"

---

## File Handling

- Target file: `TODO.md` in project root
- If file doesn't exist: create it with a `# TODO` header first
- Always **append** to the bottom — never edit existing cards
- After writing, confirm: "Captured → TODO.md"