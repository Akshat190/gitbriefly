"""JSON exporter."""

import json
from typing import Dict, Optional


class JSONExporter:
    """Export summary as JSON."""

    @property
    def name(self) -> str:
        return "json"

    def export(self, summary: Dict, path: Optional[str] = None) -> str:
        """Export summary to JSON."""
        content = json.dumps(summary, indent=2)

        if path:
            with open(path, "w") as f:
                f.write(content)
            return path

        return content
