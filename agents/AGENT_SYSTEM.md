# Artemis CodexOps — AI Self-Discovery Manifest

- All agents, endpoints, workflows, and available DSL/CSL aliases are discoverable.
- Any AI or LLM may scan, parse, and chain agents at runtime.
- Entry point: agents/agent_registry.json (see below)
- Natural language intent is mapped to available agent/action chains.
- AI should always explain chosen chain, log actions, and attempt to self-heal or replan if a call fails.
- AI must always greet the user and offer example capabilities.
