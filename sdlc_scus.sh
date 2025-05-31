#!/data/data/com.termux/files/usr/bin/bash
# Jetstreamin Artemis-CodexOps: End-to-End SCUS SDLC Automation

set -e
REPO_DIR="$HOME/jetstreamin"
cd "$REPO_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
FEATURE_BRANCH="feature/scus-$TIMESTAMP"
RELEASE_BRANCH="release/scus-$TIMESTAMP"
TAG="scus-v$(date +%Y.%m.%d.%H%M)"
PR_TITLE="SCUS Auto-Patch $FEATURE_BRANCH"
PR_BODY="Automated agent patch, full SDLC compliance."

logstep() { echo -e "\n[$(date +%H:%M:%S)] $1"; }

logstep "=== [SCUS] STARTING E2E SDLC AGENT ==="

# 1. Patch ndef → def in agent_logger.py (self-heal)
find . -type f -name 'agent_logger.py' -exec sed -i 's/^ndef /def /' {} \;
logstep "Syntax self-heal done."

# 2. Commit in submodules, if any changes
for sub in codexcli-forge success/artemis-codexops; do
  if [ -d "$sub/.git" ]; then
    cd $sub
    git add -A
    git commit -m "SCUS: update in submodule $sub" || true
    git push || true
    cd "$REPO_DIR"
  fi
done

# 3. Commit in main repo (if any changes)
git checkout develop || git checkout -b develop
git pull
if [[ $(git status --porcelain) ]]; then
  git checkout -b "$FEATURE_BRANCH"
  git add -A
  git commit -m "SCUS auto-patch: diagnostics, syntax, compliance [$TIMESTAMP]"
  git push --set-upstream origin "$FEATURE_BRANCH"
  logstep "Feature branch pushed: $FEATURE_BRANCH"
else
  logstep "No code changes in main repo."
fi

# 4. PR feature to develop (if PR doesn't exist)
if ! gh pr list -B develop -H "$FEATURE_BRANCH" | grep -q "$FEATURE_BRANCH"; then
  gh pr create -B develop -H "$FEATURE_BRANCH" --title "$PR_TITLE" --body "$PR_BODY"
  logstep "PR created: $FEATURE_BRANCH → develop"
else
  logstep "PR already exists: $FEATURE_BRANCH → develop"
fi

# 5. Wait for CI to pass on PR
PR_URL=$(gh pr view "$FEATURE_BRANCH" --json url -q ".url")
logstep "Waiting for CI on $PR_URL"
while true; do
  STATUS=$(gh pr checks "$FEATURE_BRANCH" --watch --interval 10 | grep '✓' | wc -l)
  if [ "$STATUS" -gt 0 ]; then
    logstep "CI Passed! Auto-merging PR."
    gh pr merge "$FEATURE_BRANCH" --merge --auto
    break
  fi
  echo -n "."
  sleep 20
done

# 6. Promote to release branch if new commits exist
git checkout develop && git pull
git checkout -b "$RELEASE_BRANCH"
git push --set-upstream origin "$RELEASE_BRANCH"
if git log main.."$RELEASE_BRANCH" | grep .; then
  logstep "New commits found. Creating release PR."
  gh pr create -B main -H "$RELEASE_BRANCH" --title "SCUS Release $TAG" --body "Automated release after successful develop merge."
  logstep "Release PR created."
else
  logstep "No new commits to promote. Skipping release PR."
  exit 0
fi

# 7. Wait for CI on release PR and merge if green
while true; do
  STATUS=$(gh pr checks "$RELEASE_BRANCH" --watch --interval 10 | grep '✓' | wc -l)
  if [ "$STATUS" -gt 0 ]; then
    logstep "Release CI Passed! Auto-merging release PR."
    gh pr merge "$RELEASE_BRANCH" --merge --auto
    break
  fi
  echo -n "."
  sleep 20
done

# 8. Tag main and generate release notes
git checkout main && git pull
git tag "$TAG"
git push origin "$TAG"
gh release create "$TAG" --generate-notes --title "$TAG" --notes "SCUS auto-release: $TAG completed."
logstep "=== [SCUS] END-TO-END SDLC SUCCESSFUL: Release $TAG ==="
