"""CLI entry point for gitbrief - backward compatible shim."""

import typer

from gitbrief.cli import app

if __name__ == "__main__":
    app()
