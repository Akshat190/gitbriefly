"""Git data extraction module."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from git import Repo, InvalidGitRepositoryError
from pathlib import Path


class GitReader:
    """Reads Git commit data from repositories."""

    def __init__(self, path: str = "."):
        self.path = Path(path).resolve()
        self.repos: List[str] = []
        self.commits: List[Dict] = []

    def get_commits(
        self,
        days: int = 7,
        since: Optional[str] = None,
        until: Optional[str] = None,
        author: Optional[str] = None,
        branch: Optional[str] = None,
        max_count: int = 100,
    ) -> List[Dict]:
        """Get commits from the last N days or within a date range."""
        self.commits = []

        if since:
            try:
                self.since = datetime.fromisoformat(since)
            except ValueError:
                self.since = datetime.now() - timedelta(
                    days=int(since) if since.isdigit() else days
                )
        else:
            self.since = datetime.now() - timedelta(days=days)

        if until:
            try:
                self.until = datetime.fromisoformat(until)
            except ValueError:
                self.until = datetime.now()
        else:
            self.until = datetime.now()

        self.author_filter = author
        self.branch_filter = branch
        self.max_count = max_count

        if self._is_git_repo(self.path):
            self.repos.append(str(self.path))
            self._scan_repo(self.path)
        else:
            self._scan_directory(self.path)

        return self.commits

    def _is_git_repo(self, path: Path) -> bool:
        """Check if a path is a Git repository."""
        try:
            Repo(str(path))
            return True
        except InvalidGitRepositoryError:
            return False

    def _scan_directory(self, directory: Path):
        """Scan a directory for Git repositories."""
        if not directory.exists() or not directory.is_dir():
            return

        for entry in directory.iterdir():
            if entry.name.startswith("."):
                continue

            if entry.is_dir() and self._is_git_repo(entry):
                self.repos.append(str(entry))
                self._scan_repo(entry)
            elif entry.is_dir():
                self._scan_directory(entry)

    def _scan_repo(self, repo_path: Path):
        """Scan a single repository for commits."""
        try:
            repo = Repo(str(repo_path))

            branch = self.branch_filter if self.branch_filter else "HEAD"

            for commit in repo.iter_commits(branch, all=True, max_count=self.max_count):
                commit_time = commit.committed_datetime.replace(tzinfo=None)

                if not (self.since <= commit_time <= self.until):
                    continue

                if (
                    self.author_filter
                    and self.author_filter.lower() not in commit.author.name.lower()
                ):
                    continue

                self.commits.append(
                    {
                        "repo": repo_path.name,
                        "message": commit.message.strip(),
                        "author": commit.author.name,
                        "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M"),
                        "files": list(commit.stats.files.keys()),
                        "insertions": commit.stats.total.get("insertions", 0),
                        "deletions": commit.stats.total.get("deletions", 0),
                    }
                )
        except Exception as e:
            print(f"Error scanning {repo_path}: {e}")

    def get_repos(self) -> List[str]:
        """Get list of scanned repositories."""
        return self.repos
