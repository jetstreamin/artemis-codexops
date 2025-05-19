#!/usr/bin/env python3
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess, os, json

app = FastAPI(title="Artemis CodexOps API")

# Serve static dashboard
app.mount("/web", StaticFiles(directory="web", html=True), name="web")
app.mount("/logs", StaticFiles(directory="logs", html=True), name="logs")

@app.get("/", response_class=HTMLResponse)
def root():
    # Redirect to dashboard
    return '<meta http-equiv="refresh" content="0;URL=\'/web/\'" />'

@app.get("/api/artemis")
def artemis_status():
    try:
        result = subprocess.check_output(["python3", "agents/codexagent_nasa_artemis.py"], timeout=15)
        return JSONResponse(content=json.loads(result))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/agents")
def list_agents():
    files = [f for f in os.listdir("agents") if f.endswith(".py")]
    return {"agents": files}

@app.post("/api/run-agent")
async def run_agent(req: Request):
    data = await req.json()
    fname = data.get("agent")
    if not fname or not fname.endswith(".py") or "/" in fname: return JSONResponse({"error": "invalid agent"}, status_code=400)
    try:
        result = subprocess.check_output(["python3", f"agents/{fname}"], timeout=30)
        return JSONResponse(content={"output": result.decode()})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/log")
def get_log():
    with open("logs/agent.log", "r") as f: log = f.read().splitlines()[-20:]
    return {"log": log}

@app.get("/api/status")
def get_status():
    try:
        with open("logs/agent_status.json", "r") as f: status = json.load(f)
    except Exception:
        status = {"status": "No status yet"}
    return status
