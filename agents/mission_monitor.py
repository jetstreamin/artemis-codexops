
def agent_self_post(name, status="online", version="1.0", endpoint="http://localhost:8080/api/agent_post"):
    data = {
        "agent_name": name,
        "status": status,
        "version": version,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "timestamp": time.time()
    }
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")


#!/usr/bin/env python3
"""
Mission/workflow monitor for Artemis CodexOps.
- Periodically checks mission status, agent health, and triggers webhooks/alerts.
- Outputs to web dashboard and logs.
"""
import time, os, requests, json
INTERVAL = 15 # seconds
while True:
    try:
        r = requests.get('http://localhost:8080/api/artemis', timeout=5)
        data = r.json()
        print("MISSION STATUS:", json.dumps(data, indent=2))
        # Optional: trigger webhook if certain event detected
        if os.getenv('WEBHOOK_ON') == "1":
            requests.post(os.getenv('WEBHOOK_URL',''), json=data)
        with open("logs/mission_monitor.log","a") as f: f.write(json.dumps(data)+"\n")
    except Exception as e:
        print("Monitor error:", e)
    if os.getenv('DEBUG_MONITOR') == "1":
        print("Debug mode: sleeping", INTERVAL, "sec")
    time.sleep(INTERVAL)
