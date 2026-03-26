import pytest
import subprocess
import json
import os
from pathlib import Path

def run_cmd(cmd_list, cwd):
    """Run command and return output."""
    result = subprocess.run(
        cmd_list,
        cwd=str(cwd),
        capture_output=True,
        text=True
    )
    return result

def make_git_vendor_repo(base_dir, name):
    """Create a local git repo that mimics a vendor skill catalog."""
    repo_dir = base_dir / name
    repo_dir.mkdir()
    (repo_dir / "skills").mkdir()
    (repo_dir / "skills" / "remote-skill").mkdir()
    (repo_dir / "skills" / "remote-skill" / "SKILL.md").write_text("# Remote Skill")
    (repo_dir / "skills_index.json").write_text(
        json.dumps(
            {
                "version": 1,
                "skills": [
                    {"id": "remote-skill", "path": "skills/remote-skill"},
                ],
            }
        )
    )
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-c", "user.name=Test User", "-c", "user.email=test@example.com", "commit", "-m", "Initial"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    return repo_dir

def test_init(ai_cmd, tmp_path):
    """Verify init creates necessary directories and manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    result = run_cmd([ai_cmd, "init"], project_dir)
    assert result.returncode == 0
    
    # Check directories
    assert (project_dir / ".agents" / "skills").is_dir()
    assert (project_dir / ".agents" / "agents").is_dir()
    assert (project_dir / ".claude").is_dir()
    
    # Check bootstrap files
    assert (project_dir / "AGENTS.md").exists()
    assert (project_dir / "AGENTS.md").read_text() == "# AGENTS.md\n\nTemplate bootstrap for project instructions.\n"
    assert (project_dir / "CLAUDE.md").is_symlink()
    assert (project_dir / "CLAUDE.md").resolve() == (project_dir / "AGENTS.md")
    
    # Check manifest
    manifest = project_dir / ".agentic.json"
    assert manifest.exists()
    assert json.loads(manifest.read_text()) == {"version": 2, "skills": [], "bundles": []}

def test_add_personal_skill(ai_cmd, repo_root, tmp_path):
    """Verify adding a personal skill updates manifest and symlinks."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    
    # Add personal skill (defined in conftest.py)
    result = run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    assert result.returncode == 0
    assert "Added personal skill" in result.stdout
    
    # Check symlink
    skill_link = project_dir / ".agents" / "skills" / "personal-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "skills" / "personal-skill")
    
    # Check manifest
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert manifest["skills"] == [
        {
            "name": "personal-skill",
            "ref": "local:personal-skill",
            "source": "local",
        }
    ]
    assert manifest["bundles"] == []

def test_add_vendor_skill(ai_cmd, repo_root, tmp_path):
    """Verify adding a vendor skill updates manifest and symlinks."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    
    result = run_cmd([ai_cmd, "add", "--vendor", "community-repo", "community-skill"], project_dir)
    assert result.returncode == 0
    assert "Added community skill" in result.stdout
    
    # Check symlink
    skill_link = project_dir / ".agents" / "skills" / "community-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "vendor" / "community-repo" / "skills" / "community-skill")
    
    # Check manifest
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert manifest["skills"] == [
        {
            "name": "community-skill",
            "ref": "vendor:community-repo/community-skill",
            "source": "vendor",
        }
    ]

def test_vendor_install_uses_repo_name_by_default(ai_cmd, repo_root, tmp_path):
    """Verify `ai vendor install` derives the local vendor name from the repo basename."""
    source_repo = make_git_vendor_repo(tmp_path, "catalog-source.git")
    source_url = source_repo.as_uri()

    result = run_cmd([ai_cmd, "vendor", "install", source_url], repo_root)
    assert result.returncode == 0
    assert f"Installing {source_url} into {repo_root / 'vendor' / 'catalog-source'}" in result.stdout
    assert f"Installed {source_url} into {repo_root / 'vendor' / 'catalog-source'}" in result.stdout
    assert "Vendor repo: catalog-source" in result.stdout
    assert "Cloning into" in result.stderr

    installed_repo = repo_root / "vendor" / "catalog-source"
    assert installed_repo.is_dir()
    assert (installed_repo / "skills" / "remote-skill" / "SKILL.md").exists()

    project_dir = tmp_path / "project-default-vendor"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    add_result = run_cmd([ai_cmd, "add", "--vendor", "catalog-source", "remote-skill"], project_dir)
    assert add_result.returncode == 0
    assert (project_dir / ".agents" / "skills" / "remote-skill").resolve() == (installed_repo / "skills" / "remote-skill")

def test_vendor_install_supports_name_override(ai_cmd, repo_root, tmp_path):
    """Verify `ai vendor install --name` installs under the requested local vendor name."""
    source_repo = make_git_vendor_repo(tmp_path, "override-source.git")
    source_url = source_repo.as_uri()

    result = run_cmd(
        [ai_cmd, "vendor", "install", source_url, "--name", "custom-vendor"],
        repo_root,
    )
    assert result.returncode == 0
    assert f"Installed {source_url} into {repo_root / 'vendor' / 'custom-vendor'}" in result.stdout
    assert "Vendor repo: custom-vendor" in result.stdout

    installed_repo = repo_root / "vendor" / "custom-vendor"
    assert installed_repo.is_dir()
    assert (installed_repo / "skills_index.json").exists()

def test_vendor_install_fails_if_target_exists(ai_cmd, repo_root, tmp_path):
    """Verify `ai vendor install` refuses to overwrite an existing vendor directory."""
    source_repo = make_git_vendor_repo(tmp_path, "duplicate-source.git")
    source_url = source_repo.as_uri()

    first_result = run_cmd([ai_cmd, "vendor", "install", source_url], repo_root)
    assert first_result.returncode == 0

    second_result = run_cmd([ai_cmd, "vendor", "install", source_url], repo_root)
    assert second_result.returncode != 0
    assert "already exists" in second_result.stdout

def test_add_personal_skill_with_quote(ai_cmd, repo_root, tmp_path):
    """Verify skill names with quotes don't break manifest updates."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    skill_name = "bad'skill"
    result = run_cmd([ai_cmd, "add", skill_name], project_dir)
    assert result.returncode == 0

    skill_link = project_dir / ".agents" / "skills" / skill_name
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "skills" / skill_name)

    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert manifest["skills"] == [
        {
            "name": skill_name,
            "ref": f"local:{skill_name}",
            "source": "local",
        }
    ]

def test_add_vendor_md_skill_links_to_requested_name(ai_cmd, repo_root, tmp_path):
    """Verify vendor foo.md installs as .agents/skills/foo (not foo.md)."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    result = run_cmd([ai_cmd, "add", "--vendor", "community-repo", "md-skill"], project_dir)
    assert result.returncode == 0
    assert "Added community skill" in result.stdout

    skill_link = project_dir / ".agents" / "skills" / "md-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "vendor" / "community-repo" / "skills" / "md-skill.md")

def test_add_missing_skill_exits_nonzero(ai_cmd, tmp_path):
    """Verify ai add returns non-zero when a requested skill is missing."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    result = run_cmd([ai_cmd, "add", "does-not-exist"], project_dir)
    assert result.returncode != 0
    assert "not found" in result.stdout

def test_add_missing_vendor_skill_exits_nonzero(ai_cmd, tmp_path):
    """Verify ai add --vendor returns non-zero when the skill is missing."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    result = run_cmd([ai_cmd, "add", "--vendor", "community-repo", "does-not-exist"], project_dir)
    assert result.returncode != 0
    assert "not found" in result.stdout

def test_remove_skill(ai_cmd, repo_root, tmp_path):
    """Verify removing a skill cleans up symlinks and manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    
    result = run_cmd([ai_cmd, "remove", "local:personal-skill"], project_dir)
    assert result.returncode == 0
    assert "Removed skill" in result.stdout
    
    # Check symlink gone
    skill_link = project_dir / ".agents" / "skills" / "personal-skill"
    assert not skill_link.exists()
    
    # Check manifest update
    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert manifest["skills"] == []

def test_sync_from_manifest(ai_cmd, repo_root, tmp_path):
    """Verify sync recreates symlinks from manifest."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    # Simulate a cloned repo with just a manifest
    (project_dir / ".agentic.json").write_text(json.dumps({
        "version": 2,
        "skills": [
            {"name": "personal-skill", "ref": "local:personal-skill", "source": "local"},
            {"name": "community-skill", "ref": "vendor:community-repo/community-skill", "source": "vendor"},
            {"name": "md-skill", "ref": "vendor:community-repo/md-skill", "source": "vendor"},
        ],
        "bundles": []
    }))
    
    result = run_cmd([ai_cmd, "sync"], project_dir)
    assert result.returncode == 0
    
    # Check symlinks created
    assert (project_dir / ".agents" / "skills" / "personal-skill").is_symlink()
    assert (project_dir / ".agents" / "skills" / "community-skill").is_symlink()
    assert (project_dir / ".agents" / "skills" / "md-skill").is_symlink()

def test_install_alias_syncs_manifest(ai_cmd, repo_root, tmp_path):
    """Verify install remains an alias for sync."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / ".agentic.json").write_text(json.dumps({
        "version": 2,
        "skills": [
            {"name": "community-skill", "ref": "vendor:community-repo/community-skill", "source": "vendor"}
        ],
        "bundles": []
    }))

    result = run_cmd([ai_cmd, "install"], project_dir)
    assert result.returncode == 0
    assert "Installing skills" in result.stdout

    skill_link = project_dir / ".agents" / "skills" / "community-skill"
    assert skill_link.is_symlink()
    assert skill_link.resolve() == (repo_root / "vendor" / "community-repo" / "skills" / "community-skill")

def test_add_bundle_records_bundle_and_resolved_skills(ai_cmd, repo_root, tmp_path):
    """Verify ai add --bundle installs all refs and records provenance."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)

    result = run_cmd([ai_cmd, "add", "--bundle", "basic"], project_dir)
    assert result.returncode == 0
    assert "Added bundle" in result.stdout

    assert (project_dir / ".agents" / "skills" / "personal-skill").is_symlink()
    assert (project_dir / ".agents" / "skills" / "community-skill").is_symlink()
    assert (project_dir / ".agents" / "skills" / "md-skill").is_symlink()

    manifest = json.loads((project_dir / ".agentic.json").read_text())
    assert manifest["bundles"] == [
        {
            "name": "basic",
            "ref": "local:basic",
            "source": "local",
        }
    ]
    assert manifest["skills"] == [
        {
            "name": "personal-skill",
            "ref": "local:personal-skill",
            "source": "local",
            "via": "local:basic",
        },
        {
            "name": "community-skill",
            "ref": "vendor:community-repo/community-skill",
            "source": "vendor",
            "via": "local:basic",
        },
        {
            "name": "md-skill",
            "ref": "vendor:community-repo/md-skill",
            "source": "vendor",
            "via": "local:basic",
        },
    ]

def test_list(ai_cmd, repo_root, tmp_path):
    """Verify list command output."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    run_cmd([ai_cmd, "add", "personal-skill"], project_dir)
    
    result = run_cmd([ai_cmd, "list"], project_dir)
    assert result.returncode == 0
    assert "Available Skills" in result.stdout
    assert "local:personal-skill" in result.stdout
    assert "vendor:community-repo/community-skill" in result.stdout
    assert "local:basic" in result.stdout
    assert "Active in Project" in result.stdout

def test_completion_zsh_outputs_completion_script(ai_cmd, tmp_path):
    """Verify ai completion zsh prints a usable zsh completion function."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "completion", "zsh"], project_dir)
    assert result.returncode == 0
    assert "#compdef ai" in result.stdout
    assert "__ai_complete()" in result.stdout
    assert "_ai()" in result.stdout
    assert "command ai __complete" in result.stdout
    assert "compdef _ai ai" in result.stdout
    assert "'init:initialize a project workspace'" in result.stdout
    assert "'add:add local skills, vendor skills, or bundles'" in result.stdout
    assert "'vendor:install local vendor catalogs'" in result.stdout

def test_completion_internal_lists_refs(ai_cmd, tmp_path):
    """Verify internal completion candidates match add/bundle/remove UX."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    run_cmd([ai_cmd, "init"], project_dir)
    run_cmd([ai_cmd, "add", "personal-skill"], project_dir)

    skills_result = run_cmd([ai_cmd, "__complete", "skills"], project_dir)
    assert skills_result.returncode == 0
    assert "local:personal-skill" in skills_result.stdout
    assert "vendor:community-repo/community-skill" in skills_result.stdout

    local_add_result = run_cmd([ai_cmd, "__complete", "local-candidates"], project_dir)
    assert local_add_result.returncode == 0
    assert "personal-skill" in local_add_result.stdout
    assert "vendor:community-repo/community-skill" not in local_add_result.stdout

    vendor_repo_result = run_cmd([ai_cmd, "__complete", "vendor-repos"], project_dir)
    assert vendor_repo_result.returncode == 0
    assert vendor_repo_result.stdout.splitlines() == ["community-repo", "indexed-repo"]

    vendor_skill_result = run_cmd([ai_cmd, "__complete", "vendor-repo-skills", "community-repo"], project_dir)
    assert vendor_skill_result.returncode == 0
    assert "community-skill" in vendor_skill_result.stdout
    assert "md-skill" in vendor_skill_result.stdout

    bundles_result = run_cmd([ai_cmd, "__complete", "bundles"], project_dir)
    assert bundles_result.returncode == 0
    assert "local:basic" in bundles_result.stdout

    bundle_candidate_result = run_cmd([ai_cmd, "__complete", "bundle-candidates"], project_dir)
    assert bundle_candidate_result.returncode == 0
    assert bundle_candidate_result.stdout.strip() == "basic"

    active_result = run_cmd([ai_cmd, "__complete", "active"], project_dir)
    assert active_result.returncode == 0
    assert active_result.stdout.strip() == "local:personal-skill"

def test_add_completion_local_candidates_are_local_skill_names(ai_cmd, tmp_path):
    """Verify `ai add <TAB>` candidates are local bare skill names."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "__complete", "local-candidates"], project_dir)
    assert result.returncode == 0
    assert "personal-skill" in result.stdout
    assert "bad'skill" in result.stdout
    assert "vendor:community-repo/community-skill" not in result.stdout

def test_add_completion_vendor_repo_candidates_are_repo_names(ai_cmd, tmp_path):
    """Verify `ai add --vendor <TAB>` candidates are vendor repo names."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "__complete", "vendor-repos"], project_dir)
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["community-repo", "indexed-repo"]

def test_add_completion_vendor_skill_candidates_are_repo_scoped(ai_cmd, tmp_path):
    """Verify `ai add --vendor <repo> <TAB>` candidates are vendor skill names."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "__complete", "vendor-repo-skills", "community-repo"], project_dir)
    assert result.returncode == 0
    assert "community-skill" in result.stdout
    assert "md-skill" in result.stdout
    assert "personal-skill" not in result.stdout

def test_add_completion_vendor_skill_candidates_use_repo_index_when_present(ai_cmd, tmp_path):
    """Verify `skills_index.json` is preferred over scanning vendor skills directly."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "__complete", "vendor-repo-skills", "indexed-repo"], project_dir)
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["indexed-skill", "indexed-md"]
    assert "ignored-scan-only" not in result.stdout

def test_completion_zsh_add_branch_uses_dynamic_skill_describe(ai_cmd, tmp_path):
    """Verify the generated zsh script uses a direct dynamic branch for `ai add`."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    result = run_cmd([ai_cmd, "completion", "zsh"], project_dir)
    assert result.returncode == 0
    assert "skills=(\"${(@f)$(__ai_complete local-candidates)}\")" in result.stdout
    assert "repos=(\"${(@f)$(__ai_complete vendor-repos)}\")" in result.stdout
    assert "skills=(\"${(@f)$(__ai_complete vendor-repo-skills \"$vendor_repo\")}\")" in result.stdout
    assert "bundles=(\"${(@f)$(__ai_complete bundle-candidates)}\")" in result.stdout
    assert 'if [[ $prev == --vendor ]]; then' in result.stdout
    assert "vendor_repo=${words[i+1]:-}" in result.stdout
    assert "_describe 'skill' skills" in result.stdout
    assert "_describe 'vendor repo' repos" in result.stdout
    assert "_describe 'vendor skill' skills" in result.stdout
    assert "_describe 'bundle' bundles" in result.stdout
    assert "add_options=(--bundle --vendor)" in result.stdout
    assert "case $cmd in" in result.stdout
    assert "_arguments -C" not in result.stdout
