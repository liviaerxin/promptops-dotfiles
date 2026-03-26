# Knowledge Publishing Skill

A small prompt pack for turning conversations into publishable knowledge.

## Files
- `SKILL.md` -> top-level routing logic
- `0-extract_note.md` -> convert raw chat into a structured note
- `1-critique_reasoning.md` -> improve rigor and framing
- `2-generate_blog.md` -> create a blog draft
- `3-generate_short.md` -> create a concise note
- `4-generate_x.md` -> create X post + thread

## Recommended flow
1. extract_note
2. critique_reasoning
3. generate_blog
4. generate_short or generate_x

## Design principle
Unified entry, modular execution.

## Notes
Keep prompts short and editable.
Improve each file independently over time.
Do one stage at a time unless multi-stage output is explicitly requested.