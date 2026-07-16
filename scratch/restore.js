const fs = require('fs'); let js = fs.readFileSync('frontend/js/main.js', 'utf8');

// Add automatic routing
js = js.replace(/setNotesMessage\("success", "Notes generated successfully."\);/g, `setNotesMessage("success", "Notes generated successfully.");\n    learningWorkspaceEl.hidden = false;\n    switchWorkspaceTab('notes');`);
js = js.replace(/setFlashcardsMessage\("success", "Flashcards generated successfully."\);/g, `setFlashcardsMessage("success", "Flashcards generated successfully.");\n    learningWorkspaceEl.hidden = false;\n    switchWorkspaceTab('flashcards');`);

js = js.replace(/quizMessageEl\.dataset\.state = "success";\n\s*quizMessageEl\.textContent = "Quiz generated successfully\.";\n\s*renderQuizResponse\(response\);/g, `quizMessageEl.dataset.state = "success";\n    quizMessageEl.textContent = "Quiz generated successfully.";\n    renderQuizResponse(response);\n    learningWorkspaceEl.hidden = false;\n    switchWorkspaceTab('quiz');`);

js = js.replace(/renderRevisionResponse\(response\);\n\s*switchWorkspaceTab\('revision'\);/g, `renderRevisionResponse(response);\n      learningWorkspaceEl.hidden = false;\n      switchWorkspaceTab('revision');`);

// Retest routing (assuming there is a handleGenerateRetest)
js = js.replace(/quizMessageEl\.dataset\.state = "success";\n\s*quizMessageEl\.textContent = "Retest generated successfully\.";\n\s*renderQuizResponse\(response\);/g, `quizMessageEl.dataset.state = "success";\n    quizMessageEl.textContent = "Retest generated successfully.";\n    renderQuizResponse(response);\n    learningWorkspaceEl.hidden = false;\n    switchWorkspaceTab('quiz');`);


// Quiz Mode Indicator
js = js.replace(/document\.getElementById\('quiz-heading'\)\.textContent = currentQuizMode === 'retest' \? 'Retest' : 'Quiz';/g, `document.getElementById('quiz-heading').textContent = currentQuizMode === 'retest' ? 'Retest: Weak Concepts' : 'Original Quiz';`);


// Keyboard Navigation and Unanswered Button
js += `
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
`;

// Update updateQuizView to show/hide the unanswered button
js = js.replace(/if \(quizControlsEl\) quizControlsEl\.hidden = false;/g, `if (quizControlsEl) quizControlsEl.hidden = false;
  if (quizFirstUnansweredBtn) {
    if (stats.submittedCount < stats.total && stats.submittedCount > 0) {
      quizFirstUnansweredBtn.hidden = false;
    } else {
      quizFirstUnansweredBtn.hidden = true;
    }
  }`);

fs.writeFileSync('frontend/js/main.js', js);
