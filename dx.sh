# File: dx (make it executable: chmod +x dx)
#!/data/data/com.termux/files/usr/bin/bash
# Artemis DevOps Diagnostics (dx)

echo "==== Artemis CodexOps Self-Diagnosis ===="

# 1. Git Status and Last Commit
echo -e "\n--- GIT STATUS ---"
git status
echo -e "\n--- LAST COMMIT ---"
git log -1 --oneline

# 2. Most Recent Health or Magic Loop Output
if [ -f cli/magic_loop_full.sh ]; then
  echo -e "\n--- MAGIC LOOP (Health Check) ---"
  ./cli/magic_loop_full.sh | tail -20
fi

# 3. Error and Blocker Logs
for f in health_check.log milestone_health.log CRITICAL_BLOCKER.log; do
  [ -f "$f" ] && { echo -e "\n--- $f ---"; tail -20 "$f"; }
done

# 4. Environment Variables (selected, safe subset)
echo -e "\n--- ENVIRONMENT ---"
env | grep -E 'PROJECT_ROOT|PYTHON|TERMUX|PATH|VIRTUAL_ENV'

# 5. Active Plugins, Agent Registry, and Versions
echo -e "\n--- AGENT REGISTRY (short) ---"
jq '.[] | {name, path}' agents/agent_registry.json 2>/dev/null | head -10

echo -e "\n--- PLUGINS DIRECTORY ---"
[ -d plugins ] && ls -l plugins || echo "No plugins dir."

echo -e "\n--- PYTHON VERSION ---"
python --version

echo -e "\n--- PIP FREEZE ---"
pip freeze | grep -E 'openai|requests|termux|coder|vscode' || echo "(Common packages not found)"

echo -e "\n--- DEVICE INFO (Termux) ---"
uname -a

echo -e "\n==== End of DX Diagnosis ===="

# Optional: Copy last 100 lines to clipboard for AI support
tail -100 health_check.log 2>/dev/null | termux-clipboard-set
echo "(Last 100 lines of health_check.log copied to clipboard, if available)"
