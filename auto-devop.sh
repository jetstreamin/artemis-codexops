#!/data/data/com.termux/files/usr/bin/bash
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
