"""Test fixtures for gitbrief tests."""

import pytest
import tempfile
from pathlib import Path
from git import Repo


@pytest.fixture
def fake_repo():
    """Create a temporary git repo with fake commits."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        repo.config_writer().set_value("user", "name", "Test User").release()
        repo.config_writer().set_value("user", "email", "test@test.com").release()

        # Create 3 fake commits
        for i, msg in enumerate(["feat: add auth", "fix: login bug", "refactor: clean utils"]):
            f = Path(tmpdir) / f"file{i}.py"
            f.write_text(f"# file {i}")
            repo.index.add([f"file{i}.py"])
            repo.index.commit(msg)

        yield tmpdir
