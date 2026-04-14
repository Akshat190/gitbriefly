"""Stats command - show commit statistics."""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from gitbriefly.core.git_reader import GitReader
from gitbriefly.core.utils import load_config, get_config_value

console = Console()
config = load_config()


def _resolve_arg(value, key, default):
    if value is not None:
        return value
    return get_config_value(key, default)


def stats_command(
    path: Optional[str] = None,
    days: int = 7,
    author: Optional[str] = None,
):
    """Show commit statistics for the specified period."""
    path = _resolve_arg(path, "path", ".")

    reader = GitReader(str(path))
    commits = reader.get_commits(days=days, author=author)

    if not commits:
        console.print(f"[yellow]No commits found in the last {days} days.[/yellow]")
        raise typer.Exit(0)

    _display_stats(commits, days)


def _display_stats(commits, days):
    """Display commit statistics."""
    from collections import Counter

    total_commits = len(commits)

    authors = Counter(c["author"] for c in commits)
    top_authors = authors.most_common(5)

    repos = Counter(c["repo"] for c in commits)
    top_repos = repos.most_common(5)

    files_changed = Counter()
    total_insertions = 0
    total_deletions = 0
    for c in commits:
        for f in c.get("files", []):
            files_changed[f] += 1
        total_insertions += c.get("insertions", 0)
        total_deletions += c.get("deletions", 0)

    top_files = files_changed.most_common(10)

    table = Table(title=f"Commit Statistics (Last {days} days)", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Commits", str(total_commits))
    table.add_row("Unique Authors", str(len(authors)))
    table.add_row("Unique Repos", str(len(repos)))
    table.add_row("Total Insertions", f"+{total_insertions}")
    table.add_row("Total Deletions", f"-{total_deletions}")

    console.print(table)

    if top_authors:
        console.print("\n[bold]Top Contributors:[/bold]")
        for author, count in top_authors:
            console.print(f"  {author}: {count} commits")

    if top_repos:
        console.print("\n[bold]Repositories:[/bold]")
        for repo, count in top_repos:
            console.print(f"  {repo}: {count} commits")

    if top_files:
        console.print("\n[bold]Most Changed Files:[/bold]")
        for filename, count in top_files:
            console.print(f"  {filename}: {count} changes")
