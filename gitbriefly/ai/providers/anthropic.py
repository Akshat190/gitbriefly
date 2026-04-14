"""Anthropic AI provider."""

import json
import os
import re
import sys
from typing import Dict, List

from gitbriefly.core.utils import get_config_value

try:
    from anthropic import Anthropic as AnthropicClient

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AnthropicProvider:
    """AI provider using Anthropic API."""

    def __init__(self, model: str = "claude-3-haiku-20240307", timeout: int = None):
        self.model = model
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.timeout = timeout or get_config_value("timeout", 120)
        self._validate_api_key()
        self.client = (
            AnthropicClient(api_key=self.api_key)
            if self.api_key and ANTHROPIC_AVAILABLE
            else None
        )

    def _validate_api_key(self):
        """Validate that API key is set."""
        if not self.api_key:
            print(
                "[red]Error: Anthropic provider selected but ANTHROPIC_API_KEY not set[/red]",
                file=sys.stderr,
            )
            print("[dim]Fix: export ANTHROPIC_API_KEY=your-key[/dim]", file=sys.stderr)
            raise ValueError("ANTHROPIC_API_KEY not set")
        if not ANTHROPIC_AVAILABLE:
            print("[red]Error: Anthropic package not installed[/red]", file=sys.stderr)
            print("[dim]Fix: pip install anthropic[/dim]", file=sys.stderr)
            raise ImportError(
                "Anthropic package not installed. Run: pip install anthropic"
            )

    @property
    def name(self) -> str:
        return "anthropic"

    def complete(self, prompt: str) -> str:
        """Send prompt to Anthropic, return raw response."""
        if not self.client:
            raise ValueError("Anthropic API key not set")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        if not commits:
            return {"yesterday": [], "risks": [], "next_steps": []}

        if not self.client:
            return {
                "yesterday": [],
                "risks": [
                    "Anthropic API key not set. Set ANTHROPIC_API_KEY env variable."
                ],
                "next_steps": [],
            }

        from gitbriefly.ai.prompts import get_summarization_prompt

        prompt = get_summarization_prompt(commits)
        try:
            response = self.complete(prompt)
            return self._parse_response(response)
        except Exception as e:
            return self._fallback_summary(commits, str(e))

    def summarize_for_standup(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate standup summary."""
        if not commits:
            return {"yesterday": [], "today": [], "blockers": []}

        if not self.client:
            return {
                "yesterday": [c["message"] for c in commits[:5]],
                "today": ["Continue working on pending tasks"],
                "blockers": ["Anthropic API key not set"],
            }

        from gitbriefly.ai.prompts import get_standup_prompt

        prompt = get_standup_prompt(commits)
        try:
            response = self.complete(prompt)
            return self._parse_response(response)
        except Exception as e:
            return self._fallback_standup(commits, str(e))

    def _parse_response(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM JSON response."""
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return {
                    "yesterday": parsed.get("yesterday", []),
                    "risks": parsed.get("risks", []),
                    "next_steps": parsed.get("next_steps", []),
                }
            except json.JSONDecodeError:
                pass

        return {"yesterday": [], "risks": [], "next_steps": []}

    def _fallback_summary(
        self, commits: List[Dict], error: str
    ) -> Dict[str, List[str]]:
        """Fallback when Anthropic fails."""
        return {
            "yesterday": [c["message"] for c in commits[:5]],
            "risks": [f"Anthropic API error: {error}"],
            "next_steps": ["Check ANTHROPIC_API_KEY environment variable"],
        }

    def _fallback_standup(
        self, commits: List[Dict], error: str
    ) -> Dict[str, List[str]]:
        """Fallback standup."""
        return {
            "yesterday": [c["message"] for c in commits[:5]],
            "today": ["Continue working on pending tasks"],
            "blockers": [f"API error: {error}"],
        }
