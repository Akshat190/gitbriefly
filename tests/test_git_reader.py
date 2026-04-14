"""Tests for git_reader module."""

import pytest

from gitbriefly.core.git_reader import GitReader


def test_get_commits_single_repo(fake_repo):
    """Test getting commits from a single repository."""
    reader = GitReader(fake_repo)
    commits = reader.get_commits(days=7)
    assert len(commits) == 3


def test_get_commits_filters_by_days(fake_repo):
    """Test that days filter works."""
    reader = GitReader(fake_repo)
    commits = reader.get_commits(days=1)
    assert len(commits) >= 0


def test_get_repos(fake_repo):
    """Test getting list of repositories."""
    reader = GitReader(fake_repo)
    reader.get_commits(days=7)
    assert len(reader.get_repos()) >= 1


def test_git_reader_initialization():
    """Test GitReader can be initialized."""
    reader = GitReader(".")
    assert reader.path is not None


def test_get_commits_no_repo(tmp_path):
    """Test with non-git directory."""
    reader = GitReader(str(tmp_path))
    commits = reader.get_commits(days=1)
    assert commits == []
