#!/data/data/com.termux/files/usr/bin/bash
# Jetstreamin Diagnostic Script
# Run as: bash jetstreamin-diagnostic.sh

set -e

# === Config ===
ROOT="$HOME/jetstreamin"
REPO="https://github.com/jetstreamin/artemis-codexops"
LOG="$ROOT/diagnostics/$(date +%Y%m%d-%H%M%S)-diag.log"
REQS="$ROOT/requirements.txt"
LOCK="$ROOT/locks/jetstreamin.lock"
DASH="================================================================================"

# Ensure required folders
mkdir -p "$ROOT/diagnostics"
mkdir -p "$ROOT/logs"

center() { COLS=$(tput cols); printf "%*s\n" $(((${#1}+$COLS)/2)) "$1"; }

log() { echo -e "$1" | tee -a "$LOG"; }

header() {
  clear
  echo "$DASH" | tee "$LOG"
  center "JETSTREAMIN DIAGNOSTIC DASHBOARD"
  echo "$DASH" | tee -a "$LOG"
  center "$(date)"
  echo "$DASH" | tee -a "$LOG"
}

splash() {
  log "\n"
  center "🌩️ Jetstreamin Artemis-CodexOps 🌩️"
  center "Self-Check & Diagnostics"
  log "$DASH"
}

# --- Dependency Checks ---
check_pkg() { 
  dpkg -s "$1" &>/dev/null && log "[OK]  $1" || { log "[ERR]  $1 not found"; MISSING_PKGS+=("$1"); }
}

check_py() { 
  python3 -c "import $1" 2>/dev/null && log "[OK]  Python module: $1" || { log "[ERR]  Python: $1"; MISSING_PY+=("$1"); }
}

check_bin() {
  command -v "$1" &>/dev/null && log "[OK]  $1 in PATH" || { log "[ERR]  $1 not in PATH"; MISSING_BINS+=("$1"); }
}

# --- Main Checks ---
main_checks() {
  splash

  log "Checking persistent paths..."
  [[ -d "$ROOT" ]] && log "[OK]  $ROOT exists" || { log "[ERR]  $ROOT missing"; }
  [[ -f "$LOCK" ]] && log "[OK]  Lock file present" || log "[ERR]  Lock file missing"
  [[ -f "$REQS" ]] && log "[OK]  requirements.txt found" || log "[ERR]  requirements.txt missing"

  log "\nChecking API/env keys..."
  [[ -n "$OPENAI_API_KEY" ]] && log "[OK]  OPENAI_API_KEY loaded" || log "[ERR]  OPENAI_API_KEY missing"
  [[ -n "$GITHUB_TOKEN" ]] && log "[OK]  GITHUB_TOKEN loaded" || log "[WARN]  GITHUB_TOKEN missing"

  log "\nChecking agent repo sync..."
  cd "$ROOT" && git status &>/dev/null && \
    log "[OK]  Git repo present" && git remote -v | tee -a "$LOG" && git fetch && git status | tee -a "$LOG" \
    || log "[ERR]  Git repo not present in $ROOT"

  log "\nChecking system packages..."
  MISSING_PKGS=()
  for pkg in git curl termux-api python3 jq ffmpeg sox openssl; do check_pkg "$pkg"; done

  log "\nChecking required Python modules..."
  MISSING_PY=()
  for py in requests openai termcolor; do check_py "$py"; done

  log "\nChecking required binaries..."
  MISSING_BINS=()
  for bin in git curl jq ffmpeg sox python3 openssl; do check_bin "$bin"; done

  log "\nChecking permissions..."
  [[ -w "$ROOT" ]] && log "[OK]  Write access to $ROOT" || log "[ERR]  Cannot write to $ROOT"
}

# --- Repair Suggestions ---
auto_fix() {
  if (( ${#MISSING_PKGS[@]} )); then
    log "\nAuto-fixing missing packages: ${MISSING_PKGS[*]}"
    pkg install -y "${MISSING_PKGS[@]}"
  fi
  if (( ${#MISSING_PY[@]} )); then
    log "\nAuto-fixing missing Python modules: ${MISSING_PY[*]}"
    pip install "${MISSING_PY[@]}"
  fi
  if (( ${#MISSING_BINS[@]} )); then
    log "\nMissing binaries: ${MISSING_BINS[*]} (manual fix may be needed)"
  fi
}

# --- Run Diagnostic ---
header
main_checks
auto_fix

log "\n$DASH"
center "Diagnostic Complete"
log "$DASH"
log "See $LOG for full details."
