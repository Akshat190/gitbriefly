"""Memory storage for gitbrief."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


MEMORY_FILE = Path("memory.json")


def load_memory() -> List[Dict]:
    """Load memory.json data."""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE) as f:
            return json.load(f).get("summaries", [])
    return []


def save_summary(summary: Dict) -> None:
    """Save a summary to memory.json."""
    data = {"summaries": [], "last_updated": datetime.now().isoformat()}

    if MEMORY_FILE.exists():
        with open(MEMORY_FILE) as f:
            data = json.load(f)

    data.setdefault("summaries", []).append(
        {
            "date": datetime.now().isoformat(),
            "summary": summary,
        }
    )

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_history(days: int = 7) -> List[Dict]:
    """Get summaries from the last N days."""
    memory = load_memory()
    return memory[-days:] if memory else []
