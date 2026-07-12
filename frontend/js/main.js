/**
 * DOM rendering and interaction logic.
 * Network calls live in api.js; this file only updates the UI.
 */

const statusTextEl = document.getElementById("status-text");
const checkButtonEl = document.getElementById("check-connection-btn");
const notesFormEl = document.getElementById("notes-form");
const sourceTextEl = document.getElementById("source-text");
const learningGoalEl = document.getElementById("learning-goal");
const knowledgeLevelEl = document.getElementById("knowledge-level");
const noteLengthEl = document.getElementById("note-length");
const outputFormatEl = document.getElementById("output-format");
const notesMessageEl = document.getElementById("notes-message");
const generateNotesButtonEl = document.getElementById("generate-notes-btn");
const notesOutputEl = document.getElementById("notes-output");
const notesMetaEl = document.getElementById("notes-meta");
const notesContentEl = document.getElementById("notes-content");
const copyNotesButtonEl = document.getElementById("copy-notes-btn");
const exportPdfButtonEl = document.getElementById("export-pdf-btn");
const notesUtilityMessageEl = document.getElementById("notes-utility-message");
const pdfFileEl = document.getElementById("pdf-file");
const extractPdfButtonEl = document.getElementById("extract-pdf-btn");
const pdfMessageEl = document.getElementById("pdf-message");

let isGeneratingNotes = false;
let isExtractingPdf = false;
let isExportingPdf = false;
let latestNotesResponse = null;

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

function setNotesMessage(state, message) {
  notesMessageEl.dataset.state = state;
  notesMessageEl.textContent = message;
}

function setNotesUtilityMessage(state, message) {
  notesUtilityMessageEl.dataset.state = state;
  notesUtilityMessageEl.textContent = message;
}

function updateNotesUtilityButtons() {
  const hasGeneratedNotes = latestNotesResponse !== null;
  copyNotesButtonEl.disabled = !hasGeneratedNotes;
  exportPdfButtonEl.disabled = !hasGeneratedNotes || isExportingPdf;
}

function buildNotesPayload() {
  return {
    source_text: sourceTextEl.value.trim(),
    learning_goal: learningGoalEl.value,
    knowledge_level: knowledgeLevelEl.value,
    note_length: noteLengthEl.value,
    output_format: outputFormatEl.value,
  };
}

function validateNotesPayload(payload) {
  if (payload.source_text.length < 50) {
    return "Paste at least 50 characters of source material.";
  }

  if (payload.source_text.length > 20000) {
    return "Source material must be 20,000 characters or less.";
  }

  return "";
}

function appendTextElement(parent, tagName, text, className) {
  if (!text) {
    return null;
  }

  const element = document.createElement(tagName);
  element.textContent = text;

  if (className) {
    element.className = className;
  }

  parent.appendChild(element);
  return element;
}

function appendList(parent, title, items) {
  if (!Array.isArray(items) || items.length === 0) {
    return;
  }

  appendTextElement(parent, "h4", title);
  const list = document.createElement("ul");

  items.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    list.appendChild(listItem);
  });

  parent.appendChild(list);
}

function appendDefinitions(parent, definitions) {
  if (!Array.isArray(definitions) || definitions.length === 0) {
    return;
  }

  appendTextElement(parent, "h4", "Definitions");
  const list = document.createElement("dl");

  definitions.forEach((item) => {
    appendTextElement(list, "dt", item.term);
    appendTextElement(list, "dd", item.definition);
  });

  parent.appendChild(list);
}

function formatListForCopy(title, items) {
  const lines = [`${title}:`];

  if (!Array.isArray(items) || items.length === 0) {
    lines.push("- None");
    return lines.join("\n");
  }

  items.forEach((item) => {
    lines.push(`- ${item}`);
  });

  return lines.join("\n");
}

function formatDefinitionsForCopy(definitions) {
  const lines = ["Definitions:"];

  if (!Array.isArray(definitions) || definitions.length === 0) {
    lines.push("- None");
    return lines.join("\n");
  }

  definitions.forEach((item) => {
    lines.push(`- ${item.term}: ${item.definition}`);
  });

  return lines.join("\n");
}

function formatNotesResponseAsPlainText(response) {
  const notes = response.notes;
  const sections = [
    notes.title,
    "",
    `Estimated reading time: ${response.estimated_reading_time_minutes} minute(s)`,
    "",
    formatListForCopy("Table of Contents", notes.table_of_contents),
  ];

  if (Array.isArray(notes.sections)) {
    notes.sections.forEach((section) => {
      sections.push(
        "",
        section.heading,
        "",
        section.content,
        "",
        formatListForCopy("Key Points", section.key_points),
        "",
        formatDefinitionsForCopy(section.definitions),
        "",
        formatListForCopy("Examples", section.examples),
        "",
        formatListForCopy("Memory Tricks", section.memory_tricks),
        "",
        formatListForCopy("Common Mistakes", section.common_mistakes)
      );
    });
  }

  sections.push(
    "",
    "Summary",
    "",
    notes.summary,
    "",
    formatListForCopy("Key Takeaways", notes.key_takeaways),
    "",
    "One-Minute Revision",
    "",
    notes.one_minute_revision
  );

  return sections.join("\n").trim();
}

function renderNotesResponse(response) {
  notesMetaEl.replaceChildren();
  notesContentEl.replaceChildren();

  const notes = response.notes;
  const meta = document.createElement("p");
  meta.textContent = `Estimated reading time: ${response.estimated_reading_time_minutes} minute(s)`;
  notesMetaEl.appendChild(meta);

  appendTextElement(notesContentEl, "h3", notes.title);
  appendList(notesContentEl, "Table of Contents", notes.table_of_contents);

  if (Array.isArray(notes.sections)) {
    notes.sections.forEach((section) => {
      const sectionEl = document.createElement("section");
      sectionEl.className = "generated-section";

      appendTextElement(sectionEl, "h3", section.heading);
      appendTextElement(sectionEl, "p", section.content);
      appendList(sectionEl, "Key Points", section.key_points);
      appendDefinitions(sectionEl, section.definitions);
      appendList(sectionEl, "Examples", section.examples);
      appendList(sectionEl, "Memory Tricks", section.memory_tricks);
      appendList(sectionEl, "Common Mistakes", section.common_mistakes);

      notesContentEl.appendChild(sectionEl);
    });
  }

  appendTextElement(notesContentEl, "h3", "Summary");
  appendTextElement(notesContentEl, "p", notes.summary);
  appendList(notesContentEl, "Key Takeaways", notes.key_takeaways);
  appendTextElement(notesContentEl, "h3", "One-Minute Revision");
  appendTextElement(notesContentEl, "p", notes.one_minute_revision);

  notesOutputEl.hidden = false;
}

async function handleGenerateNotes(event) {
  event.preventDefault();

  if (isGeneratingNotes) {
    return;
  }

  const payload = buildNotesPayload();
  const validationMessage = validateNotesPayload(payload);

  if (validationMessage) {
    setNotesMessage("error", validationMessage);
    return;
  }

  isGeneratingNotes = true;
  generateNotesButtonEl.disabled = true;
  setNotesMessage("loading", "Generating notes...");

  try {
    const response = await generateNotes(payload);
    latestNotesResponse = response;
    renderNotesResponse(response);
    updateNotesUtilityButtons();
    setNotesUtilityMessage("idle", "");
    setNotesMessage("success", "Notes generated successfully.");
  } catch (error) {
    setNotesMessage("error", error.message || "Could not generate notes.");
  } finally {
    isGeneratingNotes = false;
    generateNotesButtonEl.disabled = false;
  }
}

async function handleCopyNotes() {
  if (!latestNotesResponse) {
    setNotesUtilityMessage("error", "Generate notes before copying.");
    return;
  }

  if (!navigator.clipboard || !navigator.clipboard.writeText) {
    setNotesUtilityMessage("error", "Clipboard access is not available in this browser.");
    return;
  }

  try {
    await navigator.clipboard.writeText(
      formatNotesResponseAsPlainText(latestNotesResponse)
    );
    setNotesUtilityMessage("success", "Notes copied.");
  } catch (error) {
    setNotesUtilityMessage("error", "Could not copy notes.");
  }
}

async function handleExportPdf() {
  if (!latestNotesResponse || isExportingPdf) {
    return;
  }

  isExportingPdf = true;
  updateNotesUtilityButtons();
  setNotesUtilityMessage("loading", "Exporting PDF...");

  try {
    const pdfBlob = await exportNotesPdf(latestNotesResponse);
    const objectUrl = URL.createObjectURL(pdfBlob);
    const downloadLink = document.createElement("a");

    downloadLink.href = objectUrl;
    downloadLink.download = "mindcraft-notes.pdf";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    downloadLink.remove();
    URL.revokeObjectURL(objectUrl);

    setNotesUtilityMessage("success", "PDF export started.");
  } catch (error) {
    setNotesUtilityMessage("error", error.message || "Could not export PDF.");
  } finally {
    isExportingPdf = false;
    updateNotesUtilityButtons();
  }
}

function setPdfMessage(state, message) {
  pdfMessageEl.dataset.state = state;
  pdfMessageEl.textContent = message;
}

async function handleExtractPdf() {
  if (isExtractingPdf) {
    return;
  }

  const file = pdfFileEl.files[0];

  if (!file) {
    setPdfMessage("error", "Choose a PDF file first.");
    return;
  }

  if (sourceTextEl.value.trim().length > 0) {
    const shouldOverwrite = window.confirm(
      "This will replace the text currently in the source material box. Continue?"
    );

    if (!shouldOverwrite) {
      return;
    }
  }

  isExtractingPdf = true;
  extractPdfButtonEl.disabled = true;
  setPdfMessage("loading", "Extracting text from PDF...");

  try {
    const result = await extractPdfText(file);
    sourceTextEl.value = result.extracted_text;
    setPdfMessage(
      "success",
      `Extracted ${result.character_count} characters from ${result.page_count} page(s). Review the text below, then click Generate Notes.`
    );
  } catch (error) {
    setPdfMessage("error", error.message || "Could not extract text from that PDF.");
  } finally {
    isExtractingPdf = false;
    extractPdfButtonEl.disabled = false;
  }
}

checkButtonEl.addEventListener("click", handleCheckConnection);
notesFormEl.addEventListener("submit", handleGenerateNotes);
extractPdfButtonEl.addEventListener("click", handleExtractPdf);
copyNotesButtonEl.addEventListener("click", handleCopyNotes);
exportPdfButtonEl.addEventListener("click", handleExportPdf);
updateNotesUtilityButtons();
