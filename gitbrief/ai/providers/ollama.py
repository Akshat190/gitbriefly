"""Ollama AI provider."""

import json
import re
import sys
from typing import Dict, List, Optional

import requests

try:
    from llm_json_repair import parse_json

    JSON_REPAIR_AVAILABLE = True
except ImportError:
    JSON_REPAIR_AVAILABLE = False

from gitbrief.ai.prompts import get_summarization_prompt, get_standup_prompt
from gitbrief.core.utils import get_config_value


class OllamaProvider:
    """AI provider using Ollama."""

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
        stream: bool = False,
        timeout: int = None,
        check_connection: bool = True,
    ):
        self.model = model
        self.base_url = base_url
        self.stream = stream
        self.timeout = timeout or get_config_value("timeout", 120)
        if check_connection:
            self._check_connection()
            self._validate_model()

    def _check_connection(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code != 200:
                print(
                    "[yellow]Warning: Ollama may not be running properly[/yellow]", file=sys.stderr
                )
        except Exception:
            print("[red]Error: Cannot connect to Ollama[/red]", file=sys.stderr)
            print("[dim]Fix: Run 'ollama serve' in a terminal[/dim]", file=sys.stderr)
            raise RuntimeError("Cannot connect to Ollama. Is it running?")

    def _validate_model(self):
        """Validate that the model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            models = response.json().get("models", [])
            available = [m.get("name", "") for m in models]
            if self.model not in available:
                print(f"[yellow]Warning: Model '{self.model}' not found[/yellow]", file=sys.stderr)
                print(
                    f"Available models: {', '.join(available) if available else 'None'}",
                    file=sys.stderr,
                )
                if available:
                    print(f"[dim]Using first available: {available[0]}[/dim]", file=sys.stderr)
                    self.model = available[0]
                else:
                    raise RuntimeError("No models available. Pull one with: ollama pull <model>")
        except RuntimeError:
            raise
        except Exception as e:
            print(f"[yellow]Warning: Could not verify model: {e}[/yellow]", file=sys.stderr)

    @property
    def name(self) -> str:
        return "ollama"

    def complete(self, prompt: str) -> str:
        """Send prompt to Ollama, return raw response."""
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": self.stream}

        if self.stream:
            response = requests.post(url, json=payload, timeout=self.timeout + 30, stream=True)
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
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("response", "")

    def summarize(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate summary from commits."""
        if not commits:
            return {"yesterday": [], "risks": [], "next_steps": []}

        prompt = get_summarization_prompt(commits)
        try:
            response = self.complete(prompt)
            result = self._parse_response(response)
            return self._clean_output(result)
        except Exception as e:
            return self._fallback_summary(commits, str(e))

    def summarize_for_standup(self, commits: List[Dict]) -> Dict[str, List[str]]:
        """Generate standup summary."""
        if not commits:
            return {"yesterday": [], "today": [], "blockers": []}

        prompt = get_standup_prompt(commits)
        try:
            response = self.complete(prompt)
            result = self._parse_standup_response(response)
            return self._clean_output(result)
        except Exception as e:
            return self._fallback_standup(commits, str(e))

    def _clean_output(self, result: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Clean and validate output."""
        if not result:
            # Return appropriate empty structure based on what keys we expect
            # Since we don't know the context here, return a generic structure
            # The calling functions should handle context-specific defaults
            return {"yesterday": [], "risks": [], "next_steps": []}

        cleaned = {}
        # Process whatever keys are present in the result
        for key, items in result.items():
            if not isinstance(items, list):
                items = []

            seen = set()
            clean_items = []
            for item in items:
                if not item or not isinstance(item, str):
                    continue
                item = item.strip()
                # Allow items with at least 1 character (more lenient than original 3)
                if len(item) < 1:
                    continue
                item_lower = item.lower()
                if item_lower in seen:
                    continue
                # Still enforce 50 character limit
                if len(item) > 50:
                    item = item[:47] + "..."
                clean_items.append(item)
                seen.add(item_lower)

            cleaned[key] = clean_items[:5]  # Still limit to 5 items per section

        # Ensure required keys exist with appropriate defaults
        # For summarization: yesterday, risks, next_steps
        # For standup: yesterday, today, blockers
        expected_summarization_keys = {"yesterday", "risks", "next_steps"}
        expected_standup_keys = {"yesterday", "today", "blockers"}

        # Determine context based on which keys are present in original result
        result_keys = set(result.keys())
        if expected_summarization_keys.issubset(result_keys) or (
            len(result_keys & expected_summarization_keys) >= 2
            and len(result_keys & expected_standup_keys) < 2
        ):
            # Looks like summarization context
            for key in expected_summarization_keys:
                if key not in cleaned:
                    cleaned[key] = []
            # Only set default for yesterday if it's empty and we're doing summarization
            if not cleaned.get("yesterday"):
                cleaned["yesterday"] = ["No activity detected"]
        elif expected_standup_keys.issubset(result_keys) or (
            len(result_keys & expected_standup_keys) >= 2
            and len(result_keys & expected_summarization_keys) < 2
        ):
            # Looks like standup context
            for key in expected_standup_keys:
                if key not in cleaned:
                    cleaned[key] = []
            # For standup, we don't set a default message - let it be empty if appropriate
        else:
            # Unknown context, ensure basics exist
            for key in ["yesterday", "risks", "next_steps"]:
                if key not in cleaned:
                    cleaned[key] = []

        return cleaned

    def _parse_response(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM JSON response with repair."""
        if JSON_REPAIR_AVAILABLE:
            result = parse_json(response, strict=False)
            if result.data:
                data = result.data
                return {
                    "yesterday": data.get("yesterday", []),
                    "risks": data.get("risks", []),
                    "next_steps": data.get("next_steps", []),
                }

        cleaned = self._extract_json(response)
        if cleaned:
            try:
                parsed = json.loads(cleaned)
                return {
                    "yesterday": parsed.get("yesterday", []),
                    "risks": parsed.get("risks", []),
                    "next_steps": parsed.get("next_steps", []),
                }
            except json.JSONDecodeError:
                pass

        return self._text_parse(response)

    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from text."""
        patterns = [
            r"```json\s*(\{.*?\})\s*```",
            r"```\s*(\{.*?\})\s*```",
            r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1) if match.group(1) else match.group()
        return None

    def _text_parse(self, response: str) -> Dict[str, List[str]]:
        """Parse text response."""
        result = {"yesterday": [], "risks": [], "next_steps": []}
        current = None
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            lower = line.lower()
            if "yesterday" in lower or "completed" in lower:
                current = "yesterday"
            elif "risk" in lower or "blocker" in lower or "unfinished" in lower:
                current = "risks"
            elif "next" in lower or "today" in lower or "plan" in lower:
                current = "next_steps"
            elif line.startswith("•") or line.startswith("-") or line.startswith("*"):
                if current and current in result:
                    clean = line.lstrip("•*-").strip()
                    if clean and len(clean) > 2:
                        result[current].append(clean)
            elif current and line and len(line) > 2:
                result[current].append(line)
        return result if any(result.values()) else self._simple_parse(response)

    def _parse_standup_response(self, response: str) -> Dict[str, List[str]]:
        """Parse standup response with repair."""
        if JSON_REPAIR_AVAILABLE:
            result = parse_json(response, strict=False)
            if result.data:
                data = result.data
                return {
                    "yesterday": data.get("yesterday", []),
                    "today": data.get("today", []),
                    "blockers": data.get("blockers", []),
                }

        cleaned = self._extract_json(response)
        if cleaned:
            try:
                parsed = json.loads(cleaned)
                return {
                    "yesterday": parsed.get("yesterday", []),
                    "today": parsed.get("today", []),
                    "blockers": parsed.get("blockers", []),
                }
            except json.JSONDecodeError:
                pass

        return self._text_parse_standup(response)

    def _text_parse_standup(self, response: str) -> Dict[str, List[str]]:
        """Parse standup text."""
        result = {"yesterday": [], "today": [], "blockers": []}
        current = None
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            lower = line.lower()
            if "yesterday" in lower or "completed" in lower:
                current = "yesterday"
            elif "today" in lower or "working" in lower or "plan" in lower:
                current = "today"
            elif "blocker" in lower or "stuck" in lower:
                current = "blockers"
            elif line.startswith("•") or line.startswith("-") or line.startswith("*"):
                if current and current in result:
                    clean = line.lstrip("•*-").strip()
                    if clean and len(clean) > 2:
                        result[current].append(clean)
            elif current and line and len(line) > 2:
                result[current].append(line)
        return result if any(result.values()) else self._simple_standup_parse(response)

    def _simple_standup_parse(self, response: str) -> Dict[str, List[str]]:
        """Simple standup fallback."""
        result = {"yesterday": [], "today": [], "blockers": []}
        for section in response.split("\n\n"):
            lines = [line.strip() for line in section.split("\n") if line.strip()]
            if not lines:
                continue
            if "yesterday" in lines[0].lower():
                result["yesterday"] = lines[1:]
            elif "today" in lines[0].lower():
                result["today"] = lines[1:]
            elif "blocker" in lines[0].lower():
                result["blockers"] = lines[1:]
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
        """Fallback when AI fails - create meaningful summary from commits."""
        print("[yellow]Note: Showing commit summary[/yellow]", file=sys.stderr)

        repo_groups = {}
        for commit in commits[:10]:
            repo = commit.get("repo", "unknown")
            if repo not in repo_groups:
                repo_groups[repo] = []
            msg = commit.get("message", "")[:40]
            repo_groups[repo].append(msg)

        result = {"yesterday": [], "risks": [], "next_steps": []}
        for repo, messages in repo_groups.items():
            if messages:
                result["yesterday"].append(f"{repo}: {len(messages)} changes")

        if len(commits) > 10:
            result["next_steps"].append(f"+ {len(commits) - 10} more commits")

        return result

    def _fallback_standup(self, commits: List[Dict], error: str) -> Dict[str, List[str]]:
        """Fallback standup."""
        items = [c.get("message", "")[:40] for c in commits[:3]]
        if not items:
            items = ["No commits"]
        return {
            "yesterday": items,
            "today": ["Continue pending work"],
            "blockers": ["None"],
        }
