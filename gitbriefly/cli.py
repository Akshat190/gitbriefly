"""CLI entry point for gitbriefly."""

import typer
from typing import Optional

from gitbriefly.commands.today import today_command
from gitbriefly.commands.week import week_command
from gitbriefly.commands.standup import standup_command
from gitbriefly.commands.stats import stats_command
from gitbriefly.commands.history import history_command
from gitbriefly.commands.doctor import doctor_command

app = typer.Typer(
    name="gitbriefly",
    help="Your daily developer standup - powered by your Git history",
    add_completion=False,
)


@app.command()
def today(
    path: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    no_ai: bool = False,
    json_output: bool = False,
    stream: bool = False,
    export: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    days_ago: Optional[int] = typer.Option(
        7, "--days-ago", help="Number of days to look back"
    ),
    max_commits: int = 100,
    author: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Show summary of Git activity from the last 7 days."""
    today_command(
        path=path,
        model=model,
        provider=provider,
        no_ai=no_ai,
        json_output=json_output,
        stream=stream,
        export=export,
        since=since,
        until=until,
        days=days_ago,
        max_commits=max_commits,
        author=author,
        branch=branch,
    )


@app.command()
def week(
    path: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    no_ai: bool = False,
    json_output: bool = False,
    stream: bool = False,
    export: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    days_ago: int = 7,
    max_commits: int = 100,
    author: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Show summary of Git activity from the last 7 days."""
    week_command(
        path=path,
        model=model,
        provider=provider,
        no_ai=no_ai,
        json_output=json_output,
        stream=stream,
        export=export,
        since=since,
        until=until,
        days=days_ago,
        max_commits=max_commits,
        author=author,
        branch=branch,
    )


@app.command()
def standup(
    path: Optional[str] = None,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    no_ai: bool = False,
    json_output: bool = False,
    stream: bool = False,
    export: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    days_ago: int = 7,
    max_commits: int = 100,
    author: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Generate a ready-to-paste standup message (Yesterday / Today / Blockers)."""
    standup_command(
        path=path,
        model=model,
        provider=provider,
        no_ai=no_ai,
        json_output=json_output,
        stream=stream,
        export=export,
        since=since,
        until=until,
        days=days_ago,
        max_commits=max_commits,
        author=author,
        branch=branch,
    )


@app.command()
def stats(
    path: str = None,
    days: int = 7,
    author: str = None,
):
    """Show commit statistics for the specified period."""
    stats_command(path=path, days=days, author=author)


@app.command()
def history(
    days: int = 7,
    json_output: bool = False,
):
    """Show past summaries from memory."""
    history_command(days=days, json_output=json_output)


@app.command()
def doctor(
    path: Optional[str] = None,
):
    """Run diagnostics to check for common issues."""
    doctor_command(path=path)


@app.command()
def version():
    """Show gitbriefly version."""
    from gitbriefly import __version__

    print(f"gitbriefly version {__version__}")
    raise typer.Exit(0)


if __name__ == "__main__":
    app()
