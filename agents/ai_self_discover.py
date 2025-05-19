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
        subprocess.run(["python", agent["path"]])
        log_action("run_agent", agent["name"])

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
