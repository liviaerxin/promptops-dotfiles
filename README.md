# promptops-dotfiles

Personal dotfiles for AI prompts, skills, agent templates, and bootstrap workflows.

## 🚀 Overview

If you keep re-copying prompts, agent instructions, and reusable skills across projects, this repo gives you one place to manage them.

**promptops-dotfiles** is a small personal promptops hub:

- keep reusable local skills in one repo
- install third-party skill catalogs once and use them locally
- bootstrap new projects with a consistent `AGENTS.md`
- inject only the skills a project actually needs

### Key Benefits
- **DRY (Don't Repeat Yourself):** Edit a prompt once in `~/.promptops-dotfiles` and it updates everywhere.
- **Zero Context Dilution:** Inject only the skills needed for the current task (Principle of Least Privilege).
- Tool Agnostic: Cross-compatible with Claude (`CLAUDE.md`), Codex/Antigravity (`.agents/`).
- **Manifest Tracking:** Uses `.agentic.json` to manage project-specific skill state robustly.
- **Explicit Provenance:** Namespaced refs such as `local:capture` and `vendor:repo/skill` keep source details in the manifest.

### What You Can Do

```bash
ai vendor list
ai vendor install https://github.com/sickn33/antigravity-awesome-skills.git

mkdir my-project && cd my-project
ai init
ai add capture
ai add --vendor antigravity-awesome-skills mcp-builder
```

---

## 🏗 Architecture

```text
~/.promptops-dotfiles/
├── bin/
│   └── ai                 # The CLI tool (Bash + Python)
├── skills/                # Your personal/private skills
│   ├── capture/
│   ├── handoff/
│   └── ...
├── templates/             # Bootstrap templates for new projects
│   └── AGENTS.md
├── vendor/                # Optional local vendor catalogs (git clones)
│   └── (installed on demand)
├── vendor-sources.json    # Shipped references for known vendor catalogs
├── skill-bundles.json     # Curated local bundles of skill refs
├── tests/                 # Pytest suite
└── .venv/                 # Local test environment
```

---

## 🛠 Installation

### Environment

- Tested working environment: macOS
- Expected to work on: Linux
- Runtime requirements: `bash`, `python3`, `git`
- Test-only requirement: `pytest`
- Optional shell integration: `zsh`

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url> ~/.promptops-dotfiles
   cd ~/.promptops-dotfiles
   ```

2. **Run installer script:**
   ```bash
   bash bin/install-ai
   ```

3. **Verify:**
   ```bash
   ai list
   ```

Optional: skip shell rc updates and install to a custom directory:
```bash
bash bin/install-ai --dir "$HOME/bin" --no-path
```

---

## ⚡ Quick Start

```bash
ai vendor list
ai vendor install https://github.com/sickn33/antigravity-awesome-skills.git

mkdir my-project && cd my-project
ai init
ai add <local-skill>
ai add --vendor <vendor-repo> <vendor-skill>
```

The shipped vendor references live in `vendor-sources.json`.

---

## 📖 Usage Guide

### 1. Initialize a Project
Run this in any new project root to set up runtime folders plus a project-root `AGENTS.md` copied from `templates/AGENTS.md`.
```bash
ai init
```

### 2. Add Skills
See the shipped vendor references:
```bash
ai vendor list
```

Install a vendor catalog once, then use it locally:
```bash
ai vendor install https://github.com/sickn33/antigravity-awesome-skills.git
```

Inject specific brains from your hub into the current project.
```bash
ai add <local-skill>
ai add --vendor <vendor-repo> <vendor-skill>
ai add --bundle basic
```

Concrete examples:
```bash
ai add capture
ai add --vendor antigravity-awesome-skills mcp-builder
```

### 3. Sync Fresh Clones
If you clone a project that already has an `.agentic.json` manifest, restore all skill symlinks instantly:
```bash
ai sync
```

`ai install` remains as a compatibility alias for `ai sync`.

### 4. Remove Skills
Clean up the AI's context when a task is finished.
```bash
ai remove local:capture
```

### 5. Shell Completion
For `zsh`, the installer adds completion automatically. The intended interaction is:
```bash
ai <TAB>
ai add <TAB>                  # local skill names
ai add --vendor <TAB>         # vendor repo names
ai add --vendor <repo> <TAB>  # skill names within that vendor repo
ai add --bundle <TAB>         # bundle names
```

### 6. Publishing a Vendor Repo for Others
Local `ai add <TAB>` currently scans `skills/` directly. If you choose to publish a vendor repo for others later, dynamic vendor completion can come from a repo-level `skills_index.json`.

Preferred layout:
```text
vendor/your-repo/
├── skills/
│   ├── capture/
│   └── recap/
└── skills_index.json
```

Recommended index shape:
```json
{
  "version": 1,
  "skills": [
    {"id": "capture", "path": "skills/capture"},
    {"id": "recap", "path": "skills/recap"}
  ]
}
```

Notes:
- `ai vendor list` prints the shipped vendor references from `vendor-sources.json`.
- `vendor-sources.json` is a curated reference list, not a lockfile or registry.
- `ai vendor install <git-url>` clones into `vendor/<repo-name>` by default.
- Use `--name <vendor>` if you want a shorter local alias.
- `ai vendor install` is the only networked step; `ai add`, `ai sync`, and completion stay local.
- `ai add <TAB>` uses scan mode over local `skills/` today.
- `ai add --vendor <repo> <TAB>` reads `skills_index.json` first.
- If no index is present, the CLI falls back to scanning `skills/`.
- `skills-index.json` is still accepted for compatibility.

---

## 🧭 Recommended Pattern (2026)

Use a two-layer model:

- **`promptops-dotfiles` = personal layer**
  - Keep reusable generic skills and private preferences here.
  - This is your local AI toolbox.

- **`project B` = team layer**
  - Commit only project-critical instructions (for example `AGENTS.md`).
  - Do not commit generated local runtime artifacts: `.agents/`, `CLAUDE.md`, `.claude/`.
  - Keep `.agentic.json` local by default; optionally commit `.agentic.json.example` for opt-in onboarding.

### Practical Workflow in Project B

```bash
ai init
ai add <local-skill>
ai add --vendor <vendor-repo> <vendor-skill>
ai add --bundle basic
# later, on fresh clones (if .agentic.json is present):
ai sync
```

Copy skills into `project B` only when they are truly project-specific and must be identical for all contributors. Keep generic skills in `promptops-dotfiles`.

---

## 🧪 Testing

The repository includes a comprehensive `pytest` suite to ensure the CLI remains robust across platforms.

```bash
source .venv/bin/activate
pytest tests
```

---

## 📄 License
MIT
