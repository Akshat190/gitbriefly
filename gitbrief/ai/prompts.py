"""Prompt templates for AI summarization."""

from typing import Dict, List


QUALITY_CHECK = """
STRICT RULES (you MUST follow):
- Output MUST contain only information from the provided commits
- Do NOT add items that aren't supported by the commits
- If no meaningful risks exist, use empty array []
- Each item MUST be under 50 characters
- Include at least 2 items in "yesterday" if commits exist
- NEVER include raw commit messages verbatim - summarize them
- Be concise - max 5 items per section
- Group similar items together"""


JSON_PROMPT_SUFFIX = """

RESPONSE FORMAT (REQUIRED):
You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanation.

JSON Schema:
{"yesterday": ["completed work"], "risks": ["issues"], "next_steps": ["actions"]}

Rules:
- All fields are required arrays
- Each string under 50 characters
- Empty arrays [] allowed
- No extra fields"""


STANDUP_PROMPT_SUFFIX = """

RESPONSE FORMAT (REQUIRED):
You MUST respond with ONLY valid JSON. No markdown, no code blocks, no explanation.

JSON Schema:
{"yesterday": ["completed"], "today": ["planned"], "blockers": ["issues"]}

Rules:
- All fields are required arrays
- Each string under 50 characters
- Empty arrays [] allowed"""


def get_summarization_prompt(commits: List[Dict]) -> str:
    """Generate prompt for summarizing Git commits."""

    commit_summary = []
    for commit in commits:
        files_info = ""
        if commit.get("files"):
            files_info = f" ({', '.join(commit['files'][:3])})"
        commit_summary.append(f"- {commit['message']}{files_info}")

    commits_text = "\n".join(commit_summary[:15])

    prompt = f"""You are a developer assistant that summarizes Git commits.

TASK: Create a concise daily briefing from these commits.

Commits:
{commits_text}

{QUALITY_CHECK}

Output this JSON (no other text):
{{"yesterday": ["summarized item 1", "summarized item 2"], "risks": ["risk if any"], "next_steps": ["next action"]}}

Example: {{"yesterday": ["Added user auth", "Fixed login bug"], "risks": [], "next_steps": ["Add logout"]}}{JSON_PROMPT_SUFFIX}"""

    return prompt


def get_week_summarization_prompt(commits: List[Dict]) -> str:
    """Generate prompt for weekly summary."""

    by_day = {}
    for commit in commits:
        day = commit.get("date", "")[:10]
        if day not in by_day:
            by_day[day] = []
        by_day[day].append(commit)

    daily_summaries = []
    for day, day_commits in sorted(by_day.items()):
        msgs = [c["message"] for c in day_commits]
        daily_summaries.append(f"{day}: {len(msgs)} commits")

    commits_text = "\n".join(daily_summaries)

    prompt = f"""You are a developer assistant that summarizes Git commits.

TASK: Create a weekly summary from these commits.

Commits by day:
{commits_text}

{QUALITY_CHECK}

Output this JSON:
{{"yesterday": ["week summary"], "risks": ["issues"], "next_steps": ["next week goals"]}}{JSON_PROMPT_SUFFIX}"""

    return prompt


def get_standup_prompt(commits: List[Dict]) -> str:
    """Generate prompt for standup message."""

    commit_summary = []
    for commit in commits[:10]:
        commit_summary.append(f"- {commit['message']}")

    commits_text = "\n".join(commit_summary)

    prompt = f"""You are a developer preparing a daily standup.

TASK: Convert these commits into a standup message.

Commits:
{commits_text}

{QUALITY_CHECK}

Output this JSON:
{{"yesterday": ["completed work"], "today": ["planned work"], "blockers": ["issues if any"]}}

Example: {{"yesterday": ["Fixed auth bug", "Added login"], "today": ["Work on dashboard"], "blockers": []}}{STANDUP_PROMPT_SUFFIX}"""

    return prompt
