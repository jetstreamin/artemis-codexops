
def agent_self_post(name, status="online", version="1.0", endpoint="http://localhost:8080/api/agent_post"):
    data = {
        "agent_name": name,
        "status": status,
        "version": version,
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "timestamp": time.time()
    }
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")
    try:
        requests.post(endpoint, json=data, timeout=2)
        print(f"[SELF-POST] {name} posted status to {endpoint}")
    except Exception as e:
        print(f"[SELF-POST] Failed to post agent status: {e}")


#!/usr/bin/env python3
"""
Vision Agent: captures image from device camera (Termux, Linux, Mac, or Windows).
- Termux: uses termux-camera-photo.
- Desktop: uses OpenCV for webcam capture.
- Can be called by other agents, exposes output via logs and web API.
"""
import os, sys, time

def termux_camera():
    out = f"logs/capture_{int(time.time())}.jpg"
    os.system(f"termux-camera-photo -c 0 {out}")
    print(f"Saved: {out}")

def opencv_camera():
    try:
        import cv2
    except ImportError:
        print("Install opencv-python (pip install opencv-python)")
        sys.exit(1)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    out = f"logs/capture_{int(time.time())}.jpg"
    if ret:
        cv2.imwrite(out, frame)
        print(f"Saved: {out}")
    cap.release()

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    if os.getenv("TERMUX_VERSION"):
        termux_camera()
    else:
        opencv_camera()
