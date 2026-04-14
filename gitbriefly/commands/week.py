"""Week command."""

import typer
import json
from rich.console import Console
from rich.panel import Panel
from typing import Optional

from gitbrieflyly.core.git_reader import GitReader
from gitbrieflyly.ai import Summarizer
from gitbrieflyly.core.utils import load_config, get_config_value
from gitbrieflyly.exporters import get_exporter

console = Console()
config = load_config()


def _resolve_arg(value, key, default):
    if value is not None:
        return value
    return get_config_value(key, default)


def week_command(
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
    days: int = 7,
    max_commits: int = 100,
):
    """Show summary of Git activity from the last 7 days."""
    path = _resolve_arg(path, "path", ".")
    model = _resolve_arg(model, "model", "llama3")
    provider = _resolve_arg(provider, "provider", "ollama")

    console.print(
        Panel.fit("[bold cyan][ Scanning repositories... ][/bold cyan]", border_style="cyan")
    )

    reader = GitReader(str(path))
    commits = reader.get_commits(
        days=days, since=since, until=until, author=author, branch=branch, max_count=max_commits
    )

    if not commits:
        console.print("[yellow]No commits found in the specified time range.[/yellow]")
        console.print("[dim]Tip: Try --since 2026-03-01 or a wider date range[/dim]")
        raise typer.Exit(0)

    console.print(
        f"[green]Found {len(commits)} commits across {len(reader.repos)} repositories[/green]"
    )

    if no_ai:
        _display_commits(commits, json_output, export)
        raise typer.Exit(0)

    console.print(
        Panel.fit("[bold purple][ Generating AI summary... ][/bold purple]", border_style="purple")
    )

    summarizer = Summarizer(provider=provider, model=model, stream=stream)
    summary = summarizer.summarize(commits)

    if json_output:
        output = {
            "yesterday": summary.get("yesterday", []),
            "risks": summary.get("risks", []),
            "next_steps": summary.get("next_steps", []),
            "commits_count": len(commits),
            "repos": reader.repos,
        }
        console.print(json.dumps(output, indent=2))
        if export:
            _export_output(export, output)
    else:
        _display_summary(summary)
        if export:
            _export_output(export, summary)


def _display_commits(commits, json_output, export):
    if json_output:
        output = [
            {"repo": c["repo"], "message": c["message"], "author": c["author"], "date": c["date"]}
            for c in commits
        ]
        console.print(json.dumps(output, indent=2))
    else:
        for commit in commits:
            console.print(f"[bold]{commit['repo']}[/bold]")
            console.print(f"  {commit['message']}")
            console.print(f"  [dim]{commit['author']} - {commit['date']}[/dim]")
            console.print()


def _display_summary(summary: dict):
    if "yesterday" in summary and summary["yesterday"]:
        console.print(
            Panel.fit(
                "\n".join(f"- {item}" for item in summary["yesterday"]),
                title=" Yesterday ",
                border_style="green",
                padding=(0, 1),
            )
        )

    if "risks" in summary and summary["risks"]:
        console.print(
            Panel.fit(
                "\n".join(f"! {item}" for item in summary["risks"]),
                title=" Risks ",
                border_style="yellow",
                padding=(0, 1),
            )
        )

    if "next_steps" in summary and summary["next_steps"]:
        console.print(
            Panel.fit(
                "\n".join(f"> {item}" for item in summary["next_steps"]),
                title=" Next Steps ",
                border_style="blue",
                padding=(0, 1),
            )
        )


def _export_output(path: str, summary: dict):
    exporter = get_exporter("markdown")
    exporter.export(summary, path)
    console.print(f"[green]Exported to {path}[/green]")



