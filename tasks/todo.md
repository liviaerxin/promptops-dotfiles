# Todo

- [x] Inspect current `ai` CLI behavior in `bin/ai`
- [x] Check the existing contract in `tests/test_ai_cli.py`
- [x] Research current 2026 instruction-file and skill-bundle patterns
- [x] Write a minimal recommendation for next features
- [x] Verify current CLI behavior with tests

## Review

Date: 2026-03-25

### What I Think You're Actually Solving

You want a very small personal promptops CLI that bootstraps a repo, injects only the skills you need, and stays compatible with the 2026 agent ecosystem without turning into a full package manager.

### The Real Risks

- `ai init` currently creates `.agents/AGENTS.md` and symlinks `CLAUDE.md`, but the repo story says project-critical instructions should live in `AGENTS.md`. That split will confuse whether instructions are runtime-only or meant to be committed.
- Discovery is weak. `ai list` is fine for a small repo, but once your personal skills and vendor skills grow, `ai add foo` becomes guesswork without search or completion.
- Bundles can become accidental package management if you add nesting, versions, remote sources, or dependencies too early.

### What You're Trading Away

| You gain | You give up |
|----------|-------------|
| Tiny CLI surface | Less automation than a marketplace-style installer |
| Local bundles | No versioning or dependency graph |
| Canonical `AGENTS.md` bootstrap | Slightly more opinionated `ai init` |

### What I'd Do Instead

Keep the product boring and add only four things:

1. Make `ai init` create a project-root `AGENTS.md` from one small template.
2. Keep `.agents/` as runtime-only wiring for skills and agent-specific folders.
3. Add `ai search <term>` and shell completion for `ai add` / `ai remove`.
4. Add one local `skill-bundles.json` file with one starter bundle, for example `basic`.

Suggested shape:

```json
{
  "basic": ["capture", "handoff", "recap"]
}
```

Suggested commands:

```bash
ai init
ai search review
ai add capture
ai add --bundle basic
ai completion zsh
```

### Verdict

Proceed with modifications.

The idea is good, but the right v1 is a cleaner bootstrap story plus better discovery, not more system complexity.

## Recommended Minimal Scope

### Build Now

- `ai init` should create `AGENTS.md` in the project root if missing.
- Keep `CLAUDE.md` compatibility via symlink only if it helps Claude Code.
- Add `ai search <term>` over personal and vendor skills.
- Add `skill-bundles.json` in this repo, not per project.
- Add `ai add --bundle <name>`.
- Add shell completion generation for `zsh` first.

### Skip For Now

- Remote registries
- Bundle inheritance
- Bundle versioning
- Per-skill metadata databases
- Interactive TUI selection
- Network install flows

## Verification

- Ran `pytest tests/test_ai_cli.py`
- Result: `10 passed in 0.95s`

## Implementation Plan

- [x] Add `ai sync` as the manifest restore verb and keep `install` as a compatibility alias
- [x] Add namespaced refs in `.agentic.json` for local and vendor skills
- [x] Add `skill-bundles.json` support and `ai add --bundle <name>`
- [x] Update tests to cover refs, bundles, and `sync`
- [x] Update docs to reflect the new command contract

## Research Notes

- AGENTS.md is now a broad open format used across many coding agents: https://agents.md/
- Anthropic Claude Code documents project memory in `./CLAUDE.md` and supports bootstrapping with `/init`: https://docs.anthropic.com/en/docs/claude-code/memory
- Anthropic Claude Code also supports custom project commands as Markdown files in `.claude/commands`: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/common-workflows
- Your bundled vendor repo already uses curated bundles as a first-class concept: `vendor/antigravity-awesome-skills/docs/users/bundles.md`

## Final Verification

- Ran `pytest tests/test_ai_cli.py`
- Result: `11 passed in 1.24s`

## Completion Follow-up

- [x] Add `ai completion zsh`
- [x] Reuse existing skill, bundle, and active manifest helpers for completion candidates
- [x] Add tests for completion output and dynamic candidate lists

## Latest Verification

- Ran `pytest tests/test_ai_cli.py`
- Result: `13 passed in 1.61s`

## Installer Follow-up

- [x] Update `bin/install-ai` to append `eval "$(<installed-ai> completion zsh)"` to `~/.zshrc`
- [x] Keep `~/.bashrc` limited to PATH updates only
- [x] Verify installer behavior in a temporary HOME

## CLI Follow-up

- [x] Change vendor add flow to `ai add --vendor <repo> <skill>`
- [x] Replace brittle `vendor:` completion with repo-scoped vendor completion
- [x] Add descriptions for top-level `ai <TAB>` command completion
- [x] Update tests and docs to match the new contract

## Template Follow-up

- [x] Add `templates/AGENTS.md` as the project bootstrap source
- [x] Update `ai init` to copy from the AGENTS template
- [x] Verify init behavior in tests

## Latest Verification

- Ran `pytest tests/test_ai_cli.py`
- Result: `18 passed in 2.01s`

## Repo Rename Follow-up

- [x] Confirm the repo-facing name and short description to adopt
- [x] Update the README title, summary, and example clone paths
- [x] Verify the repo-facing rename is reflected consistently in current docs
- [ ] Collapse local git history to one commit for the new repo bootstrap

## Repo Rename Review

Date: 2026-03-25

- Scope kept intentionally narrow: repo-facing branding changed to `promptops-dotfiles`.
- Internal command names and manifest conventions such as `ai` and `.agentic.json` remain unchanged to avoid mixing branding edits with behavior changes.
- Verification: `.venv/bin/pytest tests/test_ai_cli.py` passed with `18 passed in 1.83s`.

## Vendor Index Follow-up

- [x] Define the repo-level completion contract for third-party skill repos
- [x] Add `skills_index.json` support to vendor repo completion
- [x] Add an example `skills_index.json` to this repo
- [x] Verify the new index path and fallback behavior in tests

## Vendor Index Review

Date: 2026-03-25

- Third-party repos can now publish `skills_index.json` at repo root and have `ai add --vendor <repo> <TAB>` use it directly.
- Backward compatibility is preserved for `skills-index.json` and for repos with no index file.
- Verification: `.venv/bin/pytest tests/test_ai_cli.py` passed with `19 passed in 2.10s`.
