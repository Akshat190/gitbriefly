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

TASK: Create a concise daily briefing from these commits by summarizing what was accomplished, identifying risks, and suggesting next steps.

COMMITS TO PROCESS:
{commits_text}

{QUALITY_CHECK}

INSTRUCTIONS:
1. Summarize commits into meaningful activities (don't list commit messages verbatim)
2. Group similar changes together (e.g., "Fixed multiple bugs in auth module" instead of listing each fix)
3. Focus on user-visible changes and technical accomplishments
4. Identify potential risks or blockers from the commits
5. Suggest logical next steps based on the work done

OUTPUT FORMAT (MUST BE VALID JSON ONLY):
{{
  "yesterday": ["specific accomplishment 1", "specific accomplishment 2"],
  "risks": ["potential issue if any", "another risk"],
  "next_steps": ["logical next action", "follow-up task"]
}}

EXAMPLES:
Good: {{"yesterday": ["Implemented user authentication", "Fixed validation bug in login form"], "risks": ["Auth service may need rate limiting"], "next_steps": ["Add OAuth integration"]}}
Good: {{"yesterday": ["Refactored database layer for performance", "Added unit tests for user service"], "risks": [], "next_steps": ["Monitor query performance after deploy"]}}
Needs improvement: {{"yesterday": ["Fixed bug #123", "Updated README"], "risks": [], "next_steps": ["Fix bug #456"]}} (too vague)

{JSON_PROMPT_SUFFIX}"""

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

TASK: Create a weekly summary from these commits by identifying major accomplishments, risks, and goals for next week.

WEEKLY COMMITS BY DAY:
{commits_text}

{QUALITY_CHECK}

INSTRUCTIONS:
1. Summarize the week's work into meaningful accomplishments (don't just list commit counts)
2. Group similar work across days (e.g., "Worked on user authentication system throughout the week")
3. Identify any risks or technical debt accumulated during the week
4. Suggest goals for next week based on progress made
5. Focus on trends and patterns rather than individual commits

OUTPUT FORMAT (MUST BE VALID JSON ONLY):
{{
  "yesterday": ["major accomplishment from the week", "another key achievement"],
  "risks": ["technical debt concern", "potential blocker"],
  "next_steps": ["goal for next week", "follow-up task"]
}}

EXAMPLES:
Good: {{"yesterday": ["Completed user authentication module", "Implemented API rate limiting"], "risks": ["Auth module needs security review"], "next_steps": ["Begin work on user dashboard"]}}
Good: {{"yesterday": ["Fixed critical database performance issues", "Added comprehensive test suite"], "risks": [], "next_steps": ["Performance monitoring setup"]}}
Needs improvement: {{"yesterday": ["Made 15 commits this week", "Fixed some bugs"], "risks": [], "next_steps": ["Continue work"]}} (too vague)

{JSON_PROMPT_SUFFIX}"""

    return prompt


def get_standup_prompt(commits: List[Dict]) -> str:
    """Generate prompt for standup message."""

    commit_summary = []
    for commit in commits[:10]:
        commit_summary.append(f"- {commit['message']}")

    commits_text = "\n".join(commit_summary)

    prompt = f"""You are a developer preparing a daily standup.

TASK: Convert these commits into a standup message by summarizing what was completed, what will be worked on today, and identifying any blockers.

COMMITS FROM YESTERDAY:
{commits_text}

{QUALITY_CHECK}

INSTRUCTIONS:
1. Summarize commits into meaningful completed work (DO NOT list commit messages verbatim)
2. Group similar completed tasks together (e.g., "Fixed multiple bugs in authentication system")
3. For "today": based on the commits, suggest logical next steps or continuation of work
4. Identify any blockers or issues that might impede progress (look for mentions of failures, errors, or incomplete work)
5. Be concise and focus on what matters for team coordination

OUTPUT FORMAT (MUST BE VALID JSON ONLY):
{{
  "yesterday": ["specific completed task 1", "specific completed task 2"],
  "today": ["planned task for today", "follow-up activity"],
  "blockers": ["blocking issue if any", "another blocker"]
}}

EXAMPLES:
Good: {{"yesterday": ["Implemented user login functionality", "Fixed validation errors in signup form"], "today": ["Work on password reset feature", "Write unit tests for auth module"], "blockers": ["Waiting for API documentation from backend team"]}}
Good: {{"yesterday": ["Refactored database queries for better performance", "Added indexing on frequently queried columns"], "today": ["Monitor query performance after deploy", "Optimize remaining slow queries"], "blockers": []}}
Needs improvement: {{"yesterday": ["Fixed bug #123", "Updated dependencies"], "today": ["Fix bug #456"], "blockers": []}} (just listing commits rather than summarizing)

{STANDUP_PROMPT_SUFFIX}"""

    return prompt



