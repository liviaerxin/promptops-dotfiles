---
name: requirements-capture
description: >
  Capture OR refine requirements from a conversation into docs/specs/requirements.md.
  Trigger on CAPTURE: "capture this requirement", "add requirement", "log this feature",
  "write this up as a requirement", "save this to specs", "requirement for X", or when a
  conversation has settled on what to build and needs to be recorded before coding starts.
  Trigger on REFINE: "refine this requirement", "improve the spec", "tighten FR-xxx",
  "this requirement is too vague", "fill in the gaps", "make this clearer", "review my spec",
  "what's missing from this requirement", or when the user pastes a rough or incomplete
  requirement and wants it made implementation-ready.
  Never starts implementation — output is always a spec only.
---

# Requirements Capture & Refine Skill

Two modes — detect from context:

| Mode | When | Output |
|------|------|--------|
| **CAPTURE** | New feature discussed in conversation, nothing written yet | New FR entry appended to requirements.md |
| **REFINE** | Existing rough/vague requirement pasted or referenced | Improved version of that same entry, with change notes |

For small/solo projects: one file, sections per feature.
For larger projects: one file per feature under `docs/specs/<feature>.md`.
Default to one file unless the project already has per-feature files.

---

## MODE: CAPTURE

### Step 1 — Extract from Conversation

Read the conversation and identify:
- What the user wants to build (the feature)
- Any constraints or non-goals mentioned
- Any acceptance signals ("it should...", "must...", "fail clearly if...")
- Any open questions still unresolved

Do NOT ask clarifying questions unless a field is completely missing and cannot be inferred.
Make a best-effort draft — the human will review it.

---

### Step 2 — Assign an ID

Check `docs/specs/requirements.md` for existing FR-xxx entries.
Assign the next available ID. Start at FR-001 if file is new.

NFR (non-functional) requirements get NFR-xxx IDs.

---

## Output Format

Append this block to `docs/specs/requirements.md`:

```markdown
---

## [Feature Name]

**FR-[N]** — [One sentence: what must be true]  
**Status:** Draft  
**Priority:** P[0/1/2]  

### Description
2–3 sentences. What does this feature do and why does it exist?

### Scope
- IN: [what is included]
- OUT: [what is explicitly not included]

### Acceptance Criteria
- [ ] [Concrete, testable condition]
- [ ] [Concrete, testable condition]
- [ ] [Failure path: what happens when X is missing or wrong]

### Constraints
- [Performance, platform, dependency constraints if any]

### Open Questions
- [ ] [Unresolved question that needs human decision before coding]

### Assumptions
- [What was assumed to fill gaps in the conversation]
```

---

## MODE: REFINE

Takes a rough, vague, or incomplete requirement and makes it implementation-ready.
Can work from: a pasted FR block, a referenced FR-xxx ID, or a rough paragraph the user typed.

### Step 1 — Diagnose What's Weak

Check the existing requirement against this list and note every gap:

| Check | Problem if missing |
|---|---|
| Acceptance criteria present? | Agent has no done-condition |
| At least one failure/edge case in AC? | Happy path only — will break in prod |
| Scope IN/OUT defined? | Agent will guess boundaries |
| Open Questions resolved or listed? | Silent assumptions get baked in |
| Constraints specified? | Performance/platform surprises later |
| Ambiguous verbs? ("handle", "support", "manage") | Agent interprets freely |
| Testable language? ("must", "shall" vs "should", "nice to have") | Untestable AC |

### Step 2 — Rewrite

Produce a refined version of the full FR block using the same output format as CAPTURE.

### Step 3 — Show a Change Summary

After the refined block, always append:

```markdown
### Refinement Notes
- **Added:** [what was missing and is now included]
- **Clarified:** [what was vague and is now precise]
- **Assumed:** [gaps filled by inference — human should verify]
- **Still open:** [anything that genuinely needs human input before Approved]
```

### Refine Rules

- Keep the same FR-xxx ID — do not renumber
- Reset Status to `Draft` if it was `Approved` — a refinement invalidates prior approval
- Never silently drop scope — if something in the original was removed, explain why in Refinement Notes
- If the original had no problems, say so briefly and do not pad the output

---

## Rules (Both Modes)

- **Status options:** Draft → Approved → In Progress → Done → Deprecated
- Status is always `Draft` on first capture — human must change it to `Approved`
- Acceptance criteria must include at least one failure/edge case
- Open Questions must be listed even if empty (write "None" if so)
- Assumptions section is required — makes implicit reasoning explicit
- Write for a future coding agent with zero conversation context
- Never include implementation details unless the user explicitly specified them
- If `docs/specs/requirements.md` does not exist, create it with this header first:

```markdown
# Requirements

> Status legend: Draft → Approved → In Progress → Done → Deprecated  
> All requirements must reach **Approved** before implementation begins.

```

---

## After Writing (Both Modes)

1. Save to `docs/specs/requirements.md` (or per-feature file if that pattern exists)
2. Present the file with `present_files`
3. Call out **Open Questions** and **Still Open** items explicitly
4. If REFINE reset Status to Draft, remind the human to re-approve before coding resumes
5. Remind: "Set Status to **Approved** when ready for an agent to implement"

Do NOT generate a task list, test plan, or implementation — those are separate skills.