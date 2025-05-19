# Artemis CodexOps

Open, automation-ready, AI-augmented toolkit supporting NASA Artemis missions.

**Roadmap:**
1. CodexAgent for Artemis mission data
2. Unity/VR lunar simulation
3. Real-time open APIs + automation
4. STEM/Outreach tools
5. Contributor-friendly, CI-ready, public by design

_“Built for NASA & explorers, by Jetstreamin.”_

## 🚀 Public Demo & Enterprise/Federal-Ready

- **Live demo:** Deploy instantly to Fly.io, Heroku, or any open cloud for real-time value and collaboration.
- **Portable:** Dockerfile and AWS CloudFormation template included for production/FedRAMP/enterprise use.
- **Compliance:** See COMPLIANCE_CHECKLIST.md for requirements and current status.
- **Contact:** For onboarding or regulated deployments, [open an issue or email yourteam@yourdomain.com](mailto:yourteam@yourdomain.com).


## Option: Auto-load MCP tools
- Place any MCP tools/scripts in cli/mcp_tools/. Agents will auto-import if present.

## Voice & Conversation
- Run `python agents/voice_agent.py` for natural language conversation and agent control (requires mic).
- Optionally extend with Whisper (for transcription) or GPT for AI responses.

## VR/AR/Creative Mode
- Open the Unity VR project in vr/unity/. Build scenes, drag ArtemisAPI.cs onto 3D UI, create your own worlds!
- Everything in VR can be driven by API/agent commands or voice (see above).
- Encourage experimentation: “Describe what you want and have the agents/VR respond!”

## Mission Monitor
- Run `python agents/mission_monitor.py` to monitor and log agent status, trigger webhooks, or debug.

## Webhooks/Debug
- Use dashboard buttons to enable/disable debug output and webhook mode.
- Set `WEBHOOK_URL` env var for outgoing events.

## Optionability & Fun
- Every feature has an on/off toggle. Everything can be mixed: CLI, voice, VR, web, mobile.
- Designed so ANYONE can create, remix, and play.


## Vision Agents (Camera & Scene)

- **Capture with device camera:** `python agents/vision_agent.py`
- **Capture Unity VR scene:** Add VisionCapture.cs to any camera, press [C] in Play mode to save screenshot.
- **Access vision images in dashboard:** Use the Vision section (or /api/vision).
- **Use for AI/automation:** Process, share, or use captured images as agent context for creative, AR, or workflow triggers.


## Local-Only Auth for Testing
- Uses SQLite and FastAPI-Users. No cloud DB or paid infra. Not for prod use.

## Local-Only Auth for Testing
- Uses SQLite and FastAPI-Users. No cloud DB or paid infra. Not for prod use.

## Cloud Cost Monitor
- Run: python agents/cost_monitor.py
- Alerts if any AWS RDS/EC2 is active. Extend for S3, Lambda, GCP, Azure, etc.
