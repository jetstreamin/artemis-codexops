#!/data/data/com.termux/files/usr/bin/bash

cd ~/jetstreamin

# 1. Ensure ALL .log files are ignored (main repo)
echo "*.log" >> .gitignore

# 2. Untrack all log files in main repo (no errors, no matter what)
for logfile in *.log; do
  [ -f "$logfile" ] && git check-ignore "$logfile" >/dev/null 2>&1 && git rm --cached "$logfile" 2>/dev/null || true
done

# 3. Heal all submodules, recursively
find . -type d -name .git -exec sh -c '
  cd "$(dirname "{}")"
  echo "*.log" >> .gitignore
  for logfile in *.log; do
    [ -f "$logfile" ] && git check-ignore "$logfile" >/dev/null 2>&1 && git rm --cached "$logfile" 2>/dev/null || true
  done
  git add .gitignore
  git commit -m "Self-heal: untrack log files (submodule)" || true
' \;

# 4. Finalize and push
git add .gitignore
git commit -m "Self-heal: untrack log files everywhere" || true
git push || true


cd ~/jetstreamin || exit 1
LOG=~/jetstreamin/auto-devop.log
echo "[`date`] [AUTO-DEVOP] CYCLE START" >> $LOG
[ -x ./dx.sh ] && bash ./dx.sh >> $LOG 2>&1
git add -A
TS=$(date +%Y%m%d-%H%M%S)
git commit -m "AUTO-DEVOP: Full cycle [$TS]" || true
git push || true
git fetch origin
git checkout main || git checkout -b main
git pull || true
git merge develop || git merge $(git branch --sort=-committerdate | grep feature/ | head -n1) || true
git push origin main || true
echo "[`date`] [AUTO-DEVOP] CYCLE END" >> $LOG
