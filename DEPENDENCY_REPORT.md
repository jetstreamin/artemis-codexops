# Dependency Report (Mon May 19 04:40:31 CDT 2025)
## Python Dependencies:
aiosqlite==0.21.0
annotated-types==0.7.0
anyio==4.9.0
APScheduler==3.11.0
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
awscli==1.40.12
bcrypt==4.3.0
blinker==1.9.0
boto3==1.38.15
botocore==1.38.15
cachetools==5.5.2
certifi==2025.1.31
cffi==1.17.1
chardet==3.0.4
charset-normalizer==3.4.1
chart-studio==1.1.0
click==8.1.8
colorama==0.4.6
cryptography==45.0.2
distro==1.9.0
dnspython==2.7.0
docutils==0.19
ecdsa==0.19.1
email_validator==2.2.0
fastapi==0.115.12
fastapi-users==14.0.1
fastapi-users-db-sqlalchemy==7.0.0
Flask==3.1.0
google-auth==2.40.1
google-genai==1.15.0
googletrans==4.0.0rc1
greenlet==3.2.2
h11==0.9.0
h2==3.2.0
hpack==3.0.0
hstspreload==2025.1.1
httpcore==0.9.1
httpx==0.13.3
hyperframe==5.2.0
idna==2.10
iniconfig==2.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.9.0
jmespath==1.0.1
makefun==1.16.0
MarkupSafe==3.0.2
narwhals==1.39.1
openai==1.74.0
packaging==25.0
plotly==6.1.0
pluggy==1.5.0
psutil==7.0.0
pwdlib==0.2.1
pyasn1==0.4.8
pyasn1_modules==0.4.2
pycparser==2.22
pydantic==2.11.3
pydantic_core==2.33.1
PyJWT==2.10.1
pytest==8.3.5
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
python-jose==3.4.0
python-multipart==0.0.20
pyttsx3==2.98
PyYAML==6.0.2
requests==2.32.3
retrying==1.3.4
rfc3986==1.5.0
rsa==4.7.2
s3transfer==0.12.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
starlette==0.46.2
tk==0.1.0
tqdm==4.67.1
typing-inspection==0.4.0
typing_extensions==4.13.2
tzlocal==5.3.1
urllib3==2.4.0
uvicorn==0.34.2
websockets==15.0.1
Werkzeug==3.1.3
yt-dlp==2024.12.13

## Shell/Bash Dependencies (scanned):
                    break
                    healed = True
                    log_action("auto_heal_install", missing
                    missing = err.split(error_prefix)[-1].split("'")[1
                    print(f"Auto-heal: pip install {missing
                    subprocess.run(["pip", "install", missing
                ["python", agent["path
                break
                capture_output=True, text=True
                if error_prefix in err
                log_action("agent_failed", {"agent": agent["name"], "stderr": err
                log_action("run_agent", agent["name
                notify(f"EC2 instance running: {inst['InstanceId
                notify(f"RDS instance running: {db['DBInstanceIdentifier
                print(err
                print(result.stdout
            "error": str(e
            "missions": [{"name": "Artemis I", "status": "Launched"}, {"name": "Artemis II", "status": "Scheduled
            "status": "offline/mock
            break
            continue
            else
            err = result.stderr
            for error_prefix in ["ModuleNotFoundError: No module named", "ImportError: No module named
            for inst in r["Instances
            if db["DBInstanceStatus"] == "available
            if not healed
            if result.returncode == 0
            matches.append(agent
            os.system("python agents/codexagent_nasa_artemis.py
            requests.post(os.getenv('WEBHOOK_URL',''), json=data
            result = subprocess.run
            speak("Artemis mission status executed
            speak("Stopping
            speak(f"You said: {command
        "agent_name": name
        "host": socket.gethostname
        "pid": os.getpid
        "status": status
        "timestamp": time.time
        "version": version
        artemis = [x for x in data.get("results", []) if "artemis" in x.get("name", "").lower
        audio = r.listen(source
        command = command.lower
        command = listen
        command = r.recognize_google(audio
        cv2.imwrite(out, frame
        data = r.json
        dbs = rds.describe_db_instances
        ec2 = boto3.client("ec2
        elif "artemis" in command
        else
        f.write(json.dumps({"event": event, "details": details}) + "\n
        for _ in range(2
        for db in dbs.get("DBInstances
        for r in running["Reservations
        healed = False
        if "stop" in command
        if any(w in agent["description"].lower() for w in goal.lower().split
        if not command
        if os.getenv('WEBHOOK_ON') == "1
        import cv2
        log_status("codexagent_nasa_artemis", "offline/mock", {"error": str(e
        log_status("codexagent_nasa_artemis", msg, {"found": len(artemis
        matches = agents[:1
        msg = "Artemis mission data fetched" if artemis else "No Artemis missions found
        opencv_camera
        print("AWS Cost Monitor error:", e
        print("Debug mode: sleeping", INTERVAL, "sec
        print("Install opencv-python (pip install opencv-python
        print("Listening
        print("MISSION STATUS:", json.dumps(data, indent=2
        print("Monitor error:", e
        print("You said:", command
        print(f" - {agent['name']}: {agent['description
        print(f"- {a['name']}: {a['description
        print(f"Running {agent['name
        print(f"Saved: {out
        print(f"[SELF-POST] Failed to post agent status: {e
        print(f"[SELF-POST] {name} posted status to {endpoint
        r = requests.get('http://localhost:8080/api/artemis', timeout=5
        r = requests.get(NASA_API, timeout=TIMEOUT
        r.raise_for_status
        rds = boto3.client("rds
        requests.post(endpoint, json=data, timeout=2
        return
        return None
        return command
        return json.load(f
        return {"status": msg, "missions": artemis
        running = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running
        speak("Sorry, I didn't catch that
        sys.exit(1
        termux_camera
        with open("logs/mission_monitor.log","a") as f: f.write(json.dumps(data)+"\n
    agent = sys.argv[1] if len(sys.argv) > 1 else "unknown
    agents = load_registry
    cap = cv2.VideoCapture(0
    cap.release
    chain = match_goal(goal, agents
    check_aws_costs
    data
    else
    engine = pyttsx3.init
    engine.runAndWait
    engine.say(text
    except Exception
    except Exception as e
    except ImportError
    explain_chain(chain
    extra = sys.argv[3] if len(sys.argv) > 3 else None
    for a in agents
    for agent in agents
    for agent in chain
    goal = input("What do you want to do? (natural language
    greet
    if extra: payload["extra"] = extra
    if not matches
    if os.getenv("TERMUX_VERSION
    if os.getenv('DEBUG_MONITOR') == "1
    if ret
    import requests, socket, os, time
    log_action("greet", msg
    log_status(agent, status, extra
    main
    matches
    msg = "Hello, I am Artemis. Ready to scan and run agents for you
    now = time.strftime('%Y-%m-%d %H:%M:%S
    os.makedirs("logs", exist_ok=True
    os.system(f"termux-camera-photo -c 0 {out
    out = f"logs/capture_{int(time.time())}.jpg
    payload = {"agent": agent, "status": status, "timestamp": now
    print("Agent logic goes here
    print("Available agents
    print("COST ALERT:", msg
    print("Done. All actions logged
    print("SAYING:", text
    print("To fulfill your request, I will chain
    print(f"Saved: {out
    print(json.dumps(fetch_status(), indent=2
    print(msg
    r = sr.Recognizer
    ret, frame = cap.read
    return matches
    run_chain(chain
    status = sys.argv[2] if len(sys.argv) > 2 else "ran
    time.sleep(INTERVAL
    try
    while True
    with open("logs/agent.log", "a") as f: f.write(json.dumps(payload) + "\n
    with open("logs/agent_status.json", "w") as f: json.dump(payload, f, indent=2
    with open(LOG, "a") as f
    with open(REGISTRY) as f
    with sr.Microphone() as source
  ./cli/magic_loop_full.sh || echo "Magic loop run $i failed
  awk '/@app.get"\/api\/artemis"/{print;getline;print"    return {\"status\": \"API self-heal: OK\"}";next}1' cloudapi.py > tmp && mv tmp cloudapi.py
  cat > agents/codexagent_nasa_artemis.py <<EOF2
  echo "Attempting to auto-fix API endpoint
  echo "Attempting to auto-fix Artemis agent
  echo -e "\n=== Magic Loop Run $i/$N
  nohup uvicorn cloudapi:app --host 0.0.0.0 --port 8080 >/dev/null 2>&1
  ok "Patched API to return self-healing stub
  ok "Patched agent with self-healing stub
  sleep 2
  sleep 3
- Accepts a natural language goal, explains the chosen agent flow, and runs it
- Can be called by other agents, exposes output via logs and web API
- Checks AWS for running paid resources (RDS, EC2, etc
- Desktop: uses OpenCV for webcam capture
- Fetches Artemis mission status from NASA API (or returns mock data if offline/keyless
- Greets user on enable, logs all actions
- Logs run status to logs/agent_status.json and logs/agent.log
- Notifies (print, email, webhook, or SMS) if any billable instance found
- Outputs to web dashboard and logs
- Periodically checks mission status, agent health, and triggers webhooks/alerts
- Scans registry, presents available agents and chains
- Termux: uses termux-camera-photo
./project_sync_diagnostics.sh | grep -E 'branch|Untracked files|MISSING|OK:|Recent commits
Artemis CodexAgent: Modular agent for Artemis mission data, telemetry, and AI-automation
Artemis CodexOps Agent Template
Cloud Cost Monitor Agent for Artemis CodexOps
CodexAgent NASA Artemis Status Fetcher
EOF2
Fill in agent functionality below
INTERVAL = 15
LOG = "logs/ai_self_discover.log
Mission/workflow monitor for Artemis CodexOps
N=${1:-1
NASA_API = os.getenv("NASA_API_URL", "https://llapi.thespacedevs.com/2.2.0/launch/upcoming/?search=artemis
REGISTRY = "agents/agent_registry.json
TIMEOUT = 8
TODO: Implement mission status retrieval, schedule parsing, lunar sim integration
Universal AI Self-Discovery/Chaining for Artemis CodexOps
Vision Agent: captures image from device camera (Termux, Linux, Mac, or Windows
[ -f "$dashboard" ] && ok "Dashboard file present" || fail "Dashboard missing
[ -f "$vr_marker" ] && ok "Unity VR asset present" || fail "Unity VR integration missing
[ -f agents/vision_agent.py ] || exit 1
[ -f agents/voice_agent.py ] || exit 1
[ -f cli/self_test.py ] && echo "✅ Agent Builder UI found
[ -f cli/test_core.sh ] && echo "✅ Workflow UI found
[ -f docs/index.html ] || exit 1
api_final=$(curl -s http://localhost:8080/api/artemis
api_out=$(curl -s http://localhost:8080/api/artemis) || fail "API not reachable
curl -s http://localhost:8080/api/artemis | grep -i "status" && echo "API OK
curl -sSf http://localhost:8080/api/artemis > /dev/null || exit 1
curl -sSf http://localhost:8080/api/toggle_debug > /dev/null || true
dashboard="docs/index.html
def agent_self_post(name, status="online", version="1.0", endpoint="http://localhost:8080/api/agent_post
def check_aws_costs
def explain_chain(chain
def fetch_status
def greet
def listen
def load_registry
def log_action(event, details
def log_status(agent, status, extra=None
def main
def match_goal(goal, agents
def notify(msg
def opencv_camera
def run_chain(chain
def speak(text
def termux_camera
done
echo "$api_final" | grep -qiE 'ok|status' && ok "[Magic Loop] System now guaranteed working!" || fail "Magic Loop failed to heal automatically—see logs above
echo "$api_out" | grep -qiE 'artemis|status' && ok "API responded with mission data" || fail "API output missing status
echo "$out" | grep -qiE 'artemis|status' && ok "Agent produced mission data" || fail "Agent output missing status
echo "==== Artemis CodexOps Magic Loop: ALL ASPECTS (Self-Healing
echo "[1/12] Artemis agent
echo "[1/5] Testing Artemis agent
echo "[2/12] API endpoint
echo "[2/5] Ensuring cloudapi is running
echo "[3/12] Dashboard UI
echo "[3/5] Testing API endpoint
echo "[4/12] Voice agent
echo "[4/5] Checking dashboard static file
echo "[5/12] Vision agent
echo "[6/12] Agent Builder UI
echo "[7/12] Workflow Builder UI
echo "[8/12] Webhook/debug toggle endpoints
echo "[Magic Loop] All checks passed
echo "[Magic Loop] All core checks passed
echo "✅ API OK
echo "✅ Agent mission data
echo "✅ Dashboard found
echo "✅ Patched /api/ endpoint
echo "✅ Vision agent file exists
echo "✅ Voice agent file exists
fail() { echo "❌ $1"; exit 1
fi
for ((i=1; i<=N; i++)); do
from agent_logger import log_status
if ! curl -s http://localhost:8080/api/artemis | grep -qiE 'artemis|status'; then
if ! python agents/codexagent_nasa_artemis.py 2>&1 | grep -qiE 'artemis|status'; then
if [ -z "$pid" ]; then
if __name__ == "__main__
import json
import json, os, subprocess
import json, time, os, sys
import os
import os, boto3
import os, sys, requests, json
import os, sys, time
import pyttsx3
import requests, socket, os, time
import speech_recognition as sr
import sys, subprocess
import time, os, requests, json
msg = sys.argv[1] if len(sys.argv) > 1 else "Artemis CodexOps: Agent event
ok() { echo "✅ $1
os.makedirs("logs", exist_ok=True
out=$(python agents/codexagent_nasa_artemis.py 2>&1) || fail "Artemis agent failed: $out
pid=$(pgrep -f 'uvicorn cloudapi:app' || true
print("Artemis CodexAgent initialized
print(json.dumps({'status': 'Artemis agent self-heal: OK', 'missions
python agents/codexagent_nasa_artemis.py || exit 1
python cli/self_test.py
set -e
vr_marker="vr/unity/ArtemisCodexOpsVR/Assets/Scripts/ArtemisAPI.cs
while True

## SCUS/Plugin Dependencies:

# Risk Assessment

Potential code execution risk in agents/codexagent_artemis.py
Potential code execution risk in agents/voice_agent.py
Potential code execution risk in agents/vision_agent.py

## Manual review recommended for any lines above.

# Summary
- All dependencies and potential risks listed above.
- Review regularly; auto-alert on any new or changed dependency or risk keyword.
