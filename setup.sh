#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
pkg install -y python git
pip install --upgrade pip
pip install requests
[ -d .git ] || git init
chmod +x agents/*.py 2>/dev/null || true
echo "Auto-provision complete: Python, pip, requests, git set up. Agents ready."
