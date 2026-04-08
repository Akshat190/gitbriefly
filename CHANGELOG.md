# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-04-08

### Added
- CLI commands: `today` (last 24h) and `week` (last 7 days)
- Git repository scanning (single and multi-repo)
- Commit message, files changed, and timestamp extraction
- Time-based filtering for commits
- Ollama API integration for AI summarization
- Rich-formatted terminal output
- Fallback handling when Ollama is offline
- Multi-repository support (scan directories)

### Changed
- Initial release

---

## [Unreleased]

### Planned Features
- `gitbrief replay` - Timeline narration
- `gitbrief explain` - Repository purpose explanation
- Configuration file support
- JSON output flag
- Custom date range filters (--since/--until)
- Local caching for progress tracking

---

## Support

For feature requests and bug reports, please open an issue at:
https://github.com/Akshat190/gitbrief/issues

---

*This changelog was generated using [git-chglog](https://github.com/git-chglog/git-chglog) concepts.*
