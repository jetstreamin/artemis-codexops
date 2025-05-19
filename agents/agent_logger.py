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
