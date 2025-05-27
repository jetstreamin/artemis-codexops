"""
Artemis CodexOps Dashboard API

- Serves live agent status, improvement suggestions, and usage analytics for the mesh dashboard.
- Reads from local logs and agent data.
- Provides a WebSocket endpoint for real-time dashboard updates.
"""

from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import asyncio

app = FastAPI(title="Mesh Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_PATH = "artemis-codexops/ops_agent.log"
MASTER_LOG_PATH = "artemis-codexops/master_builder.log"
USAGE_LOG = "artemis-codexops/usage.log"

@app.get("/status")
def get_agent_status():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()[-10:]
        return {"status": "ok", "log": "".join(lines)}
    return {"status": "no log found"}

@app.get("/suggestions")
def get_suggestions():
    if os.path.exists(MASTER_LOG_PATH):
        with open(MASTER_LOG_PATH, "r") as f:
            lines = f.readlines()[-10:]
        return {"suggestions": "".join(lines)}
    return {"suggestions": "no suggestions found"}

@app.get("/usage")
def get_usage():
    if os.path.exists(USAGE_LOG):
        with open(USAGE_LOG, "r") as f:
            usage = f.read()
        return {"usage": usage}
    return {"usage": "no usage data found"}

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send latest status, suggestions, and usage every 5 seconds
            status = get_agent_status()
            suggestions = get_suggestions()
            usage = get_usage()
            await websocket.send_json({
                "status": status,
                "suggestions": suggestions,
                "usage": usage
            })
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()

from fastapi.responses import JSONResponse

@app.options("/feedback")
async def options_feedback():
    return JSONResponse(status_code=200, content={})

@app.post("/feedback")
async def post_feedback(request: Request):
    data = await request.json()
    feedback = data.get("feedback", "")
    log_dir = "artemis-codexops"
    log_file = os.path.join(log_dir, "feedback.log")
    if feedback:
        os.makedirs(log_dir, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().isoformat()} {feedback}\n")
        # Optionally, broadcast to mesh or notify master builder
        return {"status": "ok", "message": "Feedback received"}
    return {"status": "error", "message": "No feedback provided"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10010)
