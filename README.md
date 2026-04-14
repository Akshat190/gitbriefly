# gitbriefly 🧠

[![PyPI version](https://img.shields.io/pypi/v/gitbriefly)](https://pypi.org/project/gitbriefly/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Akshat190/gitbriefly?style=social)](https://github.com/Akshat190/gitbriefly)

Your daily developer standup — powered by your Git history.

---

## ⚡ The Problem

Every day at standup:

“What did I actually do yesterday?”

You open Git, scroll commits, and still feel unsure.

---

## ⚡ Quick Demo

<img src="https://raw.githubusercontent.com/Akshat190/gitbriefly/main/assets/gitbriefly-gif.gif" width="600" alt="gitbriefly demo"/>

```bash
$ pip install gitbriefly
$ gitbriefly standup
**Yesterday:**
- Enhanced AI output quality
- Added deduplication and truncation

**Today:**
- Continue development

**Blockers:**
- None
```

**Your standup ready in seconds.**

---

## 🚀 Install

### From PyPI (recommended)
```bash
pip install gitbriefly
```

### With OpenAI support
```bash
pip install gitbriefly[openai]
```

### With Anthropic support
```bash
pip install gitbriefly[anthropic]
```

### From source
```bash
pip install -e .
```

**Prerequisite:** [Ollama](https://ollama.ai) must be installed and running.

```bash
ollama serve
ollama pull llama3
```

---

## 🧪 Usage

```bash
# Today's summary (last 7 days)
gitbriefly today

# Weekly summary (last 7 days)
gitbriefly week

# Generate standup message (viral feature!)
gitbriefly standup

# Diagnose issues
gitbriefly doctor

# Commit statistics
gitbriefly stats
gitbriefly stats --days 30

# View past summaries
gitbriefly history
gitbriefly history --days 14

# Scan a specific repository
gitbriefly today --path /path/to/repo

# Scan multiple repositories
gitbriefly week --path /path/to/repos

# Filter by author
gitbriefly today --author yourname

# Filter by branch
gitbriefly today --branch main

# Custom date range
gitbriefly today --since 2024-01-01 --until 2024-01-07

# Days to look back (default: 7)
gitbriefly today --days-ago 14

# Limit commits processed
gitbriefly today --max-commits 50

# Use different AI model
gitbriefly today --model mistral

# Use OpenAI instead of Ollama
gitbriefly today --provider openai --model gpt-3.5-turbo

# Use Anthropic
gitbriefly today --provider anthropic --model claude-3-haiku-20240307

# Stream AI response (Ollama only)
gitbriefly today --stream

# Export to markdown file
gitbriefly today --export report.md

# Export as JSON for scripting
gitbriefly today --json
gitbriefly standup --json

# Show raw commits without AI
gitbriefly today --no-ai
```

---

## ⚙️ Configuration

Create `~/.gitbriefly.toml` to set defaults:

```toml
path = "/path/to/repos"
model = "llama3"
provider = "ollama"
timeout = 120
```

---

## 📁 Options

| Option | Alias | Description | Default |
|--------|-------|-------------|---------|
| `--path` | `-p` | Path to Git repo or directory | `.` |
| `--model` | `-m` | AI model to use | auto-detect |
| `--provider` | - | AI provider: `ollama`, `openai`, `anthropic` | `ollama` |
| `--days-ago` | - | Days to look back | `7` |
| `--max-commits` | - | Max commits to process | `100` |
| `--no-ai` | - | Skip AI, show raw commits | `false` |
| `--json` | `-j` | Output as JSON | `false` |
| `--stream` | - | Stream AI response (Ollama) | `false` |
| `--export` | `-e` | Export to file | - |
| `--since` | - | Start date (ISO format) | - |
| `--until` | - | End date (ISO format) | - |
| `--author` | - | Filter by author | - |
| `--branch` | `-b` | Filter by branch | - |

---

## 🗂️ Commands

| Command | Description |
|---------|-------------|
| `today` | Daily summary (last 7 days, for standups) |
| `week` | Weekly summary (last 7 days) |
| `standup` | Yesterday/Today/Blockers format |
| `stats` | Commit statistics |
| `history` | Past summaries |
| `doctor` | Diagnose issues & check setup |
| `version` | Show version |

---

## 🧠 Why this exists

Developers forget context. Git stores history but not understanding.

gitbriefly turns commits into insights.

> "I built this because I kept forgetting what I worked on the day before. Now I just run `gitbriefly` and know exactly what to continue working on."

---

## 🔧 Development

```bash
# Clone the repo
git clone https://github.com/Akshat190/gitbriefly.git
cd gitbriefly

# Install in development mode
pip install -e .

# Run tests
pytest

# Run linting
ruff check gitbriefly/

# Run CLI
python -m gitbriefly.cli today --path .
python -m gitbriefly.cli stats
```

---

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## ⭐ Star this repo if it saved you time

[![GitHub Stars](https://img.shields.io/github/stars/Akshat190/gitbriefly?style=social)](https://github.com/Akshat190/gitbriefly)

---

<p align="center">
Made with ❤️ for developers
</p>
