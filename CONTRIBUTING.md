# Contributing to gitbrief

Thank you for your interest in contributing to gitbrief! This guide will help you get started.

## 🧠 What is gitbrief?

gitbrief is a CLI tool that analyzes your Git activity across repositories and generates daily intelligent briefings. It answers:
- What did I work on?
- What is unfinished?
- What should I do next?

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Ollama (optional, for AI summaries)

### Setup

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/Akshat190/gitbrief.git
cd gitbrief

# Install in development mode
pip install -e .

# Test the CLI
python -m gitbrief.cli --help
python -m gitbrief.cli today --path .
```

## 🛠️ Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Follow existing code style (see Code Style below)
- Add tests for new functionality
- Keep functions small and focused

### 3. Test Your Changes

```bash
# Test CLI commands
python -m gitbrief.cli today --path . --no-ai
python -m gitbrief.cli week --path . --no-ai
python -m gitbrief.cli stats

# Run linting
ruff check gitbrief/

# Run tests
pytest
```

### 4. Submit a Pull Request

1. Push your changes:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   git push origin your-branch-name
   ```

2. Open a Pull Request on GitHub

3. Fill in the PR template

## 🎯 Good First Issues

Looking for a way to contribute? Here are some beginner-friendly issues:

### Easy
- Add test cases for existing modules
- Improve error messages
- Add Windows compatibility fixes

### Intermediate
- Implement new exporters (Slack, Notion)
- Add more statistics to `stats` command
- Improve AI prompts

### Advanced
- Implement caching system
- Add VS Code extension

## 📝 Code Style

- Use **PEP 8** for Python code
- Run `ruff check gitbrief/` before submitting
- Keep lines under 100 characters
- Use type hints where possible
- Use descriptive variable names

## 🧪 Testing

Tests are in the `tests/` directory. Run them with:

```bash
pytest
```

## 📂 Package Structure

```
gitbrief/
├── __init__.py        (version)
├── cli.py           (entry point)
├── core/           (Git access)
│   ├── git_reader.py
│   ├── utils.py
│   └── memory.py
├── ai/             (AI layer)
│   ├── summarizer.py
│   ├── prompts.py
│   └── providers/
│       ├── ollama.py
│       ├── openai.py
│       └── anthropic.py
├── commands/         (CLI commands)
│   ├── today.py
│   ├── week.py
│   ├── standup.py
│   ├── stats.py
│   └── history.py
└── exporters/       (output)
    ├── markdown.py
    └── json.py
```

## 🤝 Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 💬 Getting Help

- Open an issue for bugs or feature requests
- Star the repo if it helps you!
- Share with other developers

## ⭐ Show Your Support

If gitbrief saved you time, give it a star! It helps others discover the project.

---

**Happy Coding!** 🚀