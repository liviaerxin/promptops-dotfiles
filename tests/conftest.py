import pytest
import os
import shutil
import subprocess
from pathlib import Path

@pytest.fixture
def repo_root(tmp_path):
    """
    Creates a mock repository structure.
    """
    # Create structure
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    # Copy the actual ai script
    original_script = Path(__file__).parent.parent / "bin" / "ai"
    shutil.copy(original_script, bin_dir / "ai")
    
    # Make executable
    (bin_dir / "ai").chmod(0o755)
    
    # Create dummy skills
    (skills_dir / "personal-skill").mkdir()
    (skills_dir / "personal-skill" / "SKILL.md").write_text("# Personal Skill")

    # Skill name that would have broken the old python3 -c string interpolation
    (skills_dir / "bad'skill").mkdir()
    (skills_dir / "bad'skill" / "SKILL.md").write_text("# Personal Skill With Quote")
    
    (vendor_dir / "community-repo").mkdir()
    (vendor_dir / "community-repo" / "skills").mkdir()
    (vendor_dir / "community-repo" / "skills" / "community-skill").mkdir()
    (vendor_dir / "community-repo" / "skills" / "community-skill" / "SKILL.md").write_text("# Community Skill")

    # Vendor skill provided as a single markdown file (skill.md)
    (vendor_dir / "community-repo" / "skills" / "md-skill.md").write_text("# Vendor Markdown Skill")

    # Vendor repo that exposes a repo-level skills index for completion
    (vendor_dir / "indexed-repo").mkdir()
    (vendor_dir / "indexed-repo" / "skills").mkdir()
    (vendor_dir / "indexed-repo" / "skills" / "indexed-skill").mkdir()
    (vendor_dir / "indexed-repo" / "skills" / "indexed-skill" / "SKILL.md").write_text("# Indexed Skill")
    (vendor_dir / "indexed-repo" / "skills" / "indexed-md.md").write_text("# Indexed Markdown Skill")
    (vendor_dir / "indexed-repo" / "skills" / "ignored-scan-only").mkdir()
    (vendor_dir / "indexed-repo" / "skills" / "ignored-scan-only" / "SKILL.md").write_text("# Ignored Scan Only")
    (vendor_dir / "indexed-repo" / "skills_index.json").write_text(
        """
{
  "version": 1,
  "skills": [
    {"id": "indexed-skill", "path": "skills/indexed-skill"},
    {"name": "indexed-md", "path": "skills/indexed-md.md"}
  ]
}
""".strip()
    )

    # Bundle file used by the CLI
    (tmp_path / "skill-bundles.json").write_text(
        """
{
  "basic": {
    "description": "Test starter bundle",
    "skills": [
      "local:personal-skill",
      "vendor:community-repo/community-skill",
      "vendor:community-repo/md-skill"
    ]
  }
}
""".strip()
    )

    # AGENTS template used by init
    (templates_dir / "AGENTS.md").write_text(
        "# AGENTS.md\n\nTemplate bootstrap for project instructions.\n"
    )
    
    return tmp_path

@pytest.fixture
def ai_cmd(repo_root):
    """
    Returns the path to the mocked ai command.
    """
    return str(repo_root / "bin" / "ai")
