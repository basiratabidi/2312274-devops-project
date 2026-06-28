##
## CORS + /logs patch for your FastAPI app (main.py)
## ─────────────────────────────────────────────────
## Copy the relevant sections into your existing main.py.
## The minimal change is the CORSMiddleware block (Step 1).
## Steps 2 and 3 are optional quality-of-life additions.
##

# ── Step 1 · Add CORS middleware (REQUIRED) ────────────────────────────────────
#
# Place this right after you create the FastAPI app object:
#
#   app = FastAPI(...)          ← your existing line
#
# Then add:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to your domain in production
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# ── Step 2 · Richer health endpoint (optional) ────────────────────────────────
#
# Replace your existing /health route with this one so the dashboard
# can display more info in the top-bar chip.

@app.get("/health")
def health():
    return {
        "student": "2312274",
        "status": "ok",
        "service": "devops-project",
    }


# ── Step 3 · /logs endpoint (optional) ───────────────────────────────────────
#
# The dashboard's Logs tab calls GET /logs.
# If this route doesn't exist, the tab shows simulated logs — that's fine.
# Add this only if you want real log streaming from the API.
#
# Requires: pip install aiofiles   (add to requirements.txt)

import subprocess
from fastapi.responses import JSONResponse

@app.get("/logs")
def get_logs():
    """Return the last 50 lines from the container's stdout log."""
    try:
        result = subprocess.run(
            ["tail", "-n", "50", "/proc/1/fd/1"],
            capture_output=True, text=True, timeout=3
        )
        lines = result.stdout.strip().splitlines()
    except Exception:
        lines = ["Log access unavailable — check container permissions."]

    return JSONResponse({
        "logs": [
            {"ts": "", "level": "INFO", "msg": line}
            for line in lines
        ]
    })
