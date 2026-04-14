"""CLI entry point for gitbriefly - backward compatible shim."""

import typer

from gitbriefly.cli import app

if __name__ == "__main__":
    app()
