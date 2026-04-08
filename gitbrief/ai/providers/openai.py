"""OpenAI AI provider."""

import json
import os
import re
from typing import Dict, List

import requests


class OpenAIProvider:
    """AI provider using OpenAI API."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")

    @property
    def name(self) -> str:
        return "openai"

    def complete(self, prompt: str) -> str:
        """Send prompt to OpenAI, return raw response."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        if not commits:
            return {"yesterday": [], "risks": [], "next_steps": []}

        if not self.api_key:
            return {
                "yesterday": [],
                "risks": ["OpenAI API key not set. Set OPENAI_API_KEY env variable."],
                "next_steps": [],
            }

        from gitbrief.ai.prompts import get_summarization_prompt

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

        if not self.api_key:
            return {
                "yesterday": [c["message"] for c in commits[:5]],
                "today": ["Continue working on pending tasks"],
                "blockers": ["OpenAI API key not set"],
            }

        from gitbrief.ai.prompts import get_standup_prompt

        prompt = get_standup_prompt(commits)
        try:
            response = self.complete(prompt)
            return self._parse_standup_response(response)
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

        result = {"yesterday": [], "risks": [], "next_steps": []}
        current_section = None
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            line_lower = line.lower()
            if "yesterday" in line_lower or "summary" in line_lower:
                current_section = "yesterday"
            elif "risk" in line_lower or "unfinished" in line_lower:
                current_section = "risks"
            elif "next" in line_lower or "suggest" in line_lower:
                current_section = "next_steps"
            elif line.startswith("•") or line.startswith("-") or line.startswith("*"):
                if current_section and current_section in result:
                    clean_line = line.lstrip("•*-").strip()
                    if clean_line:
                        result[current_section].append(clean_line)
            elif current_section and line:
                result[current_section].append(line)

        return result

    def _parse_standup_response(self, response: str) -> Dict[str, List[str]]:
        """Parse standup response."""
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
                return {
                    "yesterday": parsed.get("yesterday", []),
                    "today": parsed.get("today", []),
                    "blockers": parsed.get("blockers", []),
                }
            except json.JSONDecodeError:
                pass

        result = {"yesterday": [], "today": [], "blockers": []}
        current_section = None
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            line_lower = line.lower()
            if "yesterday" in line_lower:
                current_section = "yesterday"
            elif "today" in line_lower:
                current_section = "today"
            elif "blocker" in line_lower:
                current_section = "blockers"
            elif line.startswith("•") or line.startswith("-") or line.startswith("*"):
                if current_section and current_section in result:
                    clean_line = line.lstrip("•*-").strip()
                    if clean_line:
                        result[current_section].append(clean_line)
            elif current_section and line:
                result[current_section].append(line)

        return result

    def _fallback_summary(self, commits: List[Dict], error: str) -> Dict[str, List[str]]:
        """Fallback when OpenAI fails."""
        return {
            "yesterday": [c["message"] for c in commits[:5]],
            "risks": [f"OpenAI API error: {error}"],
            "next_steps": ["Check OPENAI_API_KEY environment variable"],
        }

    def _fallback_standup(self, commits: List[Dict], error: str) -> Dict[str, List[str]]:
        """Fallback standup."""
        return {
            "yesterday": [c["message"] for c in commits[:5]],
            "today": ["Continue working on pending tasks"],
            "blockers": [f"API error: {error}"],
        }
