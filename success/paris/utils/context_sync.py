import os, json, requests

GIST_API = "https://api.github.com/gists"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def save_context(filename, data):
    payload = {
        "files": {filename: {"content": json.dumps(data, indent=2)}},
        "public": False,
        "description": "paris-agent context"
    }
    r = requests.post(GIST_API, headers=HEADERS, json=payload)
    return r.json().get("id")

def load_context(gist_id, filename):
    r = requests.get(f"{GIST_API}/{gist_id}", headers=HEADERS)
    raw = r.json()["files"][filename]["content"]
    return json.loads(raw)
