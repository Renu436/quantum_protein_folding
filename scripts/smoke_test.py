#!/usr/bin/env python3
"""Simple smoke test: start backend, wait for health, POST /simulate, validate response.

This script starts uvicorn as a subprocess on the chosen port and shuts it down
after the test. It uses only the Python standard library to avoid extra deps.
"""
import subprocess
import sys
import time
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def wait_for_health(url, timeout=15.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(url) as r:
                return r.read().decode()
        except Exception:
            time.sleep(0.3)
    raise RuntimeError("Health check timed out")


def post_simulate(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=10) as r:
        return json.load(r)


def main():
    port = 8001
    base = f"http://127.0.0.1:{port}"
    # Start uvicorn in a subprocess
    cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        print("Waiting for backend to become healthy...")
        wait_for_health(base + "/health", timeout=20)
        print("Backend healthy, running simulate POST...")
        resp = post_simulate(base + "/simulate", {"sequence": "HHPH"})
        print("Response keys:", list(resp.keys()))
        if "sequence" not in resp:
            raise RuntimeError("simulate response missing sequence")
        print("Smoke test passed")
    finally:
        p.terminate()
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()


if __name__ == "__main__":
    main()
