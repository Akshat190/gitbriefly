# gitbrief 🧠

> Your daily developer standup — powered by your Git history.

[![PyPI version](https://img.shields.io/pypi/v/gitbrief)](https://pypi.org/project/gitbrief/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Akshat190/gitbrief?style=social)](https://github.com/Akshat190/gitbrief)

---

## ⚡ The Problem

Every day at standup:

“What did I actually do yesterday?”

You open Git.  
Scroll commits.  
Try to remember.  

Still unclear.

---

## 🚀 The Solution

**gitbrief turns your Git history into a clean standup in seconds.**

No thinking. No scrolling. No manual writing.

```bash
gitbrief standup
```

---

## ✨ What You Get

- 📌 Yesterday → What you worked on  
- 🎯 Today → What to focus on next  
- ⚠️ Blockers → What might be broken  
- 📊 Stats → Commit insights  

---

## 🔥 Example Output

```md
## Yesterday
- Fixed authentication bug
- Refactored API routes
- Added caching layer

## Today
- Optimize performance
- Write unit tests

## Blockers
- API timeout issue in production
```

👉 Copy. Paste. Done.

---

## ⚡ Quick Demo

```bash
$ pip install gitbrief
$ gitbrief today

✓ Found 13 commits across 2 repositories
✓ Generating AI summary...
✓ Done in 3s
```

---

## 🚀 Installation

```bash
pip install gitbrief
```

---

## ⚙️ Requirements

```bash
ollama serve
ollama pull llama3
```

---

## 🧪 Usage

```bash
gitbrief today
gitbrief week
gitbrief standup
gitbrief stats
gitbrief history
```

---

## 🤖 AI Providers

```bash
gitbrief today --provider openai --model gpt-3.5-turbo
gitbrief today --provider anthropic --model claude-3-haiku-20240307
```

---

## 📤 Export Options

```bash
gitbrief today --export report.md
gitbrief standup --json
```

---

## ⚙️ Configuration

```toml
path = "/path/to/repos"
model = "llama3"
provider = "ollama"
```

---

## 🧠 Why gitbrief?

Git stores history.

But not understanding.

gitbrief converts raw commits into meaningful insights.

---

## 🎯 Who is this for?

- Developers doing daily standups  
- Freelancers tracking work  
- Indie hackers juggling projects  

---

## 🤝 Contributing

PRs welcome!

---

## ⭐ Support

If this saved you even 10 minutes:

👉 Star the repo  
👉 Share with your team  

---

## 📝 License

MIT License
