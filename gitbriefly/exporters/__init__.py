"""Exporters package."""

from abc import ABC, abstractmethod
from typing import Dict, Optional

from gitbriefly.exporters.markdown import MarkdownExporter
from gitbriefly.exporters.json import JSONExporter


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


def get_exporter(exporter: str, **kwargs):
    """Get exporter instance by name."""
    exporters = {
        "markdown": MarkdownExporter,
        "json": JSONExporter,
    }
    exporter_class = exporters.get(exporter, MarkdownExporter)
    return exporter_class(**kwargs)


__all__ = ["BaseExporter", "get_exporter", "MarkdownExporter", "JSONExporter"]
