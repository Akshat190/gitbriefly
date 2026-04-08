"""CLI entry point for gitbrief."""

import typer

from gitbrief.commands.today import today_command
from gitbrief.commands.week import week_command
from gitbrief.commands.standup import standup_command
from gitbrief.commands.stats import stats_command
from gitbrief.commands.history import history_command

app = typer.Typer(
    name="gitbrief",
    help="Your daily developer standup - powered by your Git history",
    add_completion=False,
)


@app.command()
def today(
    path=None,
    model=None,
    provider=None,
    no_ai=False,
    json_output=False,
    stream=False,
    export=None,
    since=None,
    until=None,
    author=None,
    branch=None,
):
    """Show summary of Git activity from the last 24 hours."""
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
        author=author,
        branch=branch,
    )


@app.command()
def week(
    path=None,
    model=None,
    provider=None,
    no_ai=False,
    json_output=False,
    stream=False,
    export=None,
    since=None,
    until=None,
    author=None,
    branch=None,
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
        author=author,
        branch=branch,
    )


@app.command()
def standup(
    path=None,
    model=None,
    provider=None,
    no_ai=False,
    json_output=False,
    stream=False,
    export=None,
    since=None,
    until=None,
    author=None,
    branch=None,
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
def version():
    """Show gitbrief version."""
    from gitbrief import __version__

    print(f"gitbrief version {__version__}")
    raise typer.Exit(0)


if __name__ == "__main__":
    app()
