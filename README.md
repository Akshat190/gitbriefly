# gitbrief 🧠

[![PyPI version](https://img.shields.io/pypi/v/gitbrief)](https://pypi.org/project/gitbrief/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Akshat190/gitbrief?style=social)](https://github.com/Akshat190/gitbrief)

Your daily developer standup — powered by your Git history.

---

## ⚡ The Problem

Every day at standup:

“What did I actually do yesterday?”

You open Git, scroll commits, and still feel unsure.

---

## 🚀 The Solution

gitbrief turns your Git history into a clean standup in seconds.

```bash
gitbrief standup
## ⚡ Quick Demo

```bash
# Install and run
$ pip install gitbrief

$ gitbrief today
✓ Found 13 commits across 2 repositories
✓ Generating AI summary...
✓ Done in 3s
```

**You'll be surprised how much you forget after 1 day.**

---

## 🚀 Install

### From PyPI (recommended)
```bash
pip install gitbrief
```

### With OpenAI support
```bash
pip install gitbrief[openai]
```

### With Anthropic support
```bash
pip install gitbrief[anthropic]
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
# Today's summary (last 24 hours)
gitbrief today

# Weekly summary (last 7 days)
gitbrief week

# Generate standup message (viral feature!)
gitbrief standup

# Commit statistics
gitbrief stats
gitbrief stats --days 30

# View past summaries
gitbrief history
gitbrief history --days 14

# Scan a specific repository
gitbrief today --path /path/to/repo

# Scan multiple repositories
gitbrief week --path /path/to/repos

# Filter by author
gitbrief today --author yourname

# Filter by branch
gitbrief today --branch main

# Custom date range
gitbrief today --since 2024-01-01 --until 2024-01-07

# Use different AI model
gitbrief today --model mistral

# Use OpenAI instead of Ollama
gitbrief today --provider openai --model gpt-3.5-turbo

# Use Anthropic
gitbrief today --provider anthropic --model claude-3-haiku-20240307

# Stream AI response (Ollama only)
gitbrief today --stream

# Export to markdown file
gitbrief today --export report.md

# Export as JSON for scripting
gitbrief today --json
gitbrief standup --json

# Show raw commits without AI
gitbrief today --no-ai
```

---

## ⚙️ Configuration

Create `~/.gitbrief.toml` to set defaults:

```toml
path = "/path/to/repos"
model = "llama3"
provider = "ollama"
```

---

## 📁 Options

| Option | Alias | Description | Default |
|--------|-------|-------------|---------|
| `--path` | `-p` | Path to Git repo or directory | `.` |
| `--model` | `-m` | AI model to use | `llama3` |
| `--provider` | - | AI provider: `ollama`, `openai`, `anthropic` | `ollama` |
| `--no-ai` | - | Skip AI, show raw commits | `false` |
| `--json` | `-j` | Output as JSON | `false` |
| `--stream` | - | Stream AI response (Ollama) | `false` |
| `--export` | `-e` | Export to file | - |
| `--since` | - | Start date (ISO or days) | - |
| `--until` | - | End date (ISO) | - |
| `--author` | - | Filter by author | - |
| `--branch` | `-b` | Filter by branch | - |

---

## 🗂️ Commands

| Command | Description |
|--------|-------------|
| `today` | Last 24 hours summary |
| `week` | Last 7 days summary |
| `standup` | Yesterday/Today/Blockers |
| `stats` | Commit statistics |
| `history` | Past summaries |
| `version` | Show version |

---

## 🧠 Why this exists

Developers forget context. Git stores history but not understanding.

gitbrief turns commits into insights.

> "I built this because I kept forgetting what I worked on the day before. Now I just run `gitbrief` and know exactly what to continue working on."

---

## 🔧 Development

```bash
# Clone the repo
git clone https://github.com/Akshat190/gitbrief.git
cd gitbrief

# Install in development mode
pip install -e .

# Run tests
pytest

# Run linting
ruff check gitbrief/

# Run CLI
python -m gitbrief.cli today --path .
python -m gitbrief.cli stats
```

---

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## ⭐ Star this repo if it saved you time

[![GitHub Stars](https://img.shields.io/github/stars/Akshat190/gitbrief?style=social)](https://github.com/Akshat190/gitbrief)

---

<p align="center">
Made with ❤️ for developers
</p>
