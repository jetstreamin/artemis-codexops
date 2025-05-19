# Contributing to Artemis CodexOps

## How to Contribute
- **Fork, branch, develop, and submit PRs.**
- **Build modular agents and payloads (SCUS where possible).**
- **Validate:** Use `python cli/self_test.py` before opening a PR.
- **Security:** Never commit secrets/tokens; pre-commit hook blocks leaks.
- **Quality:** Use `cli/codex_ai_review.sh` (if openai-cli installed) for code review.

## MVP Checklist
- [ ] All agents must pass self-test.
- [ ] All new features must have log/status output.
- [ ] All docs/README must be up to date.
- [ ] New agent: update dashboard and help CLI.

## Community
- **Questions/feedback?** Use [issues](https://github.com/jetstreamin/artemis-codexops/issues).
- **Get involved:** [How to contribute](https://github.com/jetstreamin/artemis-codexops/blob/main/CONTRIBUTING.md)
