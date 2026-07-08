# MindCraft AI — Milestone 1: Foundation

This README currently covers **local development setup only**, for Milestone 1
(backend skeleton, frontend skeleton, and health-check connectivity).
Deployment instructions will be added in a later milestone once deployment is
actually implemented.

See `docs/PROJECT_CONTEXT.md` for the full product and engineering spec.

## Prerequisites

* Python 3.10+ installed and available on PATH (`python --version`).
* No Node.js or other runtime is required — the frontend is plain HTML/CSS/JS.

All commands below are written for **Windows PowerShell**.

## 1. Backend Setup

From the repository root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks the activation script with an execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

and then re-run the activation command.

## 2. Create Your Local Environment File

Copy the example file:

```powershell
Copy-Item .env.example .env
```

`backend/.env` is loaded automatically by the application's settings
(`app/core/config.py`) and is listed in `.gitignore`, so it will never be
committed. Edit the values inside `.env` if your setup differs from the
defaults (for example, if you serve the frontend on a different port).

Gemini-related environment variables are intentionally **not** part of this
file yet — they will be added when Gemini integration begins in a later
milestone.

## 3. Start the Backend

With the virtual environment active and still inside `backend/`:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Test the Health Endpoint Directly

In a browser, or a second PowerShell window:

```powershell
curl http://127.0.0.1:8000/api/v1/health
```

Expected response shape:

```json
{
  "app_name": "MindCraft AI",
  "status": "ok",
  "api_version": "v1"
}
```

You can also open `http://127.0.0.1:8000/docs` in a browser for the
interactive FastAPI docs.

## 4. Serve the Frontend

Open a **new** PowerShell window (keep the backend running in the first one).
From the repository root:

```powershell
python -m http.server 5500 --directory frontend
```

This is the default method for this milestone. It serves `frontend/index.html`
at `http://127.0.0.1:5500`.

**Optional alternative:** if you use VS Code, the "Live Server" extension can
also serve the `frontend/` folder. If you use a different port with either
method, update `FRONTEND_ORIGIN` in `backend/.env` to match, then restart the
backend.

## 5. Verify Frontend-to-Backend Communication

1. With both servers running, open `http://127.0.0.1:5500` in a browser.
2. Click **"Check Backend Connection."**
3. The status text should change to a connected message showing the app name,
   API version, and status returned by the backend.
4. To confirm the error state works, stop the backend (`Ctrl+C` in its
   terminal) and click the button again — the page should show a
   "could not reach the backend" message rather than crashing silently.

## Verification Checklist

Run through this manually and confirm each item yourself — do not assume any
item passes without running it:

* [ ] `pip install -r requirements.txt` completes without errors.
* [ ] `uvicorn app.main:app --reload` starts without errors.
* [ ] `GET http://127.0.0.1:8000/api/v1/health` returns the expected JSON.
* [ ] `python -m http.server 5500 --directory frontend` serves the page at
      `http://127.0.0.1:5500`.
* [ ] Clicking "Check Backend Connection" shows a connected message while the
      backend is running.
* [ ] Stopping the backend and clicking the button again shows an error
      message instead of a silent failure or crash.

## Repository Structure (Milestone 1)

```text
MindCraft-AI/
|
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- v1/
|   |   |   |   |-- health.py
|   |   |
|   |   |-- core/
|   |   |   |-- config.py
|   |   |
|   |   |-- main.py
|   |
|   |-- requirements.txt
|   |-- .env.example
|
|-- frontend/
|   |-- css/
|   |   |-- style.css
|   |-- js/
|   |   |-- api.js
|   |   |-- main.js
|   |-- index.html
|
|-- docs/
|   |-- PROJECT_CONTEXT.md
|
|-- .gitignore
|-- README.md
```
