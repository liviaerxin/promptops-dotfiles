---
name: conversation-to-plan
description: >
  Use this skill when the user wants to turn a conversation into an actionable plan.
  Trigger on: "make a plan from this", "convert this to a plan", "what's our plan",
  "turn this into steps", "create a roadmap from this", "plan this out", "next steps",
  "what do we need to do", or when a brainstorm/discussion naturally needs execution structure.
  Output a clean .md file with Docusaurus-compatible frontmatter.
---

# Conversation to Plan

Read the full conversation, extract intent, and output a single focused plan as a `.md` file.

## Output Structure

```markdown
---
title: "Plan: [Goal]"
date: YYYY-MM-DD
tags: [plan, relevant-tag]
---

# Plan: [Goal]

## Goal
One sentence — what success looks like.

## Phases
### Phase 1 — [Name]
- [ ] Task
- [ ] Task

### Phase 2 — [Name]
- [ ] Task

## Decisions Needed
- Open question or blocker

## Out of Scope
- What this plan explicitly does NOT cover
```

## Rules
- Infer everything from the conversation — never ask
- Tasks must be concrete and actionable (not "think about X")
- Keep phases to 2–4; tasks per phase to 3–6
- Omit any section that doesn't apply
- Save to `/mnt/user-data/outputs/plan-[slug].md` and use `present_files`