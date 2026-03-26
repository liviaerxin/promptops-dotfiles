---
name: recap
description: Compress and summarize the current chat session to prevent context rot. Use this every 30 minutes, before a break, when approaching token limits, or when the user says "recap", "status", "save progress", "summarize session", "context dump", or "what have we done". Also trigger when the user wants to start a fresh session and carry over progress. Outputs a compact state block the user can paste into a new session.
---

# Recap Skill

Produces a **Session State Block** — a token-efficient summary of the current session that can be pasted into a new chat to resume instantly.

## Output Format

Write a markdown block with this exact structure:

```
## SESSION STATE — [date]

### Goal
One sentence: what are we building/solving?

### Completed
- [done item 1]
- [done item 2]

### In Progress
- [current task and where it's at]

### Blocked / Decisions Pending
- [anything unresolved]

### Key Files
- `path/to/file.ext` — what it does

### Next Action
Exactly one sentence: what to do first in the new session.
```

## Rules

- **Narrative, not transcript.** Summarize outcomes, not conversation turns.
- **Keep it under 200 words.** If it's longer, cut.
- **Omit dead ends.** Don't include approaches that were abandoned.
- **Next Action must be concrete.** "Continue building X" is bad. "Add error handling to `auth.ts` login function" is good.

## Usage

After outputting the block, tell the user:
> "Copy this block, start a new chat, and paste it. Say 'load state' to resume."