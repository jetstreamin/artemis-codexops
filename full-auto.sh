#!/data/data/com.termux/files/usr/bin/bash
cd ~
[ -d jetstreamin ] || git clone https://github.com/jetstreamin/artemis-codexops.git jetstreamin
cd jetstreamin
mkdir -p locks diagnostics .github/workflows agents success
touch locks/jetstreamin.lock
curl -sfL https://raw.githubusercontent.com/jetstreamin/artemis-codexops/main/auto-devop.sh -o auto-devop.sh
chmod +x auto-devop.sh
find . -type f -name '*.py' -exec sed -i 's/^ndef /def /' {} \; || true
export GH_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"
git fetch origin
git checkout develop || git checkout -b develop
git pull || true
TS=$(date +%Y%m%d-%H%M%S)
BR="feature/full-auto-$TS"
git checkout -b "$BR" || git checkout "$BR"
git add -A
git commit -m "FULL AUTO: Add/commit everything for SCUS [$TS]" || true
git push --set-upstream origin "$BR" || true
gh pr create -B develop -H "$BR" --title "FULL AUTO PR $BR" --body "Agent full-auto, all agents, configs, expansions committed." || true
nohup bash auto-devop.sh --full-auto > auto-devop.log 2>&1 &
