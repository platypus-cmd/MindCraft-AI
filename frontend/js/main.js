/**
 * DOM rendering and interaction logic for the Milestone 1 dev page.
 * Network calls live in api.js; this file only updates the UI.
 */

const statusTextEl = document.getElementById("status-text");
const checkButtonEl = document.getElementById("check-connection-btn");

function setStatus(state, message) {
  statusTextEl.dataset.state = state;
  statusTextEl.textContent = message;
}

async function handleCheckConnection() {
  checkButtonEl.disabled = true;
  setStatus("checking", "Checking backend connection...");

  try {
    const data = await checkBackendHealth();
    setStatus(
      "connected",
      `Connected: ${data.app_name} (API ${data.api_version}), status "${data.status}".`
    );
  } catch (error) {
    setStatus(
      "error",
      "Could not reach the backend. Make sure the FastAPI server is running."
    );
  } finally {
    checkButtonEl.disabled = false;
  }
}

checkButtonEl.addEventListener("click", handleCheckConnection);
