"""Ollama AI provider."""

import json
import re
from typing import Dict, List

import requests

from gitbrief.ai.prompts import get_summarization_prompt, get_standup_prompt


class OllamaProvider:
    """AI provider using Ollama."""

    def __init__(
        self, model: str = "llama3", base_url: str = "http://localhost:11434", stream: bool = False
    ):
        self.model = model
        self.base_url = base_url
        self.stream = stream

    @property
    def name(self) -> str:
        return "ollama"

    def complete(self, prompt: str) -> str:
        """Send prompt to Ollama, return raw response."""
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": self.stream}

        if self.stream:
            response = requests.post(url, json=payload, timeout=60, stream=True)
            response.raise_for_status()
            full_response = ""
            for chunk in response.iter_lines():
                if chunk:
                    data = chunk.decode("utf-8")
                    if data.startswith("data:"):
                        data = data[5:]
                    try:
                        parsed = json.loads(data)
                        if "response" in parsed:
                            full_response += parsed["response"]
                            print(parsed["response"], end="", flush=True)
                    except json.JSONDecodeError:
                        pass
            print()
            return full_response
        else:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "")

    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        if not commits:
            return {"yesterday": [], "risks": [], "next_steps": []}

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

        return result if any(result.values()) else self._simple_parse(response)

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

    def _simple_parse(self, response: str) -> Dict[str, List[str]]:
        """Simple fallback parser."""
        result = {"yesterday": [], "risks": [], "next_steps": []}
        for section in response.split("\n\n"):
            lines = [line.strip() for line in section.split("\n") if line.strip()]
            if not lines:
                continue
            if "yesterday" in lines[0].lower():
                result["yesterday"] = lines[1:]
            elif "risk" in lines[0].lower():
                result["risks"] = lines[1:]
            elif "next" in lines[0].lower():
                result["next_steps"] = lines[1:]
        return result

    def _fallback_summary(self, commits: List[Dict], error: str) -> Dict[str, List[str]]:
        """Fallback when Ollama is unavailable."""
        repo_groups = {}
        for commit in commits:
            repo = commit.get("repo", "unknown")
            if repo not in repo_groups:
                repo_groups[repo] = []
            repo_groups[repo].append(commit["message"])

        result = {"yesterday": [], "risks": [], "next_steps": []}
        for repo, messages in repo_groups.items():
            result["yesterday"].append(f"[{repo}] {len(messages)} commits")

        result["risks"].append("No AI analysis available - Ollama may be offline")
        result["next_steps"].append("Ensure Ollama is running: ollama serve")
        return result

    def _fallback_standup(self, commits: List[Dict], error: str) -> Dict[str, List[str]]:
        """Fallback standup."""
        return {
            "yesterday": [c["message"] for c in commits[:5]],
            "today": ["Continue working on pending tasks"],
            "blockers": ["None"],
        }
