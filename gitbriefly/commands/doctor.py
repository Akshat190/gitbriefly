"""Doctor command - diagnostic tool."""

import os
from pathlib import Path

import requests
import typer
from rich.console import Console
from rich.table import Table

console = Console()


def check_ollama_running():
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return True, response.json().get("models", [])
        return False, []
    except Exception:
        return False, []


def check_model_available(models, model_name):
    """Check if a specific model is available."""
    model_names = [m.get("name", "") for m in models]
    return model_name in model_names


def check_git_repo(path):
    """Check if path is a valid git repository."""
    from git import Repo, InvalidGitRepositoryError

    try:
        repo_path = Path(path).resolve()
        Repo(str(repo_path))
        return True, str(repo_path)
    except InvalidGitRepositoryError:
        return False, str(repo_path)
    except Exception as e:
        return False, f"{path}: {e}"


def check_commits_in_range(path, days=7):
    """Check if there are commits in the specified range."""
    from datetime import datetime, timedelta
    from git import Repo

    try:
        repo = Repo(str(path))
        since = datetime.now() - timedelta(days=days)
        count = 0
        for commit in repo.iter_commits(max_count=100):
            if commit.committed_datetime.replace(tzinfo=None) >= since:
                count += 1
        return True, count
    except Exception as e:
        return False, str(e)


def check_config_file():
    """Check if config file is valid."""
    from gitbriefly.core.utils import load_config

    config_path = Path.home() / ".gitbriefly.toml"
    if not config_path.exists():
        return True, "No config file (optional)"

    try:
        config = load_config()
        return True, config
    except Exception as e:
        return False, str(e)


def check_api_keys():
    """Check if API keys are configured."""
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    results = []
    if openai_key:
        results.append(f"OPENAI_API_KEY: {'*' * 8}{openai_key[-4:]}")
    else:
        results.append("OPENAI_API_KEY: Not set")

    if anthropic_key:
        results.append(f"ANTHROPIC_API_KEY: {'*' * 8}{anthropic_key[-4:]}")
    else:
        results.append("ANTHROPIC_API_KEY: Not set")

    return True, results


def doctor_command(path: str = None):
    """Run diagnostics to check for common issues."""
    console.print("\n[bold cyan]Running diagnostics...[/bold cyan]\n")

    results = []

    console.print("[bold]1. Checking Ollama...[/bold]")
    ollama_running, models = check_ollama_running()
    if ollama_running:
        model_names = [m.get("name", "") for m in models]
        console.print("  [green]✓[/green] Ollama is running")
        console.print(
            f"  Available models: {', '.join(model_names) if model_names else 'None'}"
        )
        results.append(("Ollama", "Running", "green"))
    else:
        console.print("  [red]✗[/red] Ollama is not running")
        console.print("  [dim]Fix: Run 'ollama serve' in a terminal[/dim]")
        results.append(("Ollama", "Not running", "red"))

    console.print("\n[bold]2. Checking Git repository...[/bold]")
    path = path or "."
    is_repo, repo_path = check_git_repo(path)
    if is_repo:
        console.print(f"  [green]✓[/green] Git repo found at {repo_path}")
        results.append(("Git repo", "Found", "green"))
    else:
        console.print(f"  [red]✗[/red] Not a git repository: {repo_path}")
        results.append(("Git repo", "Not found", "red"))

    console.print("\n[bold]3. Checking recent commits...[/bold]")
    if is_repo:
        has_commits, count = check_commits_in_range(path, days=7)
        if has_commits and count > 0:
            console.print(f"  [green]✓[/green] {count} commits in last 7 days")
            results.append(("Commits (7d)", str(count), "green"))
        else:
            console.print("  [yellow]⚠[/yellow] No commits in last 7 days")
            console.print("  [dim]Tip: Try --since 2026-03-01[/dim]")
            results.append(("Commits (7d)", "0", "yellow"))

    console.print("\n[bold]4. Checking config file...[/bold]")
    config_ok, config_data = check_config_file()
    if config_ok:
        if isinstance(config_data, str):
            console.print(f"  [green]✓[/green] Config file: {config_data}")
            results.append(("Config", config_data, "green"))
        else:
            console.print("  [green]✓[/green] Config file valid")
            results.append(("Config", "Valid", "green"))
    else:
        console.print(f"  [red]✗[/red] Config error: {config_data}")
        results.append(("Config", "Error", "red"))

    console.print("\n[bold]5. Checking API keys...[/bold]")
    keys_ok, key_info = check_api_keys()
    for info in key_info:
        console.print(f"  {info}")
    results.append(("API keys", str(key_info), "green" if keys_ok else "yellow"))

    table = Table(title="Diagnostic Summary")
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Result")

    for check, status, _ in results:
        color = (
            "green"
            if status in ("Running", "Found", "Valid")
            else "yellow"
            if status == "0"
            else "red"
        )
        table.add_row(check, f"[{color}]{status}[/{color}]", status)

    console.print("\n")
    console.print(table)

    all_passed = all(r[2] == "green" for r in results)
    if all_passed:
        console.print("\n[bold green]All checks passed! ✓[/bold green]\n")
    else:
        console.print(
            "\n[bold yellow]Some issues found. See suggestions above.[/bold yellow]\n"
        )

    raise typer.Exit(0)
