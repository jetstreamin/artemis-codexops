#!/usr/bin/env python3
import subprocess, sys, os

def test_agent(agent_path):
    print(f"Testing {agent_path}...", end=" ")
    try:
        out = subprocess.check_output(['python', agent_path], timeout=15)
        print("OK")
        return True
    except Exception as e:
        print("FAIL", e)
        return False

def main():
    agents = [f for f in os.listdir('agents') if f.endswith('.py') and f != 'agent_logger.py']
    results = {a: test_agent('agents/' + a) for a in agents}
    passed = sum(results.values())
    print(f"\n{passed}/{len(agents)} agents passed.")
    exit(0 if passed == len(agents) else 1)

if __name__ == "__main__":
    main()
