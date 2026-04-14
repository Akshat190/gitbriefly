"""Utility functions for gitbriefly."""

import sys
from datetime import datetime, timedelta
from pathlib import Path


def load_config() -> dict:
    """Load config from ~/.gitbriefly.toml."""
    config_path = Path.home() / ".gitbriefly.toml"
    if config_path.exists():
        try:
            if sys.version_info >= (3, 11):
                import tomllib

                with open(config_path, "rb") as f:
                    return tomllib.load(f)
            else:
                import tomli

                with open(config_path, "rb") as f:
                    return tomli.load(f)
        except ImportError:
            return {}
        except Exception as e:
            print(f"[yellow]Warning: Config file error: {e}[/yellow]", file=sys.stderr)
            print("[dim]Check ~/.gitbriefly.toml for syntax errors[/dim]", file=sys.stderr)
            return {}
    return {}


def get_config_value(key: str, default=None):
    """Get a config value with fallback to default."""
    config = load_config()
    return config.get(key, default)


def get_time_range(days: int) -> tuple:
    """Get the time range for commit filtering."""
    end = datetime.now()
    start = end - timedelta(days=days)
    return start, end


def format_date(date: datetime) -> str:
    """Format a date for display."""
    return date.strftime("%Y-%m-%d %H:%M")


def truncate(text: str, max_length: int = 50) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def group_by_repo(commits: list) -> dict:
    """Group commits by repository."""
    result = {}
    for commit in commits:
        repo = commit.get("repo", "unknown")
        if repo not in result:
            result[repo] = []
        result[repo].append(commit)
    return result



