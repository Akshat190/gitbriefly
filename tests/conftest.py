"""Test fixtures for gitbrief tests."""

import gc
import os
import pytest
import tempfile
import time
from pathlib import Path
from git import Repo


@pytest.fixture
def fake_repo():
    """Create a temporary git repo with fake commits."""
    tmpdir = tempfile.mkdtemp()
    try:
        repo = Repo.init(tmpdir)
        repo.config_writer().set_value("user", "name", "Test User").release()
        repo.config_writer().set_value("user", "email", "test@test.com").release()

        for i, msg in enumerate(
            ["feat: add auth", "fix: login bug", "refactor: clean utils"]
        ):
            f = Path(tmpdir) / f"file{i}.py"
            f.write_text(f"# file {i}")
            repo.index.add([f"file{i}.py"])
            repo.index.commit(msg)

        yield tmpdir
    finally:
        gc.collect()
        time.sleep(0.1)
        try:
            for root, dirs, files in os.walk(tmpdir, topdown=False):
                for name in files:
                    try:
                        os.chmod(os.path.join(root, name), 0o777)
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        os.chmod(os.path.join(root, name), 0o777)
                    except Exception:
                        pass
            os.remove(tmpdir) if os.path.isfile(tmpdir) else None
            if os.path.isdir(tmpdir):
                os.rmdir(tmpdir)
        except Exception:
            pass
