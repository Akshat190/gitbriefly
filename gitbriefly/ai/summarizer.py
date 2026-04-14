"""Main summarizer that wraps providers."""

from typing import Dict, List

from gitbriefly.ai.providers import get_provider, BaseProvider


class Summarizer:
    """Main summarizer class that delegates to providers."""

    def __init__(self, provider: str = "ollama", model: str = "llama3", **kwargs):
        self.provider: BaseProvider = get_provider(provider, model, **kwargs)

    @property
    def name(self) -> str:
        return self.provider.name

    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        return self.provider.summarize(commits)

    def summarize_for_standup(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate standup summary."""
        return self.provider.summarize_for_standup(commits)
