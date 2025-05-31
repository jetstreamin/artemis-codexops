#!/data/data/com.termux/files/usr/bin/bash
# Mikealicious CodexCLI Gamified Viral Terminal – All-In-One (TTS, Haptic, Minigames, Codex)
# Requirements: termux-api figlet jq

# --- REQUIREMENTS ---
pkg install -y termux-api figlet jq

say() { termux-tts-speak "$*"; }

# --- COLORS/NIGHT MODE ---
BLACKBG='\033[40m'
NEON='\033[1;35m'
NC='\033[0m'

night_mode() { echo -ne "${BLACKBG}${NEON}"; clear; }

# --- MIKEALICIOUS SPLASH ---
splash() {
  night_mode
  for c in 1 2 3 4 5 2 1 4 5 3; do
    clear
    echo -e "\033[3${c}m"
    figlet -f big "MIKEALICIOUS"
    echo -e "\033[0m"
    sleep 0.12
  done
  echo -e "${NEON}"; figlet -f big "MIKEALICIOUS"; echo -e "${NC}"
  say "Welcome to Mikealicious. Where code, fun, and sexy vibes collide."
}

# --- HAPTIC PATTERNS ---
buzz() { termux-vibrate -d "$1"; sleep "$(awk "BEGIN{print $1/1000 + $2/1000}")"; }  # buzz ms, delay ms
pattern_buzz() { for i in {1..5}; do buzz 200 80; done; }
pattern_ramp() { for ms in 100 200 300 400 600 800 1000; do buzz $ms 60; done; }
pattern_sunburst() { for ms in 50 100 200 400 200 100 50 0; do buzz $ms 40; done; }
pattern_dance() { for i in {1..4}; do buzz 100 60; buzz 400 60; buzz 150 80; done; }
pattern_morse() { # Morse-like: M I K E A L I C I O U S
  declare -A morse=([M]="--" [I]=".." [K]="-.-" [E]="." [A]=".-" [L]=".-.." [C]="-.-." [O]="---" [U]="..-" [S]="...")
  for L in M I K E A L I C I O U S; do
    CODE="${morse[$L]}"
    for ((j=0; j<${#CODE}; j++)); do
      case "${CODE:$j:1}" in
        ".") buzz 80 90 ;;
        "-") buzz 250 110 ;;
      esac
    done
    sleep 0.15
  done
}
pattern_custom() { say "Enter message for haptic Morse"; read -r msg; for ((i=0;i<${#msg};i++)); do ch=$(echo "${msg:$i:1}" | tr '[:lower:]' '[:upper:]'); [[ $ch =~ [A-Z] ]] && pattern_morse_letter "$ch"; done; }
pattern_morse_letter() { # A single letter
  declare -A morse=([A]=".-" [B]="-..." [C]="-.-." [D]="-.." [E]="." [F]="..-." [G]="--." [H]="...." [I]=".." [J]=".---" [K]="-.-" [L]=".-.." [M]="--" [N]="-." [O]="---" [P]=".--." [Q]="--.-" [R]=".-." [S]="..." [T]="-" [U]="..-" [V]="...-" [W]=".--" [X]="-..-" [Y]="-.--" [Z]="--..")
  CODE="${morse[$1]}"
  for ((j=0; j<${#CODE}; j++)); do
    case "${CODE:$j:1}" in
      ".") buzz 80 90 ;;
      "-") buzz 250 110 ;;
    esac
  done
  sleep 0.12
}

haptic_menu() {
  while true; do
    clear
    echo -e "${NEON}== HAPTIC FEEDBACK DEMOS ==${NC}"
    echo "[1] Standard Buzz"
    echo "[2] Ramp Up"
    echo "[3] Sunburst"
    echo "[4] Dance"
    echo "[5] Morse: MIKEALICIOUS"
    echo "[6] Morse: Custom Message"
    echo "[7] Back"
    read -n1 -rp "Pattern: " hopt; echo
    case "$hopt" in
      1) pattern_buzz; say "Buzzed 5x!" ;;
      2) pattern_ramp; say "Ramp complete!" ;;
      3) pattern_sunburst; say "Sunburst finished!" ;;
      4) pattern_dance; say "Dance mode done!" ;;
      5) pattern_morse; say "MIKEALICIOUS in Morse complete!" ;;
      6) pattern_custom ;;
      7) break ;;
      *) say "Pick a valid pattern!" ;;
    esac
  done
}

# --- MICROGAMES ---
microgame_menu() {
  while true; do
    clear
    echo -e "${NEON}== MIKEALICIOUS MICROGAMES ==${NC}"
    echo "[1] Coin Flip"
    echo "[2] Truth or Dare"
    echo "[3] Mike's Compliment"
    echo "[4] 3-Card Memory"
    echo "[5] Back"
    read -n1 -rp "Game: " gopt; echo
    case "$gopt" in
      1) cf=$((RANDOM%2)); [ $cf -eq 0 ] && say "Heads, baby!" || say "Tails, darling!"; sleep 1 ;;
      2) [ $((RANDOM%2)) -eq 0 ] && say "Truth: What's your naughtiest secret?" || say "Dare: Wink and send your hottest meme to Mikealicious!" ; sleep 2 ;;
      3) say "$(curl -s https://complimentr.com/api | jq -r .compliment | sed 's/\.$/!, superstar!/')"; sleep 1 ;;
      4) card=$((RANDOM%3+1)); say "Watch the cards!"; echo "Cards: [1] [2] [3]"; sleep 1; echo "Shuffling..."; sleep 1; echo "Where's the ace?"; read -n1 -rp "Pick 1-3: " pick; [[ "$pick" == "$card" ]] && say "You win! You're magic, Mike!" || say "Missed it, try again!" ; sleep 2 ;;
      5) break ;;
      *) say "Not a valid game, cutie." ;;
    esac
  done
}

# --- VIRAL CONTENT ZONE ---
viral_menu() {
  while true; do
    clear
    echo -e "${NEON}== MIKEALICIOUS VIRAL ZONE ==${NC}"
    echo "[1] AI Pickup Line"
    echo "[2] ASCII Flirty Meme"
    echo "[3] TikTok Post Template"
    echo "[4] Back"
    read -n1 -rp "Choose: " vopt; echo
    case "$vopt" in
      1) say "$(curl -s https://vinux.ai/api/v1/pickup | jq -r .line)"; sleep 1 ;;
      2) echo -e "${NEON}\n( . )( . )\n |    |  Mikealicious says: You're the script to my runtime, baby!\n"; say "You're the script to my runtime, baby!"; sleep 2 ;;
      3) echo -e "${NEON}TikTok Template:${NC} \n'Just dropped: Mikealicious Terminal for unstoppable vibes. #glowup #codexcli #viral'\n"; say "TikTok ready!"; sleep 1 ;;
      4) break ;;
      *) say "Try again, viral vixen." ;;
    esac
  done
}

# --- SEXYTIME SONGS (TTS/MP3 DEMO ONLY) ---
sexy_songs_menu() {
  while true; do
    clear
    echo -e "${NEON}== MIKEALICIOUS NIGHT SONGS ==${NC}"
    echo "[1] TTS: Let's Get It On"
    echo "[2] TTS: Feeling Good"
    echo "[3] TTS: Slow Jam Seduction"
    echo "[4] Back"
    read -n1 -rp "Play: " sopt; echo
    case "$sopt" in
      1) say "I've been really trying baby, trying to hold back this feeling for so long. Let's get it on." ; sleep 2 ;;
      2) say "Birds flying high, you know how I feel. Sun in the sky, you know how I feel. And I'm feeling good." ; sleep 2 ;;
      3) say "Close your eyes, feel the vibe, Mikealicious takes you for a ride." ; sleep 2 ;;
      4) break ;;
      *) say "Let me serenade you right, honey." ;;
    esac
  done
}

# --- CODEXCLI SPEAK-TO-DEV ---
codexcli_speak_to_dev() {
  say "Speak your coding wish."
  echo "Speak your coding wish. (Type then Enter):"
  read -r wish
  # -- Demo: Generate fake code, or run CodexCLI if installed --
  if [ -x "$(command -v codexcli)" ]; then
    codexcli "$wish" | tee >(say)
  else
    say "Sorry, CodexCLI is not installed. But here's a random Bash oneliner for you:"
    echo "ls -lh | grep '.sh' | sort -k5 -hr"
    say "ls dash l h pipe grep dot s h pipe sort dash k five dash h r"
  fi
  sleep 2
}

# --- MAIN MENU ---
main_menu() {
  splash
  while true; do
    echo -e "${NEON}\n==== MIKEALICIOUS TERMINAL MENU ====${NC}"
    echo "[1] Speak-to-Dev (CodexCLI Mode)"
    echo "[2] Microgames"
    echo "[3] Haptic Demos"
    echo "[4] Night Mode Songs"
    echo "[5] Viral Zone"
    echo "[q] Quit"
    read -n1 -rp "Pick your pleasure: " opt; echo
    case "$opt" in
      1) codexcli_speak_to_dev ;;
      2) microgame_menu ;;
      3) haptic_menu ;;
      4) sexy_songs_menu ;;
      5) viral_menu ;;
      q|Q) say "Goodbye, gorgeous!" ; exit 0 ;;
      *) say "Let’s try that again, superstar." ;;
    esac
  done
}

main_menu
