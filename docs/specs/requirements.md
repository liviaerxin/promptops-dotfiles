# Requirements

> Status legend: Draft → Approved → In Progress → Done → Deprecated  
> All requirements must reach **Approved** before implementation begins.

---

## Minimal AI Skill CLI Management

**FR-001** — The `ai` CLI must let a project add, restore, and track local and vendor skills with explicit source provenance.  
**Status:** Approved  
**Priority:** P0  

### Description
The repository provides a personal promptops CLI for activating only the skills needed in a given project. The CLI must support a small, understandable workflow for adding local skills, adding vendor skills from a chosen vendor repo, restoring a project from its manifest, and grouping common skills into bundles without becoming a package manager.

### Scope
- IN: Add local skills, add vendor skills through an explicit vendor-repo flow, restore project skill links from a manifest, record skill and bundle provenance, and support named skill bundles
- OUT: Remote registries, dependency resolution, versioned packages, interactive TUIs, and network installs

### Acceptance Criteria
- [ ] `ai add <skill>` adds a local skill when the name is unique and records it in the manifest with explicit source metadata
- [ ] `ai add --vendor <repo> <skill>` adds a vendor skill from the selected vendor repo and records an explicit vendor ref in the manifest
- [ ] `ai sync` restores project skill links from the manifest, and `ai install` remains a compatibility alias for the same restore behavior
- [ ] `ai add --bundle <name>` adds all skills in the named bundle and records both the bundle and the resolved skill provenance in the manifest
- [ ] If a requested skill or bundle does not exist, the CLI exits non-zero and prints a clear error without partially claiming success

### Constraints
- Keep the CLI surface small and predictable
- Preserve a local-first workflow for personal skills
- Keep source provenance explicit in the manifest so local and vendor skills are distinguishable

### Open Questions
- [ ] None

### Assumptions
- The personal skill source of truth is the central repo `skills/` directory
- Vendor skills are sourced from repos under `vendor/`
- Projects consume skills through linked runtime artifacts rather than copying skill content into each project

### Refinement Notes
- **Added:** Explicit vendor-repo add flow via `ai add --vendor <repo> <skill>`
- **Clarified:** Vendor adds are repo-scoped rather than free-form prefixed refs in the primary user-facing flow
- **Assumed:** Existing explicit vendor refs may remain as backward-compatible internals, but the primary UX is the repo-scoped flag form
- **Still open:** None

---

## AI CLI Zsh Completion

**FR-002** — The `ai` CLI must provide interactive zsh completion that is fast for local skills and explicit for vendor skills.  
**Status:** Approved  
**Priority:** P1  

### Description
The shell completion experience must support rapid discovery of local skills while keeping vendor completion usable in large vendor repositories. The default add flow should favor the common case of local skills, while vendor completion should be opt-in through an explicit vendor flag and repo selection.

### Scope
- IN: Zsh completion for top-level commands, local skill completion, vendor skill completion, bundle completion, and remove completion
- OUT: Bash or fish completion, fuzzy search UI, ranking, or shell-specific UI beyond standard completion lists

### Acceptance Criteria
- [ ] `ai <TAB>` completes top-level commands such as `init`, `sync`, `add`, `remove`, `list`, and `completion`, with a short description for each command
- [ ] `ai add <TAB>` completes local skill names such as `capture` and `recap` from the central local skill set
- [ ] `ai add --vendor <TAB>` completes vendor repo names
- [ ] `ai add --vendor <repo> <TAB>` completes skill names within the selected vendor repo instead of scanning vendor skills during the default local completion path
- [ ] `ai add --bundle <TAB>` completes available bundle names
- [ ] If vendor completion data cannot be resolved, local completion still works and the shell does not block for an unacceptable amount of time

### Constraints
- Local completion must feel interactive and not pause long enough to disrupt normal shell use
- Default add completion should not require scanning the full vendor tree on every tab press
- Vendor completion should remain explicit enough to avoid ambiguity with local skill names
- Vendor skill completion should be scoped to the selected repo rather than the full vendor catalog when possible

### Open Questions
- [ ] None

### Assumptions
- Zsh is the first shell target and the primary shell for this workflow
- Local skill names are the most common completion target
- Vendor skill refs may be larger in number and need a separate completion path from local skills

### Refinement Notes
- **Added:** Top-level command descriptions in `ai <TAB>` completion
- **Clarified:** Vendor completion is now a two-step flow: repo selection first, then repo-scoped skill selection
- **Assumed:** Showing `--vendor` and `--bundle` as completion hints is acceptable in the local add flow
- **Still open:** None

---

## AGENTS Template Bootstrap

**FR-003** — `ai init` must bootstrap a project `AGENTS.md` from a repo template source.  
**Status:** Approved  
**Priority:** P1  

### Description
The repository should keep project bootstrap content separate from reusable skills. Initializing a project should create a project-root `AGENTS.md` from a maintained template source so new projects start with a consistent baseline for project-specific agent instructions.

### Scope
- IN: Repo template source for AGENTS bootstrap, project-root `AGENTS.md` creation, and `CLAUDE.md` compatibility link
- OUT: Multi-template selection, per-language templates, interactive bootstrap wizards, and generated project-specific agent subfolders beyond the existing runtime layout

### Acceptance Criteria
- [ ] The repo contains a canonical AGENTS template source for project bootstrap
- [ ] `ai init` copies that template into the target project as `AGENTS.md` when the project does not already have one
- [ ] `ai init` links `CLAUDE.md` to the project-root `AGENTS.md` for compatibility
- [ ] If `AGENTS.md` already exists in the target project, `ai init` does not overwrite it
- [ ] If the template source is unavailable, `ai init` still creates a minimal `AGENTS.md` or fails in a clear, documented way

### Constraints
- Keep templates separate from reusable skills and vendor catalogs
- Project bootstrap should remain deterministic and non-interactive

### Open Questions
- [ ] None

### Assumptions
- `templates/AGENTS.md` is the canonical source for the default project bootstrap content
- Projects may customize their copied `AGENTS.md` after initialization
