---
name: foam-capture
description: Extracts a chat conversation or URL into a structured Foam PKG note ready to save into VS Code + GitHub. Trigger when the user says "save to foam", "capture to knowledge base", "save this chat", "add to PKG", "save to foam vault", "log to foam", or pastes a Claude/ChatGPT URL or raw markdown chat they want to preserve. Fetches the URL if provided, then generates a complete Foam-ready .mdx file with auto-generated frontmatter — title, tags, description, keywords — based on the content. Reads live templates from .foam/templates/ if available, falls back to hardcoded templates.
---

# Foam Capture Skill

Turns a raw chat (pasted markdown or public URL) into a production-ready Foam `.mdx` note.

---

## Step 0 — Classify: Blog or Doc?

| Pick `blog` if... | Pick `doc` if... |
|---|---|
| Opinion, lesson learned, narrative, reflection | Reference, spec, how-to, architecture, definition |
| "Here's what I discovered..." | "Use X when..." |
| Dated, personal voice, dev-blog feel | Evergreen, authoritative, docs-site feel |

**User override always wins** — "make it a blog post" or "make it a doc" skips classification.

Then load the live template: Blog → `.foam/templates/blog.md` · Doc → `.foam/templates/doc.md`
Found → use it. Not found or web UI → use fallbacks below. Always tell the user which was used.

---

## Step 1 — Get Content

- **URL provided** → fetch via `web_fetch`, strip chrome/nav/buttons
- **Markdown pasted** → use directly

---

## Step 2 — Extract Metadata

| Field | How |
|---|---|
| `title` | Central topic — concise, title-case, Googleable |
| `tags` | 3–6 specific terms (✅ `context-rot` ❌ `ai`) |
| `description` | One sentence — lesson learned (blog) or what it documents (doc) |
| `keywords` | Tags + 1–2 more granular terms |
| `slug` | Lowercase title, spaces → `-` |
| `draft` | `true` if exploratory, `false` if resolved |

---

## Step 3 — Write the Note

### Blog Style — first-person, opinionated, narrative, prose-first

```
## The Problem       ← past tense, set the scene
## What I Found      ← 3–5 insights as prose paragraphs, each with an example
## The Takeaway      ← one quotable paragraph
## Watch Out For     ← optional: gotchas and surprises
## Related           ← [[wiki-links]]
## Source            ← URL or "Chat session — [date]"
```

### Doc Style — third-person, authoritative, structure-first, scannable

```
## Overview          ← 2–3 sentences, no opinion
## When to Use This  ← specific bullet triggers
## How It Works      ← numbered steps or structured prose + code blocks
## Key Concepts      ← term/definition table
## Constraints       ← what breaks this, hard limits
## Related           ← [[wiki-links]]
## Source            ← URL or "Chat session — [date]"
```

---

## Step 4 — Output Summary

```
📁 Save to:   blog/[slug].mdx  OR  docs/[slug].md
🏷️  Tags:     [list]
🔗 Links:     [[wiki-link-1]], [[wiki-link-2]]
🎨 Style:     Blog (narrative) OR Doc (reference)
📋 Template:  live OR built-in fallback
```

---

## Fallback Templates

### Blog
```mdx
---
authors:
  - frank
tags: [tag1, tag2, tag3]
description: [lesson-learned sentence]
keywords: [kw1, kw2]
image: https://i.imgur.com/mErPwqL.png
date: YYYY-MM-DD
draft: false
enableComments: true
---
# [Title]
> [Core insight — make it quotable.]
<!--truncate-->
## The Problem
## What I Found
## The Takeaway
## Watch Out For
## Related
## Source
```

### Doc
```md
---
title: [Title]
tags: [tag1, tag2]
description: [what this documents]
keywords: [kw1, kw2]
date: YYYY-MM-DD
draft: false
---
# [Title]
> [One-line summary.]
## Overview
## When to Use This
## How It Works
## Key Concepts
## Constraints
## Related
## Source
```

---

## Rules
- Distill signal only — never dump raw transcript
- Every note needs at least one `[[wiki-link]]` — orphan notes break the graph
- Content spans 2+ distinct topics → tell user to split into separate notes
- Live template has extra frontmatter fields → keep and fill them in