# promptops-dotfiles

Personal dotfiles for AI prompts, skills, agent templates, and bootstrap workflows.

## 🚀 Overview

Just like personal dotfiles for your shell, **promptops-dotfiles** centralizes your opinionated AI prompts and vendor-provided community skills so you can selectively inject them into projects.

### Key Benefits
- **DRY (Don't Repeat Yourself):** Edit a prompt once in `~/.promptops-dotfiles` and it updates everywhere.
- **Zero Context Dilution:** Inject only the skills needed for the current task (Principle of Least Privilege).
- Tool Agnostic: Cross-compatible with Claude (`CLAUDE.md`), Codex/Antigravity (`.agents/`).
- **Manifest Tracking:** Uses `.agentic.json` to manage project-specific skill state robustly.
- **Explicit Provenance:** Namespaced refs such as `local:capture` and `vendor:repo/skill` keep source details in the manifest.

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
├── vendor/                # Community skills (Git Submodules)
│   └── (optional downloads)
├── skills_index.json      # Optional repo-level skill index for vendor completion
├── skill-bundles.json     # Curated local bundles of skill refs
├── tests/                 # Pytest suite
└── .venv/                 # Local test environment
```

---

## 🛠 Installation

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

## 📖 Usage Guide

### 1. Initialize a Project
Run this in any new project root to set up runtime folders plus a project-root `AGENTS.md` copied from `templates/AGENTS.md`.
```bash
ai init
```

### 2. Add Skills
Inject specific brains from your hub into the current project.
```bash
ai add capture
ai add --vendor antigravity-awesome-skills mcp-builder
ai add --bundle basic
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
ai add <TAB>                  # local skills
ai add --vendor <TAB>         # vendor repos
ai add --vendor repo <TAB>    # skills within that vendor repo
ai add --bundle <TAB>         # bundle names
```

### 6. Publishing This Repo for Others
If someone vendors this repo under their own `vendor/<repo>` directory, dynamic completion can come from a repo-level `skills_index.json`.

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
ai add <skills>
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
