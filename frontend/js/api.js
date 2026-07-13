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

/**
 * Uploads a PDF file and returns extracted text.
 * Uses FormData so the browser sets the correct multipart boundary itself;
 * the Content-Type header must not be set manually here.
 */
async function extractPdfText(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/v1/documents/extract`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "PDF text extraction failed.");
  }

  return data;
}

async function exportNotesPdf(notesResponse) {
  const response = await fetch(`${API_BASE_URL}/api/v1/notes/export/pdf`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(notesResponse),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "PDF export failed.");
  }

  return response.blob();
}

async function generateFlashcards(notesResponse) {
  const response = await fetch(`${API_BASE_URL}/api/v1/flashcards/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ notes_response: notesResponse }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Flashcard generation failed.");
  }

  return data;
}

async function generateQuiz(notesResponse) {
  const response = await fetch(`${API_BASE_URL}/api/v1/quiz/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ notes_response: notesResponse }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Quiz generation failed.");
  }

  return data;
}

async function generateRevision(payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1/revision/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Revision generation failed.");
  }

  return data;
}

async function generateRetest(payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/retest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Retest generation failed.");
  }

  return data;
}
