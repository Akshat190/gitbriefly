"""Prompt templates for AI summarization."""

from typing import Dict, List


JSON_PROMPT_SUFFIX = """

IMPORTANT: Respond ONLY with a JSON object. No markdown. No preamble. Use this exact format:
{"yesterday": ["item 1", "item 2"], "risks": ["item 1"], "next_steps": ["item 1"]}

Do not include any other text in your response."""


STANDUP_PROMPT_SUFFIX = """

IMPORTANT: Respond ONLY with a JSON object. No markdown. No preamble. Use this exact format:
{"yesterday": ["item 1", "item 2"], "today": ["item 1"], "blockers": ["item 1"]}

Do not include any other text in your response."""


def get_summarization_prompt(commits: List[Dict]) -> str:
    """Generate prompt for summarizing Git commits."""

    commit_summary = []
    for commit in commits:
        files_info = ""
        if commit.get("files"):
            files_info = f" (files: {', '.join(commit['files'][:5])}"
            if len(commit["files"]) > 5:
                files_info += f", +{len(commit['files']) - 5} more"
            files_info += ")"

        commit_summary.append(f"- [{commit['repo']}] {commit['message']}{files_info}")

    commits_text = "\n".join(commit_summary)

    prompt = f"""You are a developer assistant that summarizes Git activity into a daily briefing.

Analyze the following commits from the last 24 hours and create a structured summary.

Commits:
{commits_text}

Generate a briefing with these three sections:

## Yesterday
List the main work done. Group by theme/project. Use bullet points.

## Risks  
Identify potential issues:
- Unfinished work (WIP commits, "todo" in messages)
- Risky changes (large refactors, security-related)
- Missing tests or error handling

## Next Steps
Suggest logical next actions based on the commits.

Be concise and actionable.{JSON_PROMPT_SUFFIX}"""

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
        repo_groups = {}
        for c in day_commits:
            repo = c.get("repo", "unknown")
            if repo not in repo_groups:
                repo_groups[repo] = []
            repo_groups[repo].append(c["message"])

        summary = f"{day}:\n"
        for repo, msgs in repo_groups.items():
            summary += f"  [{repo}]: {len(msgs)} commits\n"

        daily_summaries.append(summary)

    commits_text = "\n".join(daily_summaries)

    prompt = f"""You are a developer assistant that summarizes Git activity into a weekly briefing.

Analyze the following commits from the last 7 days.

Commits by day:
{commits_text}

Generate a weekly briefing with:

## 🧠 Week Summary
What was accomplished each day. Group by project.

## ⚠️ Risks
Potential issues or unfinished work.

## 🎯 This Week's Goals
What should be focused on next week.

Be concise."""

    return prompt


def get_standup_prompt(commits: List[Dict]) -> str:
    """Generate prompt for standup message (Yesterday / Today / Blockers)."""

    commit_summary = []
    for commit in commits[:10]:
        files_info = ""
        if commit.get("files"):
            files_info = f" ({', '.join(commit['files'][:3])})"

        commit_summary.append(f"- {commit['message']}{files_info}")

    commits_text = "\n".join(commit_summary)

    prompt = f"""You are a developer preparing a daily standup update.

Based on these commits from yesterday:
{commits_text}

Generate a standup message in this exact format:

## Yesterday
- [What you completed]

## Today
- [What you plan to work on]

## Blockers
- [Any blockers or challenges]

For "Today", infer logical next steps from the commits.
For "Blockers", identify any risks or unfinished work.
Be concise - 3-5 items per section max.{STANDUP_PROMPT_SUFFIX}"""

    return prompt
