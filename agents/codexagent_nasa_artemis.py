#!/usr/bin/env python3
"""
CodexAgent NASA Artemis Status Fetcher
- Fetches Artemis mission status from NASA API (or returns mock data if offline/keyless).
- Usage: python agents/codexagent_nasa_artemis.py
"""

import os, sys, requests, json

NASA_API = os.getenv("NASA_API_URL", "https://llapi.thespacedevs.com/2.2.0/launch/upcoming/?search=artemis")
TIMEOUT = 8

def fetch_status():
    try:
        r = requests.get(NASA_API, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        artemis = [x for x in data.get("results", []) if "artemis" in x.get("name", "").lower()]
        if not artemis:
            return {"status": "No Artemis missions found", "missions": []}
        return {"status": "Artemis mission data fetched", "missions": artemis}
    except Exception as e:
        return {
            "status": "offline/mock",
            "missions": [{"name": "Artemis I", "status": "Launched"}, {"name": "Artemis II", "status": "Scheduled"}],
            "error": str(e)
        }

if __name__ == "__main__":
    print(json.dumps(fetch_status(), indent=2))
