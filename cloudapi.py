#!/usr/bin/env python3
from fastapi import FastAPI, Request, BackgroundTasks, WebSocket
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess, os, json, time, asyncio, threading

app = FastAPI(title="Artemis CodexOps API")
app.mount("/web", StaticFiles(directory="web", html=True), name="web")
app.mount("/logs", StaticFiles(directory="logs", html=True), name="logs")

# --- Caching ---
cache = {"artemis": None, "ts": 0}
CACHE_TTL = 60  # seconds

def run_agent_sync(cmd):
    try:
        t0 = time.time()
        result = subprocess.check_output(cmd, timeout=20)
        exec_time = round(time.time() - t0, 3)
        return result, exec_time
    except Exception as e:
        return json.dumps({"error": str(e)}).encode(), 0

@app.get("/")
def root():
    return HTMLResponse('<meta http-equiv="refresh" content="0;URL=\'/web/\'" />')

@app.get("/api/artemis")
async def artemis_status():
    now = time.time()
    if cache["artemis"] and (now - cache["ts"] < CACHE_TTL):
        data = cache["artemis"]
    else:
        loop = asyncio.get_event_loop()
        result, exec_time = await loop.run_in_executor(None, run_agent_sync, ["python3", "agents/codexagent_nasa_artemis.py"])
        try:
            data = json.loads(result)
            data["exec_time"] = exec_time
        except:
            data = {"status": "error", "exec_time": exec_time}
        cache["artemis"] = data
        cache["ts"] = now
    return JSONResponse(content=data)

@app.get("/api/metrics")
async def get_metrics():
    import psutil
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    return {"cpu": cpu, "mem": mem, "uptime": time.time() - psutil.boot_time()}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    logfile = "logs/agent.log"
    pos = 0
    while True:
        if os.path.exists(logfile):
            with open(logfile) as f:
                f.seek(pos)
                lines = f.readlines()
                pos = f.tell()
                if lines:
                    await websocket.send_text(''.join(lines[-10:]))
        await asyncio.sleep(3)

@app.get("/api/log")
def get_log():
    try:
        with open("logs/agent.log", "r") as f:
            log = f.read().splitlines()[-20:]
    except:
        log = []
    return {"log": log}

@app.get("/api/status")
def get_status():
    try:
        with open("logs/agent_status.json", "r") as f: status = json.load(f)
    except Exception:
        status = {"status": "No status yet"}
    return status

@app.get("/api/agents")
def list_agents():
    files = [f for f in os.listdir("agents") if f.endswith(".py")]
    return {"agents": files}

@app.post("/api/run-agent")
async def run_agent(req: Request):
    data = await req.json()
    fname = data.get("agent")
    if not fname or not fname.endswith(".py") or "/" in fname: return JSONResponse({"error": "invalid agent"}, status_code=400)
    loop = asyncio.get_event_loop()
    result, exec_time = await loop.run_in_executor(None, run_agent_sync, ["python3", f"agents/{fname}"])
    try:
        output = json.loads(result)
    except:
        output = {"output": result.decode()}
    output["exec_time"] = exec_time
    return JSONResponse(content=output)
