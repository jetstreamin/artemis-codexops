#!/usr/bin/env python3
"""
Agent Logger for Artemis CodexOps

Provides functions to post agent status to a central endpoint and log agent status locally.
"""

import os
import sys
import json
import time
import socket
import requests
import logging
from typing import Optional

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/agent_logger.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def agent_self_post(
    name: str,
    status: str = "online",
    version: str = "1.0",
    endpoint: str = "http://localhost:8080/api/agent_post"
) -> None:
    """
    Post agent status to a central endpoint.

    Args:
        name: Name of the agent.
        status: Current status of the agent.
        version: Agent version.
        endpoint: Endpoint to post status to.
    """
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
        logging.info(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        logging.error(f"[SELF-POST] Failed to post agent status: {e}")

def log_status(agent: str, status: str, extra: Optional[str] = None) -> None:
    """
    Log agent status to local files.

    Args:
        agent: Name of the agent.
        status: Status message.
        extra: Optional extra information.
    """
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    payload = {"agent": agent, "status": status, "timestamp": now}
    if extra:
        payload["extra"] = extra
    # Write current status
    with open("logs/agent_status.json", "w") as f:
        json.dump(payload, f, indent=2)
    # Append to rolling log
    with open("logs/agent.log", "a") as f:
        f.write(json.dumps(payload) + "\n")
    logging.info(f"Logged status for agent '{agent}': {status}")

if __name__ == "__main__":
    # CLI: agent_logger.py <agent_name> <status> [extra]
    agent = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    status = sys.argv[2] if len(sys.argv) > 2 else "ran"
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    log_status(agent, status, extra)
