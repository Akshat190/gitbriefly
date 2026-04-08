"""AI provider interface and factory."""

from abc import ABC, abstractmethod
from typing import Dict, List

from gitbrief.ai.providers.ollama import OllamaProvider
from gitbrief.ai.providers.openai import OpenAIProvider
from gitbrief.ai.providers.anthropic import AnthropicProvider


class BaseProvider(ABC):
    """Base class for all AI providers."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Send prompt, return raw text response."""
        ...

    @abstractmethod
    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        ...

    @abstractmethod
    def summarize_for_standup(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate standup summary."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        ...


def get_provider(provider: str, model: str = "llama3", **kwargs):
    """Get provider instance by name."""
    providers = {
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }
    provider_class = providers.get(provider, OllamaProvider)
    return provider_class(model=model, **kwargs)


__all__ = ["BaseProvider", "get_provider", "OllamaProvider", "OpenAIProvider", "AnthropicProvider"]
