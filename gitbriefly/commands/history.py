"""History command - show past summaries."""

import typer
import json
from rich.console import Console
from rich.table import Table
from datetime import datetime

from gitbriefly.core.memory import get_history

console = Console()


def history_command(
    days: int = 7,
    json_output: bool = False,
):
    """Show past summaries from memory."""
    history = get_history(days=days)

    if not history:
        console.print(f"[yellow]No history found for the last {days} days.[/yellow]")
        raise typer.Exit(0)

    if json_output:
        for entry in history:
            console.print(json.dumps(entry, indent=2))
    else:
        _display_history(history, days)


def _display_history(history, days):
    """Display history table."""
    table = Table(title=f"Git Brief History (Last {days} days)", show_header=True)
    table.add_column("Date", style="cyan")
    table.add_column("Commits", style="green", justify="right")
    table.add_column("Summary", style="white")

    for entry in history:
        date = entry.get("date", "")
        summary = entry.get("summary", {})

        yesterday = summary.get("yesterday", [])
        commits = len(yesterday) if yesterday else 0

        date_str = (
            datetime.fromisoformat(date).strftime("%Y-%m-%d %H:%M")
            if date
            else "Unknown"
        )

        summary_text = ", ".join(yesterday[:2]) if yesterday else "No summary"
        if len(yesterday) > 2:
            summary_text += "..."

        table.add_row(date_str, str(commits), summary_text)

    console.print(table)
