const fs = require('fs');
let lines = fs.readFileSync('frontend/js/main.js', 'utf8').split('\n');

function replaceLines(startQuery, endQuery, replacement) {
  const startIdx = lines.findIndex(l => l.includes(startQuery));
  if (startIdx === -1) throw new Error("Not found: " + startQuery);
  const endIdx = lines.findIndex((l, i) => i > startIdx && l.includes(endQuery));
  if (endIdx === -1) throw new Error("Not found: " + endQuery);
  lines.splice(startIdx, endIdx - startIdx + 1, replacement);
}

// 1. clearAdaptiveCycleState
replaceLines('function clearAdaptiveCycleState() {', 'generateRetestButtonEl.disabled = false;\n}', `function clearAdaptiveCycleState() {
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
  revisionContentEl.replaceChildren();
  revisionMessageEl.textContent = "";
  revisionMessageEl.dataset.state = "idle";
  generateRetestButtonEl.hidden = true;
  generateRetestButtonEl.disabled = false;
}`);

// 2. renderNotesResponse
replaceLines('function renderNotesResponse(response) {', 'notesOutputEl.hidden = false;\n}', `function renderNotesResponse(response) {
  notesMetaEl.replaceChildren();
  notesContentEl.replaceChildren();
  const actions = document.getElementById("notes-actions");

  if (!response) {
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
    return;
  }

  if (actions) actions.hidden = false;

  const notes = response.notes;
  const meta = document.createElement("p");
  meta.textContent = \`Estimated reading time: \${response.estimated_reading_time_minutes} minute(s)\`;
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
}`);

// 3. renderFlashcardsResponse
replaceLines('function renderFlashcardsResponse(response) {', 'updateFlashcardView();\n}', `function renderFlashcardsResponse(response) {
  latestFlashcardsResponse = response;
  const controls = document.getElementById("flashcard-controls");
  const existingBtn = document.getElementById("empty-flashcards-btn");
  if (existingBtn) existingBtn.remove();

  if (!response || !Array.isArray(response.flashcards) || response.flashcards.length === 0) {
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
    return;
  }

  if (controls) controls.hidden = false;
  flashcardFlipButtonEl.hidden = false;
  flashcardFlipButtonEl.disabled = false;
  resetFlashcardView();
  updateFlashcardView();
}`);

// 4. renderQuizResponse
replaceLines('function renderQuizResponse(response) {', 'updateQuizView();\n}', `function renderQuizResponse(response) {
  latestQuizResponse = response;
  document.getElementById("quiz-heading").textContent = currentQuizMode === "retest" ? "Retest: Weak Concepts" : "Original Quiz";

  const existingBtn = document.getElementById("empty-quiz-btn");
  if (existingBtn) existingBtn.remove();

  if (!response || !Array.isArray(response.questions) || response.questions.length === 0) {
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
    return;
  }

  if (quizControlsEl) quizControlsEl.hidden = false;
  quizSubmitButtonEl.hidden = false;
  quizFeedbackEl.hidden = false;

  resetQuizView();
  updateQuizView();
}`);

// 5. handleTeachWeakTopics + renderRevisionResponse
replaceLines('async function handleTeachWeakTopics() {', 'generateRetestButtonEl.hidden = false;\n  } catch (error) {', `function renderRevisionResponse(response) {
  latestRevisionResponse = response;
  revisionContentEl.replaceChildren();

  if (!response) {
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
    return;
  }

  const revision = response.concepts;
  if (Array.isArray(revision)) {
    revision.forEach(conceptRev => {
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
       if (Array.isArray(conceptRev.key_facts)) {
         appendList(sec, "Key Facts", conceptRev.key_facts);
       }
       if (conceptRev.common_misconception) {
         appendTextElement(sec, "h4", "Common Misconception");
         appendTextElement(sec, "p", conceptRev.common_misconception);
       }
       if (conceptRev.common_mistake) {
         appendTextElement(sec, "h4", "Common Mistake");
         appendTextElement(sec, "p", conceptRev.common_mistake);
       }
       revisionContentEl.appendChild(sec);
    });
  }
  generateRetestButtonEl.hidden = false;
}

async function handleTeachWeakTopics() {
  if (!latestNotesResponse || weakConcepts.length === 0 || isGeneratingRevision || latestRevisionResponse !== null) {
    return;
  }

  isGeneratingRevision = true;
  teachWeakTopicsButtonEl.disabled = true;
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
    revisionMessageEl.dataset.state = "success";
    revisionMessageEl.textContent = "Revision generated successfully.";
    
    renderRevisionResponse(response);
    if (learningWorkspaceEl) learningWorkspaceEl.hidden = false;
    switchWorkspaceTab('revision');
  } catch (error) {`);

// 6. updateQuizScoreDisplay
replaceLines('function updateQuizScoreDisplay() {', 'quizScoreEl.textContent = `Score: ${stats.correctCount} / ${stats.total}`;\n}', `function updateQuizScoreDisplay() {
  const stats = getQuizStats();
  if (stats.submittedCount === stats.total && stats.total > 0) {
    quizScoreEl.textContent = "";
  } else {
    quizScoreEl.innerHTML = \`Answered: \${stats.submittedCount}/\${stats.total}<br>Correct: \${stats.correctCount}<br>Wrong: \${stats.incorrectCount}<br>Remaining: \${stats.total - stats.submittedCount}\`;
  }
}`);

// 7. updateQuizSummary
replaceLines('function updateQuizSummary() {', 'teachWeakTopicsButtonEl.hidden = true;\n  }\n}', `function updateQuizSummary() {
  const stats = getQuizStats();
  const isCompleted = stats.total > 0 && stats.submittedCount === stats.total;

  quizSummaryEl.hidden = !isCompleted;

  if (!isCompleted) {
    return;
  }

  quizSummaryScoreEl.innerHTML = \`<h2 style="text-align: center;">Final Score</h2>
<p style="font-size: 2em; text-align: center; margin: 10px 0;">\${stats.correctCount} / \${stats.total}</p>
<p style="font-size: 1.5em; text-align: center; font-weight: bold; margin: 0;">\${stats.percentage}%</p>\`;
  quizSummaryDetailsEl.innerHTML = \`<p style="text-align: center;">Correct: \${stats.correctCount} | Wrong: \${stats.incorrectCount}</p>\`;

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
       appendTextElement(div, "p", \`Question: \${q.question}\`);
       appendTextElement(div, "p", \`Your Answer: \${s.submittedAnswer}\`);
       appendTextElement(div, "p", \`Correct Answer: \${q.correct_answer}\`);
       appendTextElement(div, "p", \`Explanation: \${q.explanation}\`);
       appendTextElement(div, "p", \`Concept: \${q.concept}\`);
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
}`);

// Add initialization code
lines.push(`
document.addEventListener("DOMContentLoaded", () => {
  renderNotesResponse(null);
  renderFlashcardsResponse(null);
  renderQuizResponse(null);
  renderRevisionResponse(null);
});

// Keyboard Navigation
const tabButtons = [
  document.getElementById("workspace-tab-notes"),
  document.getElementById("workspace-tab-flashcards"),
  document.getElementById("workspace-tab-quiz"),
  document.getElementById("workspace-tab-revision")
];

tabButtons.forEach((btn, index) => {
  if (!btn) return;
  btn.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      tabButtons[(index + 1) % tabButtons.length].focus();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      tabButtons[(index - 1 + tabButtons.length) % tabButtons.length].focus();
    } else if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      btn.click();
    }
  });
});

// Quiz First Unanswered logic
const quizFirstUnansweredBtn = document.getElementById("quiz-first-unanswered-btn");
if (quizFirstUnansweredBtn) {
  quizFirstUnansweredBtn.addEventListener("click", () => {
    const states = getActiveQuizStates();
    if (!states) return;
    const idx = states.findIndex(s => !s.isSubmitted);
    if (idx !== -1) {
      quizIndex = idx;
      updateQuizView();
    }
  });
}
`);

// Add automatic routing for handleGenerateNotes, Flashcards, Quiz, Retest
const text = lines.join('\\n');
let modified = text.replace(/setNotesMessage\\("success", "Notes generated successfully."\\);/g, \`setNotesMessage("success", "Notes generated successfully.");\\n    if (learningWorkspaceEl) learningWorkspaceEl.hidden = false;\\n    switchWorkspaceTab('notes');\`);
modified = modified.replace(/setFlashcardsMessage\\("success", "Flashcards generated successfully."\\);/g, \`setFlashcardsMessage("success", "Flashcards generated successfully.");\\n    if (learningWorkspaceEl) learningWorkspaceEl.hidden = false;\\n    switchWorkspaceTab('flashcards');\`);
modified = modified.replace(/quizMessageEl\\.dataset\\.state = "success";\\n\\s*quizMessageEl\\.textContent = "Quiz generated successfully\\.";/g, \`quizMessageEl.dataset.state = "success";\\n    quizMessageEl.textContent = "Quiz generated successfully.";\\n    if (learningWorkspaceEl) learningWorkspaceEl.hidden = false;\\n    switchWorkspaceTab('quiz');\`);
modified = modified.replace(/quizMessageEl\\.dataset\\.state = "success";\\n\\s*quizMessageEl\\.textContent = "Retest generated successfully\\.";/g, \`quizMessageEl.dataset.state = "success";\\n    quizMessageEl.textContent = "Retest generated successfully.";\\n    if (learningWorkspaceEl) learningWorkspaceEl.hidden = false;\\n    switchWorkspaceTab('quiz');\`);
modified = modified.replace(/if \\(quizControlsEl\\) quizControlsEl\\.hidden = false;/g, \`if (quizControlsEl) quizControlsEl.hidden = false;
  if (typeof quizFirstUnansweredBtn !== 'undefined' && quizFirstUnansweredBtn) {
    const stats = getQuizStats();
    if (stats.submittedCount < stats.total && stats.submittedCount > 0) {
      quizFirstUnansweredBtn.hidden = false;
    } else {
      quizFirstUnansweredBtn.hidden = true;
    }
  }\`);

fs.writeFileSync('frontend/js/main.js', modified);
