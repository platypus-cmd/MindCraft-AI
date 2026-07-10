/**
 * API communication layer.
 *
 * Kept separate from DOM rendering logic (see main.js) so that network
 * concerns and UI concerns don't mix, per PROJECT_CONTEXT.md section 29
 * (JavaScript coding standards).
 */

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Calls GET /api/v1/health on the backend.
 * Returns the parsed JSON body on success.
 * Throws an error on network failure or a non-OK HTTP status.
 */
async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`Backend responded with status ${response.status}`);
  }

  return response.json();
}

async function generateNotes(payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1/notes/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Notes generation failed.");
  }

  return data;
}
