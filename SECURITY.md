# Security Policy

## Supported Versions

The following versions of gitbrief are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

---

## Reporting a Vulnerability

If you discover a security vulnerability within gitbrief, please send an email to akshatchoksi8@gmail.com.

All security vulnerabilities will be promptly addressed.

### What to Include

Please include the following information:

- Type of vulnerability
- Full path of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

---

## Security Best Practices

### Local-First Design

gitbrief is designed as a **local-only** tool:
- No data is sent to external servers (except to local Ollama instance)
- All Git data stays on your machine
- No cloud dependencies

### Ollama Connection

When using AI features:
- Connects only to `localhost:11434` (local Ollama instance)
- No external API calls
- Your commit data never leaves your machine

### Git Access

- Read-only access to Git repositories
- Does not modify any repository data
- Only extracts commit metadata

---

## Security Update Process

1. Vulnerability reported
2. Maintainer confirms and triages
3. Fix developed and tested
4. New release published
5. Security advisory published

---

## Third-Party Dependencies

gitbrief uses the following dependencies:

| Package | Purpose |
|---------|---------|
| typer | CLI framework |
| rich | Terminal formatting |
| GitPython | Git access |
| requests | HTTP client |

Please ensure you keep these dependencies up to date.

---

*Last updated: 2026-04-08*
