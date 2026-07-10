# MindCraft AI - Milestone 2: Notes Vertical Slice

MindCraft AI is a personalized AI study companion for college students. This
milestone implements the first complete notes workflow:

```text
Paste study material
-> choose learning preferences
-> generate structured notes with Gemini
-> validate the AI response
-> calculate reading time locally
-> safely render notes in the frontend
```

See `docs/PROJECT_CONTEXT.md` for the full product and engineering spec.

## Current Functionality

- FastAPI backend with `GET /api/v1/health`.
- `POST /api/v1/notes/generate` for AI-powered personalized notes.
- Dynamic prompt composition for learning goal, knowledge level, note length,
  and output format.
- Structured Gemini response validation with Pydantic.
- Deterministic reading-time calculation in backend code.
- Plain HTML/CSS/JavaScript frontend with safe DOM rendering.

Not included yet: PDF upload, flashcards, quizzes, revision, retests, copy
notes, PDF export, database, authentication, AWS deployment, or final visual
design.

## Prerequisites

- Python 3.10+ installed and available on PATH (`python --version`).
- No Node.js or frontend framework is required.
- A Gemini API key from Google AI Studio for real notes generation.

All commands below are written for Windows PowerShell.

## 1. Backend Setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks the activation script with an execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then re-run the activation command.

## 2. Configure Environment Variables

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Edit only your local `backend/.env` file. Do not commit it.

Required for notes generation:

```text
GEMINI_API_KEY=your_real_key_here
```

Optional Gemini settings:

```text
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT_SECONDS=30
```

`GET /api/v1/health` works even when `GEMINI_API_KEY` is not configured. Notes
generation requires the key and will fail with a sanitized server error without
it.

## 3. Start the Backend

With the virtual environment active and still inside `backend/`:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Health check:

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

## 4. Serve the Frontend

Open a new PowerShell window. From the repository root:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500` in a browser.

If you serve the frontend from a different origin, update `FRONTEND_ORIGIN` in
`backend/.env`, then restart the backend.

## 5. Run Tests

From the `backend/` directory with the virtual environment active:

```powershell
python -m unittest discover
```

The tests cover notes prompt personalization and backend request validation.
They do not call the real Gemini API.

## 6. Manual Notes Verification

After adding your real `GEMINI_API_KEY` to `backend/.env`:

1. Start the backend.
2. Serve the frontend.
3. Open `http://127.0.0.1:5500`.
4. Click `Check Backend Connection` and confirm the health message appears.
5. Paste at least 50 characters of study material.
6. Select one option each for Learning Goal, Knowledge Level, Note Length, and
   Output Format.
7. Click `Generate Notes`.
8. Confirm readable structured notes appear with estimated reading time.
9. Try different preference combinations and confirm the generated notes change
   meaningfully.

## Repository Structure

```text
MindCraft-AI/
|
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- v1/
|   |   |   |   |-- health.py
|   |   |   |   |-- notes.py
|   |   |
|   |   |-- core/
|   |   |   |-- config.py
|   |   |
|   |   |-- prompts/
|   |   |   |-- notes.py
|   |   |
|   |   |-- schemas/
|   |   |   |-- notes.py
|   |   |
|   |   |-- services/
|   |   |   |-- gemini_errors.py
|   |   |   |-- gemini_service.py
|   |   |   |-- notes_service.py
|   |   |
|   |   |-- main.py
|   |
|   |-- tests/
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
