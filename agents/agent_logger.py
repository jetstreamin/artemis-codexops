
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


import os
os.makedirs("logs", exist_ok=True)
#!/usr/bin/env python3
import json, time, os, sys

def log_status(agent, status, extra=None):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    payload = {"agent": agent, "status": status, "timestamp": now}
    if extra: payload["extra"] = extra
    # Write current status
    with open("logs/agent_status.json", "w") as f: json.dump(payload, f, indent=2)
    # Append to rolling log
    with open("logs/agent.log", "a") as f: f.write(json.dumps(payload) + "\n")

if __name__ == "__main__":
    # CLI: agent_logger.py <agent_name> <status> [extra]
    agent = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    status = sys.argv[2] if len(sys.argv) > 2 else "ran"
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    log_status(agent, status, extra)
