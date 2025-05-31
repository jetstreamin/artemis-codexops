#!/usr/bin/env python3
import os, json, openai
from datetime import datetime
from pathlib import Path
Path("logs").mkdir(exist_ok=True)
def load_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY not set.")
    openai.api_key = key

def log(prompt, reply, logfile):
    with open(logfile, "a") as f:
        f.write(json.dumps({
            "ts": datetime.utcnow().isoformat() + "Z",
            "prompt": prompt,
            "reply": reply
        }) + "\n")

def run(prompt=None):
    load_key()
    logfile = Path("logs") / f"session-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.log"
    if prompt:
        res = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = res.choices[0].message.content.strip()
        log(prompt, reply, logfile)
        return reply

    print("Paris Agent: Type 'exit' to quit.")
    while True:
        try:
            prompt = input("> ").strip()
            if prompt.lower() in ("exit", "quit"): break
            res = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = res.choices[0].message.content.strip()
            print(reply)
            log(prompt, reply, logfile)
        except Exception as e:
            print(f"[error] {e}")

if __name__ == "__main__":
    run()
