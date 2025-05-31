#!/data/data/com.termux/files/usr/bin/bash
while true; do
  date >> bulletproof.log
  bash full-auto.sh >> bulletproof.log 2>&1
  sleep 180
done
