import requests, socket, os, time
ndef agent_self_post(name, status="online", version="1.0", endpoint="http://localhost:8080/api/agent_post"):
    data = {"agent_name": name, "status": status, "version": version, "host": socket.gethostname(), "pid": os.getpid(), "timestamp": time.time()}
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")


#!/usr/bin/env python3
"""
Universal AI Self-Discovery/Chaining for Artemis CodexOps
- Scans registry, presents available agents and chains
- Accepts a natural language goal, explains the chosen agent flow, and runs it
- Greets user on enable, logs all actions
"""
import json, os, subprocess

REGISTRY = "agents/agent_registry.json"
LOG = "logs/ai_self_discover.log"

def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)

def greet():
    msg = "Hello, I am Artemis. Ready to scan and run agents for you!"
    print(msg)
    log_action("greet", msg)

def log_action(event, details):
    with open(LOG, "a") as f:
        f.write(json.dumps({"event": event, "details": details}) + "\n")

def explain_chain(chain):
    print("To fulfill your request, I will chain:")
    for agent in chain:
        print(f" - {agent['name']}: {agent['description']}")

def run_chain(chain):
    for agent in chain:
        print(f"Running {agent['name']}...")
        healed = False
        for _ in range(2):  # try twice: original and after healing
            result = subprocess.run(
                ["python", agent["path"]],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(result.stdout)
                log_action("run_agent", agent["name"])
                break
            err = result.stderr
            # Self-heal missing module
            for error_prefix in ["ModuleNotFoundError: No module named", "ImportError: No module named"]:
                if error_prefix in err:
                    missing = err.split(error_prefix)[-1].split("'")[1]
                    print(f"Auto-heal: pip install {missing}")
                    log_action("auto_heal_install", missing)
                    subprocess.run(["pip", "install", missing])
                    healed = True
                    break
            else:
                print(result.stdout)
                print(err)
                log_action("agent_failed", {"agent": agent["name"], "stderr": err})
                break
            if not healed:
                break


def match_goal(goal, agents):
    # Naive NL matching for demo—expand as needed
    matches = []
    for agent in agents:
        if any(w in agent["description"].lower() for w in goal.lower().split()):
            matches.append(agent)
    if not matches:
        matches = agents[:1]  # fallback: first agent
    return matches

if __name__ == "__main__":
    greet()
    agents = load_registry()
    print("Available agents:")
    for a in agents:
        print(f"- {a['name']}: {a['description']}")
    goal = input("What do you want to do? (natural language) ")
    chain = match_goal(goal, agents)
    explain_chain(chain)
    run_chain(chain)
    print("Done. All actions logged.")
