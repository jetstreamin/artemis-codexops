from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os, json, time

app = FastAPI(title="Artemis CodexOps API")

@app.post("/api/agent_post")
async def agent_post(request: Request):
    try:
        data = await request.json()
        ts = time.strftime("%Y%m%d-%H%M%S")
        os.makedirs("logs", exist_ok=True)
        dump_file = f"logs/agent_post_{ts}.json"
        with open(dump_file, "w") as f:
            json.dump(data, f, indent=2)
        return JSONResponse(content={"result": "ok", "dump": dump_file}, status_code=200)
    except Exception as e:
        error_ts = time.strftime("%Y%m%d-%H%M%S")
        crash_file = f"logs/agent_post_crash_{error_ts}.log"
        with open(crash_file, "w") as f:
            f.write(f"Exception: {e}\n")
            try:
                body = await request.body()
                f.write(f"\nRaw body:\n{body}\n")
            except:
                pass
        return JSONResponse(content={"result": "error", "detail": str(e), "crash_dump": crash_file}, status_code=500)
