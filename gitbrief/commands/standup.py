"""Standup command."""

import typer
import json
from rich.console import Console
from typing import Optional

from gitbrief.core.git_reader import GitReader
from gitbrief.ai import Summarizer
from gitbrief.core.utils import load_config, get_config_value
from gitbrief.exporters import get_exporter

console = Console()
config = load_config()


def _resolve_arg(value, key, default):
    if value is not None:
        return value
    return get_config_value(key, default)


def standup_command(
    path: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    no_ai: bool = False,
    json_output: bool = False,
    stream: bool = False,
    export: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    author: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Generate a ready-to-paste standup message (Yesterday / Today / Blockers)."""
    path = _resolve_arg(path, "path", ".")
    model = _resolve_arg(model, "model", "llama3")
    provider = _resolve_arg(provider, "provider", "ollama")

    reader = GitReader(str(path))
    commits = reader.get_commits(days=1, since=since, until=until, author=author, branch=branch)

    if not commits:
        if json_output:
            output = {
                "yesterday": ["No commits found"],
                "today": ["To be determined"],
                "blockers": ["None"],
            }
            console.print(json.dumps(output, indent=2))
        else:
            standup_text = """**Yesterday:**
- No commits found

**Today:**
- To be determined

**Blockers:**
- None"""
            console.print(standup_text)
        raise typer.Exit(0)

    if no_ai:
        if json_output:
            output = {
                "yesterday": [c["message"] for c in commits[:5]],
                "today": ["To be determined"],
                "blockers": ["None"],
            }
            console.print(json.dumps(output, indent=2))
        else:
            standup_text = f"""**Yesterday:**
{chr(10).join(f"- {c['message']}" for c in commits[:5])}

**Today:**
- To be determined

**Blockers:**
- None"""
            console.print(standup_text)
        raise typer.Exit(0)

    summarizer = Summarizer(provider=provider, model=model, stream=stream)
    summary = summarizer.summarize_for_standup(commits)

    standup_text = f"""**Yesterday:**
{chr(10).join(f"- {item}" for item in summary.get("yesterday", []))}

**Today:**
{chr(10).join(f"- {item}" for item in summary.get("today", ["Continue working on pending tasks"]))}

**Blockers:**
{chr(10).join(f"- {item}" for item in summary.get("blockers", ["None"]))}"""

    if json_output:
        output = {
            "yesterday": summary.get("yesterday", []),
            "today": summary.get("today", []),
            "blockers": summary.get("blockers", []),
            "commits_count": len(commits),
        }
        console.print(json.dumps(output, indent=2))
        if export:
            _export_output(export, output)
    else:
        console.print(standup_text)
        if export:
            _export_output(export, summary)


def _export_output(path: str, summary: dict):
    exporter = get_exporter("markdown")
    exporter.export(summary, path)
    console.print(f"[green]Exported to {path}[/green]")
