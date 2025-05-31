#!/data/data/com.termux/files/usr/bin/bash

AGENT=~/jetstreamin/auto-devop.sh
LOG=~/jetstreamin/run.log
PIDFILE=~/jetstreamin/run.pid
ROADMAP=~/jetstreamin/TODO_NEXT.md
LOCK=~/jetstreamin/locks/jetstreamin.lock

touch $LOG

BOLD='\033[1m'
RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[0;33m'
CYN='\033[0;36m'
NC='\033[0m'

#fancy_banner() {
#  clear
#  echo -e "${CYN}"
#  echo -e "╔═════════════════════════════════════════════════════════════╗"
#  echo -e "║     ${BOLD}JETSTREAMIN AGENT SUPERVISOR - PRO MODE - $(date +%T)${NC}${CYN}    ║"
#  echo -e "╚═════════════════════════════════════════════════════════════╝${NC}"
#}

fancy_banner() {
  clear
  echo -e "${CYN}"
  printf '+%0.s=' $(seq 1 58); echo '+'
  printf "|${BOLD} %-53s ${NC}${CYN}|\n" "JETSTREAMIN AGENT SUPERVISOR - PRO MODE - $(date +%H:%M:%S)"
  printf '+%0.s=' $(seq 1 58); echo "+${NC}"
}

fancy_status() {
  status_agent
  echo -e "${YEL}Recent Activity:${NC}"
  # Patch: sed only runs if we have non-empty log; no \1 error possible
  if [ -s "$LOG" ]; then
    tail -n 12 $LOG 2>/dev/null | sed -E "s/(ERROR|FAIL)/${RED}\1${NC}/g"
  else
    echo "No agent activity yet."
  fi
  echo ""
}

run_agent() {
  fancy_banner
  echo -e "${GRN}[INFO] Starting agent...${NC}"
  nohup bash $AGENT >> $LOG 2>&1 &
  echo $! > $PIDFILE
  command -v termux-notification >/dev/null && termux-notification --title "Jetstreamin Agent" --content "Agent started (PID $(cat $PIDFILE))" --priority high 2>/dev/null || true
  command -v termux-vibrate >/dev/null && termux-vibrate -d 100 || true
}

stop_agent() {
  if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    kill $PID && echo -e "${RED}[INFO] Agent stopped (PID $PID)${NC}"
    command -v termux-notification >/dev/null && termux-notification --title "Jetstreamin Agent" --content "Agent stopped" 2>/dev/null || true
    rm -f $PIDFILE
  else
    echo -e "${YEL}[WARN] No agent running.${NC}"
  fi
}

status_agent() {
  if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    if ps -p $PID > /dev/null; then
      echo -e "${GRN}✔ Agent running (PID $PID)${NC}"
    else
      echo -e "${RED}✖ Agent dead but PID file present.${NC}"
    fi
  else
    echo -e "${YEL}✖ Agent not running.${NC}"
  fi
}

restart_agent() {
  stop_agent
  sleep 1
  run_agent
}

pause_agent() {
  if [ -f $PIDFILE ]; then
    kill -STOP $(cat $PIDFILE)
    echo -e "${YEL}[INFO] Agent paused.${NC}"
    command -v termux-notification >/dev/null && termux-notification --title "Jetstreamin Agent" --content "Agent paused" 2>/dev/null || true
  fi
}

resume_agent() {
  if [ -f $PIDFILE ]; then
    kill -CONT $(cat $PIDFILE)
    echo -e "${GRN}[INFO] Agent resumed.${NC}"
    command -v termux-notification >/dev/null && termux-notification --title "Jetstreamin Agent" --content "Agent resumed" 2>/dev/null || true
    command -v termux-vibrate >/dev/null && termux-vibrate -d 80 || true
  fi
}

watch_agent() {
  tail -f $LOG
}

auto_heal() {
  fancy_banner
  echo -e "${GRN}[AUTO-HEAL] Supervisor mode started.${NC}"
  while true; do
    curl -sfL https://raw.githubusercontent.com/jetstreamin/artemis-codexops/main/auto-devop.sh -o $AGENT && chmod +x $AGENT
    run_agent
    PID=$(cat $PIDFILE)
    sleep 5
    wait $PID || {
      echo -e "${RED}[ERROR] Agent crashed. Restarting...${NC}"
      command -v termux-notification >/dev/null && termux-notification --title "Jetstreamin Agent" --content "Agent crashed. Restarting..." --priority max 2>/dev/null || true
    }
    sleep 2
    fancy_status
    sleep 3
  done
}

case "$1" in
  start)   run_agent ;;
  stop)    stop_agent ;;
  restart) restart_agent ;;
  pause)   pause_agent ;;
  resume)  resume_agent ;;
  status)  fancy_status ;;
  watch)   watch_agent ;;
  auto)    auto_heal ;;
  *)
    fancy_banner
    echo -e "${BOLD}Usage:${NC} $0 {start|stop|restart|pause|resume|status|watch|auto}"
    echo ""
    fancy_status
    ;;
esac
