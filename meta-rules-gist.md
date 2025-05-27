# Artemis CodexOps — Universal Meta-Rules & Coding Standards

**Use this as the canonical reference for any project, LLM, or developer.**

---

## 1. **Meta-Rules (Universal)**
- All code must be modular, self-healing, and auto-validating.
- Every feature must be testable locally and in CI/CD, with both headless and visual (headed) UI tests.
- All deployments must be fully automated, hands-free, and repeatable (one-command or watcher-based).
- All endpoints, UIs, and services must be validated after deploy, with health checks and screenshots.
- All failures must trigger auto-fix, auto-retry, or clear notification with logs.
- No manual steps should be required after initial setup—everything must be “set and forget.”
- All code, infra, and automation must be documented in the repo for team and LLM use.

---

## 2. **Security & Compliance**
- Never commit secrets, tokens, or credentials to the repo.
- Use environment variables, AWS Secrets Manager, or Parameter Store for all secrets.
- All endpoints must validate and sanitize input.
- Use RBAC and least-privilege IAM for all cloud resources.
- All logs must be privacy-safe and auditable.

---

## 3. **Automation & DevOps**
- Use modular CloudFormation/CDK for all AWS infra.
- Use a root infra stack for shared resources (VPC, RDS, S3, ALB, IAM).
- Use a per-service stack for each microservice (ECS Fargate, env vars, scaling).
- Use a Makefile, PowerShell, or Bash script for one-command deploy, test, and validate.
- Use a watcher script (PowerShell or nodemon) for local auto-test and visual validation.
- Use GitHub Actions (or equivalent) for CI/CD, with full test, build, deploy, and health check steps.

---

## 4. **Testing & Validation**
- All code must have automated tests: unit, integration, UI (Playwright/Selenium), and TUI/CLI.
- UI tests must run in both headless and headed (visual) mode.
- All test results, screenshots, and logs must be published as artifacts.
- All endpoints must be health-checked after deploy.
- All failures must be auto-fixed or clearly reported.

---

## 5. **UI/UX & Visual Feedback**
- All UI screens must be visually validated in local and CI runs.
- Use Playwright or Selenium in headed mode for local visual feedback.
- Provide a watcher or daemon to auto-run tests and show UI on every code change.
- All errors must be logged and auto-fixed if possible.

---

## 6. **Documentation & Onboarding**
- README must include a “Quick Start” for one-command deploy and test.
- All scripts and automation must be documented for both local and cloud use.
- All meta-rules must be included in every new project and referenced in LLM prompts.

---

## 7. **Cloud & Local Parity**
- All automation must work both locally (PowerShell/Bash) and in the cloud (GitHub Actions/AWS CodeBuild).
- No step should require manual intervention after initial setup.

---

## 8. **Self-Healing & Monitoring**
- All services must auto-restart and auto-heal on failure (ECS, watcher, etc.).
- All endpoints must be monitored for uptime and health.
- Only notify the user if human intervention is required.

---

## 9. **Extensibility**
- All infra, code, and automation must be modular and reusable for new services.
- All new features must follow these meta-rules by default.

---

_Last updated: 2025-05-26_
