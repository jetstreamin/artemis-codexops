cd ~
[ -d jetstreamin ] || git clone https://github.com/jetstreamin/artemis-codexops.git jetstreamin
cd jetstreamin
mkdir -p locks diagnostics .github/workflows agents success
touch locks/jetstreamin.lock

# Download/refresh the auto-devop agent every time (always latest)
curl -sfL https://raw.githubusercontent.com/jetstreamin/artemis-codexops/main/auto-devop.sh -o auto-devop.sh
chmod +x auto-devop.sh

# Patch all 'ndef' bugs and sync files
find . -type f -name '*.py' -exec sed -i 's/^ndef /def /' {} \; || true

# Ensure you have GH CLI authenticated!
export GH_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"

# Force fresh branch for every cycle
git fetch origin
git checkout develop || git checkout -b develop
git pull || true
TS=$(date +%Y%m%d-%H%M%S)
BR="feature/full-auto-$TS"
git checkout -b "$BR" || git checkout "$BR"
git add -A
git commit -m "FULL AUTO: Add/commit everything for SCUS [$TS]" || true
git push --set-upstream origin "$BR" || true

# Create PR (ignore if already exists)
gh pr create -B develop -H "$BR" --title "FULL AUTO PR $BR" --body "Agent full-auto, all agents, configs, expansions committed." || true

# LAUNCH FULL AUTO AGENT
nohup bash auto-devop.sh --full-auto > auto-devop.log 2>&1 &

echo "=== FULL AUTO DEVOP AGENT LAUNCHED ==="
