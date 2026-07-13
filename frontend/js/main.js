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
const generateFlashcardsButtonEl = document.getElementById("generate-flashcards-btn");
const flashcardsOutputEl = document.getElementById("flashcards-output");
const flashcardsMessageEl = document.getElementById("flashcards-message");
const flashcardPrevButtonEl = document.getElementById("flashcard-prev-btn");
const flashcardNextButtonEl = document.getElementById("flashcard-next-btn");
const flashcardFlipButtonEl = document.getElementById("flashcard-flip-btn");
const flashcardProgressEl = document.getElementById("flashcard-progress");
const flashcardFrontEl = document.getElementById("flashcard-front");
const flashcardBackEl = document.getElementById("flashcard-back");
const generateQuizButtonEl = document.getElementById("generate-quiz-btn");
const quizOutputEl = document.getElementById("quiz-output");
const quizMessageEl = document.getElementById("quiz-message");
const quizPrevButtonEl = document.getElementById("quiz-prev-btn");
const quizNextButtonEl = document.getElementById("quiz-next-btn");
const quizSubmitButtonEl = document.getElementById("quiz-submit-btn");
const quizProgressEl = document.getElementById("quiz-progress");
const quizControlsEl = document.getElementById("quiz-controls");
const quizCardEl = document.getElementById("quiz-card");
const quizScoreEl = document.getElementById("quiz-score");
const quizSummaryEl = document.getElementById("quiz-summary");
const quizSummaryScoreEl = document.getElementById("quiz-summary-score");
const quizSummaryDetailsEl = document.getElementById("quiz-summary-details");
const quizIncorrectReviewEl = document.getElementById("quiz-incorrect-review");
const quizWeakConceptsEl = document.getElementById("quiz-weak-concepts");
const teachWeakTopicsButtonEl = document.getElementById("teach-weak-topics-btn");
const quizQuestionEl = document.getElementById("quiz-question");
const quizOptionsEl = document.getElementById("quiz-options");
const quizFeedbackEl = document.getElementById("quiz-feedback");
const quizRestartButtonEl = document.getElementById("quiz-restart-btn");
const revisionOutputEl = document.getElementById("revision-output");
const revisionMessageEl = document.getElementById("revision-message");
const revisionContentEl = document.getElementById("revision-content");
const generateRetestButtonEl = document.getElementById("generate-retest-btn");
const pdfFileEl = document.getElementById("pdf-file");
const extractPdfButtonEl = document.getElementById("extract-pdf-btn");
const pdfMessageEl = document.getElementById("pdf-message");

let isGeneratingNotes = false;
let isExtractingPdf = false;
let isExportingPdf = false;
let isGeneratingFlashcards = false;
let isGeneratingQuiz = false;
let isGeneratingRevision = false;
let isGeneratingRetest = false;
let latestNotesResponse = null;
let latestFlashcardsResponse = null;
let latestQuizResponse = null;
let originalQuizResponse = null;
let originalQuizQuestionStates = [];
let originalQuizResult = null;
let weakConcepts = [];
let incorrectQuestionContexts = [];
let latestRevisionResponse = null;
let latestRetestResponse = null;
let retestQuestionStates = [];
let retestResult = null;
let currentQuizMode = "original";
let flashcardIndex = 0;
let flashcardsAreFlipped = false;
let quizIndex = 0;
let quizQuestionStates = [];

function createEmptyQuizStates(response) {
  if (!response || !Array.isArray(response.questions)) {
    return [];
  }

  return response.questions.map(() => ({
    selectedAnswer: null,
    submittedAnswer: null,
    isCorrect: null,
    explanation: "",
    isSubmitted: false,
  }));
}

function getActiveQuizResponse() {
  return currentQuizMode === "retest" ? latestRetestResponse : originalQuizResponse;
}

function getActiveQuizStates() {
  return currentQuizMode === "retest" ? retestQuestionStates : originalQuizQuestionStates;
}

function setActiveQuizStates(states) {
  if (currentQuizMode === "retest") {
    retestQuestionStates = states;
  } else {
    originalQuizQuestionStates = states;
  }

  latestQuizResponse = getActiveQuizResponse();
  quizQuestionStates = states;
}

function syncActiveQuizState() {
  latestQuizResponse = getActiveQuizResponse();
  quizQuestionStates = getActiveQuizStates();
}

function normalizeForComparison(value) {
  return String(value || "").trim().toLowerCase();
}

function clearAdaptiveCycleState() {
  originalQuizResult = null;
  weakConcepts = [];
  incorrectQuestionContexts = [];
  latestRevisionResponse = null;
  latestRetestResponse = null;
  retestQuestionStates = [];
  retestResult = null;
  isGeneratingRevision = false;
  isGeneratingRetest = false;
  currentQuizMode = "original";

  quizIncorrectReviewEl.replaceChildren();
  quizWeakConceptsEl.replaceChildren();
  teachWeakTopicsButtonEl.hidden = true;
  teachWeakTopicsButtonEl.disabled = false;
  revisionOutputEl.hidden = true;
  revisionContentEl.replaceChildren();
  revisionMessageEl.textContent = "";
  revisionMessageEl.dataset.state = "idle";
  generateRetestButtonEl.hidden = true;
  generateRetestButtonEl.disabled = false;
}

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
  generateFlashcardsButtonEl.disabled = !hasGeneratedNotes || isGeneratingFlashcards;
  generateQuizButtonEl.disabled = !hasGeneratedNotes || isGeneratingQuiz;
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

function setFlashcardsMessage(state, message) {
  flashcardsMessageEl.dataset.state = state;
  flashcardsMessageEl.textContent = message;
}

function resetFlashcardView() {
  flashcardIndex = 0;
  flashcardsAreFlipped = false;
  flashcardBackEl.hidden = true;
  flashcardFlipButtonEl.textContent = "Show Answer";
  flashcardPrevButtonEl.disabled = true;
  flashcardNextButtonEl.disabled = false;
}

function renderFlashcardsResponse(response) {
  latestFlashcardsResponse = response;
  flashcardsOutputEl.hidden = false;

  if (!Array.isArray(response.flashcards) || response.flashcards.length === 0) {
    flashcardFrontEl.textContent = "No flashcards available.";
    flashcardBackEl.textContent = "";
    flashcardBackEl.hidden = true;
    flashcardProgressEl.textContent = "0 / 0";
    flashcardPrevButtonEl.disabled = true;
    flashcardNextButtonEl.disabled = true;
    flashcardFlipButtonEl.disabled = true;
    return;
  }

  flashcardFlipButtonEl.disabled = false;
  resetFlashcardView();
  updateFlashcardView();
}

function updateFlashcardView() {
  if (!latestFlashcardsResponse || !Array.isArray(latestFlashcardsResponse.flashcards)) {
    return;
  }

  const cards = latestFlashcardsResponse.flashcards;
  const total = cards.length;

  if (flashcardIndex < 0) {
    flashcardIndex = 0;
  }

  if (flashcardIndex >= total) {
    flashcardIndex = total - 1;
  }

  const card = cards[flashcardIndex];
  flashcardFrontEl.textContent = card.front;
  flashcardBackEl.textContent = flashcardsAreFlipped ? card.back : "";
  flashcardBackEl.hidden = !flashcardsAreFlipped;
  flashcardProgressEl.textContent = `${flashcardIndex + 1} / ${total}`;
  flashcardPrevButtonEl.disabled = flashcardIndex === 0;
  flashcardNextButtonEl.disabled = flashcardIndex >= total - 1;
  flashcardFlipButtonEl.textContent = flashcardsAreFlipped ? "Hide Answer" : "Show Answer";
}

function handleFlashcardFlip() {
  if (!latestFlashcardsResponse || !Array.isArray(latestFlashcardsResponse.flashcards)) {
    return;
  }

  flashcardsAreFlipped = !flashcardsAreFlipped;
  updateFlashcardView();
}

function handleFlashcardPrevious() {
  if (flashcardIndex > 0) {
    flashcardIndex -= 1;
    flashcardsAreFlipped = false;
    updateFlashcardView();
  }
}

function handleFlashcardNext() {
  if (!latestFlashcardsResponse || !Array.isArray(latestFlashcardsResponse.flashcards)) {
    return;
  }

  if (flashcardIndex < latestFlashcardsResponse.flashcards.length - 1) {
    flashcardIndex += 1;
    flashcardsAreFlipped = false;
    updateFlashcardView();
  }
}

async function handleGenerateFlashcards() {
  if (!latestNotesResponse || isGeneratingFlashcards) {
    return;
  }

  isGeneratingFlashcards = true;
  generateFlashcardsButtonEl.disabled = true;
  setFlashcardsMessage("loading", "Generating flashcards...");

  try {
    const response = await generateFlashcards(latestNotesResponse);
    renderFlashcardsResponse(response);
    setFlashcardsMessage("success", "Flashcards generated successfully.");
  } catch (error) {
    setFlashcardsMessage("error", error.message || "Could not generate flashcards.");
  } finally {
    isGeneratingFlashcards = false;
    updateNotesUtilityButtons();
  }
}

function setQuizMessage(state, message) {
  quizMessageEl.dataset.state = state;
  quizMessageEl.textContent = message;
}

function getQuizStats() {
  const total = latestQuizResponse && Array.isArray(latestQuizResponse.questions)
    ? latestQuizResponse.questions.length
    : 0;
  const submittedCount = quizQuestionStates.filter((state) => state?.isSubmitted).length;
  const correctCount = quizQuestionStates.filter((state) => state?.isSubmitted && state?.isCorrect).length;
  const incorrectCount = submittedCount - correctCount;

  return {
    total,
    submittedCount,
    correctCount,
    incorrectCount,
    percentage: total > 0 ? Math.round((correctCount / total) * 100) : 0,
  };
}

function extractWeakConcepts() {
  const weak = [];
  const seen = new Set();
  const incorrectContexts = [];

  const response = originalQuizResponse;
  const states = originalQuizQuestionStates;

  if (!response || !states) return { weak, incorrectContexts };

  for (let i = 0; i < response.questions.length; i++) {
    const q = response.questions[i];
    const s = states[i];

    if (q && s && s.isSubmitted && !s.isCorrect) {
      incorrectContexts.push({
        concept: q.concept,
        question: q.question,
        selected_answer: s.submittedAnswer,
        correct_answer: q.correct_answer,
        explanation: q.explanation
      });

      const key = (q.concept || "").trim().toLowerCase();
      if (key && !seen.has(key)) {
        seen.add(key);
        weak.push((q.concept || "").trim());
      }
    }
  }

  return { weak, incorrectContexts };
}

function updateQuizScoreDisplay() {
  const stats = getQuizStats();
  quizScoreEl.textContent = `Score: ${stats.correctCount} / ${stats.total}`;
}

function updateQuizSummary() {
  const stats = getQuizStats();
  const isCompleted = stats.total > 0 && stats.submittedCount === stats.total;

  quizSummaryEl.hidden = !isCompleted;

  if (!isCompleted) {
    return;
  }

  quizSummaryScoreEl.textContent = `You scored ${stats.correctCount} out of ${stats.total} (${stats.percentage}%).`;
  quizSummaryDetailsEl.textContent = `Answered: ${stats.submittedCount}/${stats.total} | Correct: ${stats.correctCount} | Incorrect: ${stats.incorrectCount}`;

  quizIncorrectReviewEl.replaceChildren();
  quizWeakConceptsEl.replaceChildren();

  const response = getActiveQuizResponse();
  const states = getActiveQuizStates();

  const incorrectQuestions = [];
  if (response && Array.isArray(response.questions) && Array.isArray(states)) {
    for (let i = 0; i < response.questions.length; i++) {
      const q = response.questions[i];
      const s = states[i];
      if (q && s && s.isSubmitted && !s.isCorrect) {
         incorrectQuestions.push({q, s});
      }
    }
  }

  if (incorrectQuestions.length > 0) {
    appendTextElement(quizIncorrectReviewEl, "h4", "Incorrect Answer Review");
    incorrectQuestions.forEach(({q, s}) => {
       const div = document.createElement("div");
       div.className = "incorrect-review-item";
       appendTextElement(div, "p", `Question: ${q.question}`);
       appendTextElement(div, "p", `Your Answer: ${s.submittedAnswer}`);
       appendTextElement(div, "p", `Correct Answer: ${q.correct_answer}`);
       appendTextElement(div, "p", `Explanation: ${q.explanation}`);
       appendTextElement(div, "p", `Concept: ${q.concept}`);
       quizIncorrectReviewEl.appendChild(div);
    });
  }

  if (currentQuizMode === "original") {
    const extracted = extractWeakConcepts();
    weakConcepts = extracted.weak;
    incorrectQuestionContexts = extracted.incorrectContexts;

    if (weakConcepts.length > 0) {
      appendTextElement(quizWeakConceptsEl, "h4", "Weak Concepts Identified");
      const ul = document.createElement("ul");
      weakConcepts.forEach(c => {
         appendTextElement(ul, "li", c);
      });
      quizWeakConceptsEl.appendChild(ul);

      teachWeakTopicsButtonEl.hidden = false;
    } else {
      appendTextElement(quizWeakConceptsEl, "p", "Great job! No weak concepts identified.");
      teachWeakTopicsButtonEl.hidden = true;
    }
  } else {
    teachWeakTopicsButtonEl.hidden = true;
    generateRetestButtonEl.hidden = true;
  }
}

function resetQuizView() {
  quizIndex = 0;
  quizFeedbackEl.textContent = "";
  quizFeedbackEl.dataset.state = "idle";
  quizSubmitButtonEl.disabled = true;
  quizPrevButtonEl.disabled = true;
  quizNextButtonEl.disabled = false;
  quizSummaryEl.hidden = true;
  quizSummaryScoreEl.textContent = "";
  quizSummaryDetailsEl.textContent = "";
  quizIncorrectReviewEl.replaceChildren();
  quizWeakConceptsEl.replaceChildren();
  updateQuizScoreDisplay();
  if (quizCardEl) quizCardEl.hidden = false;
  if (quizControlsEl) quizControlsEl.hidden = false;
}

function renderQuizResponse(response) {
  latestQuizResponse = response;
  quizOutputEl.hidden = false;
  document.getElementById("quiz-heading").textContent = currentQuizMode === "retest" ? "Retest" : "Quiz";

  if (!response || !Array.isArray(response.questions) || response.questions.length === 0) {
    quizQuestionStates = [];
    quizQuestionEl.textContent = "No quiz questions available.";
    quizOptionsEl.replaceChildren();
    quizProgressEl.textContent = "0 / 0";
    quizScoreEl.textContent = "Score: 0 / 0";
    quizSummaryEl.hidden = true;
    quizSummaryScoreEl.textContent = "";
    quizSummaryDetailsEl.textContent = "";
    quizPrevButtonEl.disabled = true;
    quizNextButtonEl.disabled = true;
    quizSubmitButtonEl.disabled = true;
    quizIncorrectReviewEl.replaceChildren();
    quizWeakConceptsEl.replaceChildren();
    teachWeakTopicsButtonEl.hidden = true;
    revisionOutputEl.hidden = true;
    generateRetestButtonEl.hidden = true;
    if (quizCardEl) quizCardEl.hidden = false;
    if (quizControlsEl) quizControlsEl.hidden = false;
    return;
  }

  resetQuizView();
  updateQuizView();
}

function updateQuizView() {
  if (!latestQuizResponse || !Array.isArray(latestQuizResponse.questions)) {
    return;
  }

  const questions = latestQuizResponse.questions;
  const total = questions.length;

  if (quizIndex < 0) {
    quizIndex = 0;
  }

  if (quizIndex >= total) {
    quizIndex = total - 1;
  }

  const stats = getQuizStats();
  const isCompleted = stats.total > 0 && stats.submittedCount === stats.total;

  // When the quiz is complete, hide the question UI and controls and show only the summary
  if (isCompleted) {
    if (quizCardEl) quizCardEl.hidden = true;
    if (quizControlsEl) quizControlsEl.hidden = true;
    updateQuizScoreDisplay();
    updateQuizSummary();
    return;
  }

  // Ensure question UI is visible when not complete
  if (quizCardEl) quizCardEl.hidden = false;
  if (quizControlsEl) quizControlsEl.hidden = false;

  const question = questions[quizIndex];
  const questionState = quizQuestionStates[quizIndex];
  quizQuestionEl.textContent = question.question;
  quizOptionsEl.replaceChildren();
  question.options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "quiz-option-btn";
    button.textContent = option;
    button.disabled = Boolean(questionState?.isSubmitted);

    if (questionState?.isSubmitted) {
      button.classList.toggle("selected", questionState.submittedAnswer === option);
      button.classList.toggle("correct", question.correct_answer === option);
      button.classList.toggle("incorrect", questionState.submittedAnswer === option && !questionState.isCorrect);
    } else {
      button.classList.toggle("selected", questionState?.selectedAnswer === option);
    }

    button.addEventListener("click", () => {
      if (questionState?.isSubmitted) {
        return;
      }

      questionState.selectedAnswer = option;
      Array.from(quizOptionsEl.children).forEach((child) => {
        child.classList.toggle("selected", child.textContent === option);
      });
      quizSubmitButtonEl.disabled = false;
      quizFeedbackEl.textContent = "";
      quizFeedbackEl.dataset.state = "idle";
    });
    quizOptionsEl.appendChild(button);
  });
  quizProgressEl.textContent = `${quizIndex + 1} / ${total}`;
  quizPrevButtonEl.disabled = quizIndex === 0;
  quizNextButtonEl.disabled = quizIndex >= total - 1;
  updateQuizScoreDisplay();

  if (questionState?.isSubmitted) {
    const explanation = questionState.explanation || "No explanation provided.";
    const feedback = questionState.isCorrect
      ? `Correct! ${explanation}`
      : `Incorrect. The correct answer is "${question.correct_answer}". ${explanation}`;
    quizFeedbackEl.dataset.state = questionState.isCorrect ? "success" : "error";
    quizFeedbackEl.textContent = feedback;
    quizSubmitButtonEl.disabled = true;
  } else {
    quizFeedbackEl.textContent = "";
    quizFeedbackEl.dataset.state = "idle";
    quizSubmitButtonEl.disabled = !questionState?.selectedAnswer;
  }

  updateQuizSummary();
}

function handleQuizPrevious() {
  if (quizIndex > 0) {
    quizIndex -= 1;
    updateQuizView();
  }
}

function handleQuizNext() {
  if (!latestQuizResponse || !Array.isArray(latestQuizResponse.questions)) {
    return;
  }

  if (quizIndex < latestQuizResponse.questions.length - 1) {
    quizIndex += 1;
    updateQuizView();
  }
}

function handleQuizSubmit() {
  if (!latestQuizResponse || !Array.isArray(latestQuizResponse.questions)) {
    return;
  }

  const question = latestQuizResponse.questions[quizIndex];
  const questionState = quizQuestionStates[quizIndex];
  if (!questionState || questionState.isSubmitted || !questionState.selectedAnswer) {
    return;
  }

  questionState.submittedAnswer = questionState.selectedAnswer;
  questionState.isCorrect = questionState.submittedAnswer === question.correct_answer;
  questionState.explanation = question.explanation;
  questionState.isSubmitted = true;
  updateQuizView();
}

function handleQuizRestart() {
  quizIndex = 0;

  if (currentQuizMode === "retest") {
    retestQuestionStates = createEmptyQuizStates(latestRetestResponse);
    syncActiveQuizState();
  } else {
    clearAdaptiveCycleState();
    currentQuizMode = "original";
    originalQuizQuestionStates = createEmptyQuizStates(originalQuizResponse);
    syncActiveQuizState();
  }

  document.getElementById("quiz-heading").textContent = currentQuizMode === "retest" ? "Retest" : "Quiz";

  resetQuizView();
  updateQuizView();
}

async function handleGenerateQuiz() {
  if (!latestNotesResponse || isGeneratingQuiz) {
    return;
  }

  isGeneratingQuiz = true;
  generateQuizButtonEl.disabled = true;
  setQuizMessage("loading", "Generating quiz...");

  try {
    const response = await generateQuiz(latestNotesResponse);

    if (!response || !Array.isArray(response.questions) || response.questions.length === 0) {
      throw new Error("Received empty or malformed quiz response.");
    }

    clearAdaptiveCycleState();
    originalQuizResponse = response;
    originalQuizQuestionStates = createEmptyQuizStates(response);
    syncActiveQuizState();
    renderQuizResponse(response);
    setQuizMessage("success", "Quiz generated successfully.");
  } catch (error) {
    setQuizMessage("error", error.message || "Could not generate quiz.");
  } finally {
    isGeneratingQuiz = false;
    generateQuizButtonEl.disabled = false;
    updateNotesUtilityButtons();
  }
}

async function handleTeachWeakTopics() {
  if (!latestNotesResponse || weakConcepts.length === 0 || isGeneratingRevision || latestRevisionResponse !== null) {
    return;
  }

  isGeneratingRevision = true;
  teachWeakTopicsButtonEl.disabled = true;
  revisionOutputEl.hidden = false;
  revisionMessageEl.dataset.state = "loading";
  revisionMessageEl.textContent = "Generating focused revision...";
  revisionContentEl.replaceChildren();
  generateRetestButtonEl.hidden = true;

  try {
    const payload = {
      notes_response: latestNotesResponse,
      weak_concepts: weakConcepts,
      incorrect_questions: incorrectQuestionContexts,
    };

    const response = await generateRevision(payload);
    latestRevisionResponse = response;

    revisionMessageEl.dataset.state = "success";
    revisionMessageEl.textContent = "Revision generated successfully.";

    response.concepts.forEach(conceptRev => {
       const sec = document.createElement("section");
       sec.className = "revision-concept-section";

       appendTextElement(sec, "h3", conceptRev.concept);
       appendTextElement(sec, "p", conceptRev.explanation);

       appendTextElement(sec, "h4", "Example");
       appendTextElement(sec, "p", conceptRev.example);

       if (conceptRev.analogy) {
         appendTextElement(sec, "h4", "Analogy");
         appendTextElement(sec, "p", conceptRev.analogy);
       }

       if (conceptRev.memory_trick) {
         appendTextElement(sec, "h4", "Memory Trick");
         appendTextElement(sec, "p", conceptRev.memory_trick);
       }

       appendList(sec, "Key Facts", conceptRev.key_facts);

       if (conceptRev.common_mistake) {
         appendTextElement(sec, "h4", "Common Mistake");
         appendTextElement(sec, "p", conceptRev.common_mistake);
       }

       revisionContentEl.appendChild(sec);
    });

    teachWeakTopicsButtonEl.hidden = true;
    generateRetestButtonEl.hidden = false;
  } catch (error) {
    revisionMessageEl.dataset.state = "error";
    revisionMessageEl.textContent = error.message || "Could not generate revision.";
    teachWeakTopicsButtonEl.disabled = false;
  } finally {
    isGeneratingRevision = false;
  }
}

async function handleGenerateRetest() {
  if (!latestNotesResponse || !latestRevisionResponse || isGeneratingRetest) {
    return;
  }

  isGeneratingRetest = true;
  generateRetestButtonEl.disabled = true;
  setQuizMessage("loading", "Generating retest...");

  try {
    const originalQuestions = originalQuizResponse.questions.map(q => q.question);

    const payload = {
      notes_response: latestNotesResponse,
      weak_concepts: weakConcepts,
      original_questions: originalQuestions
    };

    const response = await generateRetest(payload);

    if (!response || !Array.isArray(response.questions) || response.questions.length === 0) {
       throw new Error("Received empty or malformed retest response.");
    }

    latestRetestResponse = response;
    currentQuizMode = "retest";
    retestQuestionStates = createEmptyQuizStates(response);
    syncActiveQuizState();

    generateRetestButtonEl.hidden = true;
    renderQuizResponse(response);
    setQuizMessage("success", "Retest generated successfully.");

    quizOutputEl.scrollIntoView({ behavior: 'smooth' });

  } catch (error) {
    setQuizMessage("error", error.message || "Could not generate retest.");
    generateRetestButtonEl.disabled = false;
  } finally {
    isGeneratingRetest = false;
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
generateFlashcardsButtonEl.addEventListener("click", handleGenerateFlashcards);
generateQuizButtonEl.addEventListener("click", handleGenerateQuiz);
flashcardPrevButtonEl.addEventListener("click", handleFlashcardPrevious);
flashcardNextButtonEl.addEventListener("click", handleFlashcardNext);
flashcardFlipButtonEl.addEventListener("click", handleFlashcardFlip);
quizPrevButtonEl.addEventListener("click", handleQuizPrevious);
quizNextButtonEl.addEventListener("click", handleQuizNext);
quizSubmitButtonEl.addEventListener("click", handleQuizSubmit);
quizRestartButtonEl.addEventListener("click", handleQuizRestart);
teachWeakTopicsButtonEl.addEventListener("click", handleTeachWeakTopics);
generateRetestButtonEl.addEventListener("click", handleGenerateRetest);
updateNotesUtilityButtons();
