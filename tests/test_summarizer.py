"""Tests for summarizer module."""

import pytest

from gitbrief.ai.summarizer import Summarizer


def test_summarize_empty_commits():
    """Test summarize returns empty dict for empty commits."""
    s = Summarizer()
    result = s.summarize([])
    assert result == {"yesterday": [], "risks": [], "next_steps": []}


def test_summarize_for_standup_empty():
    """Test summarize_for_standup returns empty dict for empty commits."""
    s = Summarizer()
    result = s.summarize_for_standup([])
    assert result == {"yesterday": [], "today": [], "blockers": []}


def test_summarizer_initialization():
    """Test Summarizer can be initialized."""
    s = Summarizer()
    assert s.provider is not None


def test_summarizer_with_mock_commits():
    """Test summarize with mock commit data."""
    s = Summarizer()
    commits = [
        {
            "repo": "test",
            "message": "feat: add feature",
            "files": [],
            "insertions": 10,
            "deletions": 0,
        }
    ]
    result = s.summarize(commits)
    assert "yesterday" in result
    assert "risks" in result
    assert "next_steps" in result


def test_summarizer_fallback_on_no_ai():
    """Test that fallback works when no AI available."""
    s = Summarizer(provider="nonexistent")
    commits = [
        {"repo": "test", "message": "test commit", "files": [], "insertions": 5, "deletions": 2}
    ]
    result = s.summarize(commits)
    assert isinstance(result, dict)
    assert "yesterday" in result
