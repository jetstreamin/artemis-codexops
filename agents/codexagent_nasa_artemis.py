import os
os.makedirs("logs", exist_ok=True)
#!/usr/bin/env python3
"""
CodexAgent NASA Artemis Status Fetcher
- Fetches Artemis mission status from NASA API (or returns mock data if offline/keyless).
- Logs run status to logs/agent_status.json and logs/agent.log
"""
import os, sys, requests, json
from agent_logger import log_status

NASA_API = os.getenv("NASA_API_URL", "https://llapi.thespacedevs.com/2.2.0/launch/upcoming/?search=artemis")
TIMEOUT = 8

def fetch_status():
    try:
        r = requests.get(NASA_API, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        artemis = [x for x in data.get("results", []) if "artemis" in x.get("name", "").lower()]
        msg = "Artemis mission data fetched" if artemis else "No Artemis missions found"
        log_status("codexagent_nasa_artemis", msg, {"found": len(artemis)})
        return {"status": msg, "missions": artemis}
    except Exception as e:
        log_status("codexagent_nasa_artemis", "offline/mock", {"error": str(e)})
        return {
            "status": "offline/mock",
            "missions": [{"name": "Artemis I", "status": "Launched"}, {"name": "Artemis II", "status": "Scheduled"}],
            "error": str(e)
        }

if __name__ == "__main__":
    print(json.dumps(fetch_status(), indent=2))
