const fs = require('fs');

let mainJs = fs.readFileSync('frontend/js/main.js', 'utf8');

const replacements = [
  // Notes
  {
    find: /function renderNotesResponse\(response\) \{[\s\S]*?if \(!response\) \{[\s\S]*?\}\n\n  if \(actions\) actions\.hidden = false;/m,
    replace: `function renderNotesEmptyState() {
  notesMetaEl.replaceChildren();
  notesContentEl.replaceChildren();
  const actions = document.getElementById("notes-actions");
  if (actions) actions.hidden = true;
  
  appendTextElement(notesContentEl, "h3", "No notes generated yet.");
  appendTextElement(notesContentEl, "p", "Generate AI notes from your uploaded PDF or pasted text.");
  
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = "Generate Notes";
  btn.className = "empty-state-btn";
  btn.style.marginTop = "20px";
  btn.addEventListener("click", () => {
    if (generateNotesButtonEl) generateNotesButtonEl.click();
  });
  notesContentEl.appendChild(btn);
}

function renderNotesResponse(response) {
  notesMetaEl.replaceChildren();
  notesContentEl.replaceChildren();
  const actions = document.getElementById("notes-actions");
  if (actions) actions.hidden = false;`
  },
  
  // Flashcards
  {
    find: /function renderFlashcardsResponse\(response\) \{[\s\S]*?if \(!response \|\| !Array\.isArray\(response\.flashcards\) \|\| response\.flashcards\.length === 0\) \{[\s\S]*?return;\n  \}\n\n  if \(controls\) controls\.hidden = false;/m,
    replace: `function renderFlashcardsEmptyState() {
  const controls = document.getElementById("flashcard-controls");
  const existingBtn = document.getElementById("empty-flashcards-btn");
  if (existingBtn) existingBtn.remove();

  if (controls) controls.hidden = true;
  flashcardFlipButtonEl.hidden = true;
  flashcardFrontEl.textContent = "No flashcards generated yet.";
  flashcardBackEl.textContent = "";
  flashcardBackEl.hidden = true;
  
  const btn = document.createElement("button");
  btn.id = "empty-flashcards-btn";
  btn.type = "button";
  btn.textContent = "Generate Flashcards";
  btn.style.marginTop = "20px";
  btn.addEventListener("click", () => {
    if (generateFlashcardsButtonEl) generateFlashcardsButtonEl.click();
  });
  document.getElementById("flashcard-card").appendChild(btn);
}

function renderFlashcardsResponse(response) {
  latestFlashcardsResponse = response;
  const controls = document.getElementById("flashcard-controls");
  const existingBtn = document.getElementById("empty-flashcards-btn");
  if (existingBtn) existingBtn.remove();
  
  if (controls) controls.hidden = false;`
  },

  // Quiz
  {
    find: /function renderQuizResponse\(response\) \{[\s\S]*?if \(!response \|\| !Array\.isArray\(response\.questions\) \|\| response\.questions\.length === 0\) \{[\s\S]*?return;\n  \}\n\n  if \(quizControlsEl\) quizControlsEl\.hidden = false;/m,
    replace: `function renderQuizEmptyState() {
  document.getElementById("quiz-heading").textContent = "Quiz";
  const existingBtn = document.getElementById("empty-quiz-btn");
  if (existingBtn) existingBtn.remove();

  quizQuestionStates = [];
  if (quizControlsEl) quizControlsEl.hidden = true;
  if (quizCardEl) quizCardEl.hidden = false;
  
  quizQuestionEl.textContent = "No quiz generated yet.";
  quizOptionsEl.replaceChildren();
  quizProgressEl.textContent = "0 / 0";
  quizScoreEl.textContent = "";
  quizSummaryEl.hidden = true;
  quizSummaryScoreEl.textContent = "";
  quizSummaryDetailsEl.textContent = "";
  quizSubmitButtonEl.hidden = true;
  quizFeedbackEl.hidden = true;
  quizIncorrectReviewEl.replaceChildren();
  quizWeakConceptsEl.replaceChildren();
  teachWeakTopicsButtonEl.hidden = true;
  generateRetestButtonEl.hidden = true;

  const btn = document.createElement("button");
  btn.id = "empty-quiz-btn";
  btn.type = "button";
  btn.textContent = "Generate Quiz";
  btn.style.marginTop = "20px";
  btn.addEventListener("click", () => {
     if (generateQuizButtonEl) generateQuizButtonEl.click();
  });
  if (quizCardEl) quizCardEl.appendChild(btn);
}

function renderQuizResponse(response) {
  latestQuizResponse = response;
  document.getElementById("quiz-heading").textContent = currentQuizMode === "retest" ? "Retest: Weak Concepts" : "Original Quiz";

  const existingBtn = document.getElementById("empty-quiz-btn");
  if (existingBtn) existingBtn.remove();

  if (quizControlsEl) quizControlsEl.hidden = false;`
  },

  // Revision
  {
    find: /function renderRevisionResponse\(response\) \{[\s\S]*?if \(!response\) \{[\s\S]*?return;\n  \}\n\n  const revision = response\.concepts;/m,
    replace: `function renderRevisionEmptyState() {
  revisionContentEl.replaceChildren();
  const stats = getQuizStats();
  if (stats.total === 0 || stats.submittedCount < stats.total) {
    appendTextElement(revisionContentEl, "h3", "You haven't completed a quiz yet.");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Start Quiz";
    btn.style.marginTop = "20px";
    btn.addEventListener("click", () => {
       switchWorkspaceTab("quiz");
       if (!originalQuizResponse) {
           if (generateQuizButtonEl) generateQuizButtonEl.click();
       }
    });
    revisionContentEl.appendChild(btn);
  } else {
    appendTextElement(revisionContentEl, "h3", "Quiz completed!");
    appendTextElement(revisionContentEl, "p", "Click 'Teach Me My Weak Topics' in the Quiz tab to generate focused revision.");
  }
  generateRetestButtonEl.hidden = true;
}

function renderRevisionResponse(response) {
  latestRevisionResponse = response;
  revisionContentEl.replaceChildren();
  
  const revision = response.concepts;`
  },

  // DOMContentLoaded
  {
    find: /document\.addEventListener\("DOMContentLoaded", \(\) => \{\n  renderNotesResponse\(null\);\n  renderFlashcardsResponse\(null\);\n  renderQuizResponse\(null\);\n  renderRevisionResponse\(null\);\n\}\);/,
    replace: `document.addEventListener("DOMContentLoaded", () => {
  renderNotesEmptyState();
  renderFlashcardsEmptyState();
  renderQuizEmptyState();
  renderRevisionEmptyState();
});`
  },
  
  // switchWorkspaceTab scroll
  {
    find: /function switchWorkspaceTab\(tabName\) \{\n  const tabs = \{[\s\S]*?\}\);\n\}/m,
    replace: `function switchWorkspaceTab(tabName) {
  const tabs = {
    notes: { btn: tabNotesBtn, panel: panelNotesEl },
    flashcards: { btn: tabFlashcardsBtn, panel: panelFlashcardsEl },
    quiz: { btn: tabQuizBtn, panel: panelQuizEl },
    revision: { btn: tabRevisionBtn, panel: panelRevisionEl }
  };

  if (!tabs[tabName]) return;

  activeWorkspaceTab = tabName;

  Object.keys(tabs).forEach(key => {
    const isActive = key === tabName;
    const { btn, panel } = tabs[key];

    if (btn && panel) {
      btn.setAttribute("aria-selected", isActive ? "true" : "false");
      if (isActive) {
        panel.removeAttribute("hidden");
        // Maintain smooth UX by ensuring the user starts at the top of the newly shown panel
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        panel.setAttribute("hidden", "");
      }
    }
  });
}`
  }
];

let ok = true;
for (const r of replacements) {
  if (!r.find.test(mainJs)) {
    console.error("Could not find match for:\n", r.find);
    ok = false;
  } else {
    mainJs = mainJs.replace(r.find, r.replace);
  }
}

if (ok) {
  fs.writeFileSync('frontend/js/main.js', mainJs);
  console.log("Refactored main.js successfully.");
}
