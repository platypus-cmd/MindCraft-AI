# MindCraft AI Deployment Guide

This guide explains how to deploy MindCraft AI to production using Render for the backend and Vercel for the frontend.

## 1. Render Setup (Backend)
MindCraft AI uses a native Python environment on Render. 

- **Root Directory:** `backend`
- **Build Command:** `./build.sh` (installs Python packages and Playwright Chromium)
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python Version:** Pinned to `3.11.9` (via `.python-version` and `render.yaml`)
- **Environment Variables:**
  - `PYTHON_VERSION=3.11.9`
  - `ENVIRONMENT=production`
  - `CORS_ALLOWED_ORIGINS=https://<your-vercel-domain>.vercel.app`
  - `GEMINI_API_KEY=<your-api-key>`

**Note on `render.yaml`:**
You can deploy the backend automatically by connecting your GitHub repository to Render and selecting the Blueprint (`render.yaml`) deployment method.

## 2. Vercel Setup (Frontend)
MindCraft AI is a vanilla JavaScript frontend hosted on Vercel.

- **Root Directory:** `frontend`
- **Framework Preset:** `Other` (Static HTML/JS)
- **vercel.json Explanation:** The `vercel.json` file configures Vercel edge rewrites. It transparently forwards any frontend requests matching `/api/(.*)` to the `https://mindcraft-backend.onrender.com/api/$1` backend URL. This prevents CORS preflight issues and avoids hardcoding the production backend URL into the client-side JavaScript.

## 3. GitHub Deployment Flow
1. Push your code to the `main` branch.
2. Vercel automatically detects changes in the `frontend/` directory and triggers a new preview or production build.
3. Render automatically detects changes in the `backend/` directory and rebuilds the Python web service.

## 4. First Deployment
1. Deploy the Backend on Render first. Obtain the `.onrender.com` URL.
2. Update the `frontend/vercel.json` file to point to your new Render backend URL.
3. Deploy the Frontend on Vercel. Obtain the `.vercel.app` URL.
4. Update the `CORS_ALLOWED_ORIGINS` in your Render environment variables to include your `.vercel.app` URL.

## 5. Common Deployment Failures
- **Playwright PDF Export Fails (500 Error):** If the PDF export endpoint crashes, Render's native Python environment might be missing OS-level shared libraries required by Chromium (like `libgbm1` or `libnss3`). If this occurs, you will see a "missing shared library" stack trace in the Render logs.
- **CORS Errors:** If the frontend console shows CORS preflight blocks, ensure `CORS_ALLOWED_ORIGINS` on Render exactly matches your Vercel URL (with `https://` and no trailing slash).
- **404 on API calls:** Ensure `vercel.json` was properly recognized and the destination matches your Render URL exactly.

## 6. Troubleshooting Guide
- **Checking Backend Health:** Navigate to `https://<your-render-url>/api/v1/health`. It should return a 200 OK JSON status.
- **Reviewing Render Logs:** Check the Render dashboard for the specific worker logs if PDF generation or Gemini API calls fail.
- **Environment Validation:** Verify `GEMINI_API_KEY` is correctly set in Render without trailing spaces.

## 7. Post-Deployment Verification Checklist
See `RELEASE_CHECKLIST.md` for a comprehensive verification workflow.
