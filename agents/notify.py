import requests, socket, os, time
ndef agent_self_post(name, status="online", version="1.0", endpoint="http://localhost:8080/api/agent_post"):
    data = {"agent_name": name, "status": status, "version": version, "host": socket.gethostname(), "pid": os.getpid(), "timestamp": time.time()}
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")


#!/usr/bin/env python3
import sys, subprocess

msg = sys.argv[1] if len(sys.argv) > 1 else "Artemis CodexOps: Agent event."
try:
    # Try Termux notification
    subprocess.run(['termux-notification', '--content', msg], check=True)
except Exception:
    try:
        # Fallback: notify-send (Linux desktop)
        subprocess.run(['notify-send', msg], check=True)
    except Exception:
        print(msg)
