"""Markdown exporter."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional


class BaseExporter(ABC):
    """Base class for all exporters."""

    @abstractmethod
    def export(self, summary: Dict, path: Optional[str] = None) -> str:
        """Export summary. Returns output path or confirmation string."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Exporter name."""
        ...


class MarkdownExporter(BaseExporter):
    """Export summary as Markdown."""

    @property
    def name(self) -> str:
        return "markdown"

    def export(self, summary: Dict, path: Optional[str] = None) -> str:
        """Export summary to markdown."""
        lines = [f"# Git Brief - {datetime.now().strftime('%Y-%m-%d')}", ""]

        if "yesterday" in summary and summary["yesterday"]:
            lines.append("## Yesterday")
            lines.append("")
            for item in summary["yesterday"]:
                lines.append(f"- {item}")
            lines.append("")

        if "risks" in summary and summary["risks"]:
            lines.append("## Risks")
            lines.append("")
            for item in summary["risks"]:
                lines.append(f"- ! {item}")
            lines.append("")

        if "next_steps" in summary and summary["next_steps"]:
            lines.append("## Next Steps")
            lines.append("")
            for item in summary["next_steps"]:
                lines.append(f"- > {item}")
            lines.append("")

        content = "\n".join(lines)

        if path:
            with open(path, "w") as f:
                f.write(content)
            return path

        return content
