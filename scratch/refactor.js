const fs = require('fs'); let js = fs.readFileSync('frontend/js/main.js', 'utf8');

js = js.replace(/function renderNotesResponse\(response\) \{[\s\S]*?notesOutputEl\.hidden = false;\n\}/m, `function renderNotesResponse(response) {
  notesMetaEl.replaceChildren();
  notesContentEl.replaceChildren();
  const actions = document.getElementById('notes-actions');

  if (!response) {
    actions.hidden = true;
    const emptyState = document.createElement('div');
    emptyState.className = 'empty-state';
    
    const h = document.createElement('h3');
    h.textContent = 'No notes generated yet.';
    emptyState.appendChild(h);
    
    const p = document.createElement('p');
    p.textContent = 'Generate AI notes from your uploaded PDF or pasted text.';
    emptyState.appendChild(p);
    
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = 'Generate Notes';
    btn.className = 'empty-state-btn';
    btn.addEventListener('click', () => {
      generateNotesButtonEl.click();
    });
    emptyState.appendChild(btn);
    notesContentEl.appendChild(emptyState);
    return;
  }

  actions.hidden = false;
  const notes = response.notes;
  const meta = document.createElement('p');
  meta.textContent = \`Estimated reading time: \${response.estimated_reading_time_minutes} minute(s)\`;
  notesMetaEl.appendChild(meta);

  appendTextElement(notesContentEl, 'h3', notes.title);
  appendList(notesContentEl, 'Table of Contents', notes.table_of_contents);

  if (Array.isArray(notes.sections)) {
    notes.sections.forEach((section) => {
      const sectionEl = document.createElement('section');
      sectionEl.className = 'generated-section';
      appendTextElement(sectionEl, 'h3', section.heading);
      appendTextElement(sectionEl, 'p', section.content);
      appendList(sectionEl, 'Key Points', section.key_points);
      appendDefinitions(sectionEl, section.definitions);
      appendList(sectionEl, 'Examples', section.examples);
      appendList(sectionEl, 'Memory Tricks', section.memory_tricks);
      appendList(sectionEl, 'Common Mistakes', section.common_mistakes);
      notesContentEl.appendChild(sectionEl);
    });
  }

  appendTextElement(notesContentEl, 'h3', 'Summary');
  appendTextElement(notesContentEl, 'p', notes.summary);
  appendList(notesContentEl, 'Key Takeaways', notes.key_takeaways);
  appendTextElement(notesContentEl, 'h3', 'One-Minute Revision');
  appendTextElement(notesContentEl, 'p', notes.one_minute_revision);
}`);

js = js.replace(/function renderFlashcardsResponse\(response\) \{[\s\S]*?updateFlashcardView\(\);\n\}/m, `function renderFlashcardsResponse(response) {
  latestFlashcardsResponse = response;
  const controls = document.getElementById('flashcard-controls');

  if (!response || !Array.isArray(response.flashcards) || response.flashcards.length === 0) {
    controls.hidden = true;
    flashcardFlipButtonEl.hidden = true;
    flashcardFrontEl.textContent = 'No flashcards generated yet.';
    flashcardBackEl.textContent = '';
    flashcardBackEl.hidden = true;
    
    const existingBtn = document.getElementById('empty-flashcards-btn');
    if (existingBtn) existingBtn.remove();
    
    const btn = document.createElement('button');
    btn.id = 'empty-flashcards-btn';
    btn.type = 'button';
    btn.textContent = 'Generate Flashcards';
    btn.style.marginTop = '20px';
    btn.addEventListener('click', () => {
      generateFlashcardsButtonEl.click();
    });
    document.getElementById('flashcard-card').appendChild(btn);
    return;
  }
  
  const existingBtn = document.getElementById('empty-flashcards-btn');
  if (existingBtn) existingBtn.remove();

  controls.hidden = false;
  flashcardFlipButtonEl.hidden = false;
  flashcardFlipButtonEl.disabled = false;
  resetFlashcardView();
  updateFlashcardView();
}`);

js = js.replace(/function renderQuizResponse\(response\) \{[\s\S]*?updateQuizView\(\);\n\}/m, `function renderQuizResponse(response) {
  latestQuizResponse = response;
  document.getElementById('quiz-heading').textContent = currentQuizMode === 'retest' ? 'Retest' : 'Quiz';

  const existingBtn = document.getElementById('empty-quiz-btn');
  if (existingBtn) existingBtn.remove();

  if (!response || !Array.isArray(response.questions) || response.questions.length === 0) {
    quizQuestionStates = [];
    if (quizControlsEl) quizControlsEl.hidden = true;
    if (quizCardEl) quizCardEl.hidden = false;
    
    quizQuestionEl.textContent = 'No quiz generated yet.';
    quizOptionsEl.replaceChildren();
    quizProgressEl.textContent = '0 / 0';
    quizScoreEl.textContent = '';
    quizSummaryEl.hidden = true;
    quizSummaryScoreEl.textContent = '';
    quizSummaryDetailsEl.textContent = '';
    quizSubmitButtonEl.hidden = true;
    quizFeedbackEl.hidden = true;
    quizIncorrectReviewEl.replaceChildren();
    quizWeakConceptsEl.replaceChildren();
    teachWeakTopicsButtonEl.hidden = true;
    generateRetestButtonEl.hidden = true;

    const btn = document.createElement('button');
    btn.id = 'empty-quiz-btn';
    btn.type = 'button';
    btn.textContent = 'Generate Quiz';
    btn.style.marginTop = '20px';
    btn.addEventListener('click', () => {
       generateQuizButtonEl.click();
    });
    quizCardEl.appendChild(btn);
    return;
  }

  if (quizControlsEl) quizControlsEl.hidden = false;
  quizSubmitButtonEl.hidden = false;
  quizFeedbackEl.hidden = false;

  resetQuizView();
  updateQuizView();
}`);

const renderRevString = `
function renderRevisionResponse(response) {
  latestRevisionResponse = response;
  revisionContentEl.replaceChildren();

  if (!response) {
    const stats = getQuizStats();
    if (stats.total === 0 || stats.submittedCount < stats.total) {
      appendTextElement(revisionContentEl, 'h3', "You haven't completed a quiz yet.");
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = 'Start Quiz';
      btn.style.marginTop = '20px';
      btn.addEventListener('click', () => {
         switchWorkspaceTab('quiz');
         if (!originalQuizResponse) {
             generateQuizButtonEl.click();
         }
      });
      revisionContentEl.appendChild(btn);
    } else {
      appendTextElement(revisionContentEl, 'h3', 'Quiz completed!');
      appendTextElement(revisionContentEl, 'p', "Click 'Teach Me My Weak Topics' in the Quiz tab to generate focused revision.");
    }
    generateRetestButtonEl.hidden = true;
    return;
  }

  const revision = response.concepts;
  if (Array.isArray(revision)) {
    revision.forEach(conceptRev => {
       const sec = document.createElement('section');
       sec.className = 'revision-concept-section';
       appendTextElement(sec, 'h3', conceptRev.concept);
       appendTextElement(sec, 'p', conceptRev.explanation);
       appendTextElement(sec, 'h4', 'Example');
       appendTextElement(sec, 'p', conceptRev.example);
       if (conceptRev.analogy) {
         appendTextElement(sec, 'h4', 'Analogy');
         appendTextElement(sec, 'p', conceptRev.analogy);
       }
       if (conceptRev.memory_trick) {
         appendTextElement(sec, 'h4', 'Memory Trick');
         appendTextElement(sec, 'p', conceptRev.memory_trick);
       }
       if (Array.isArray(conceptRev.key_facts)) {
         appendList(sec, 'Key Facts', conceptRev.key_facts);
       }
       if (conceptRev.common_misconception) {
         appendTextElement(sec, 'h4', 'Common Misconception');
         appendTextElement(sec, 'p', conceptRev.common_misconception);
       }
       revisionContentEl.appendChild(sec);
    });
  }
  generateRetestButtonEl.hidden = false;
}
`;

js = js.replace(/async function handleTeachWeakTopics\(\) \{[\s\S]*?catch \(error\)/m, `${renderRevString}\n\nasync function handleTeachWeakTopics() {
    if (!latestNotesResponse || weakConcepts.length === 0 || isGeneratingRevision || latestRevisionResponse !== null) {
      return;
    }
  
    isGeneratingRevision = true;
    teachWeakTopicsButtonEl.disabled = true;
    
    revisionMessageEl.dataset.state = 'loading';
    revisionMessageEl.textContent = 'Generating focused revision...';
    revisionContentEl.replaceChildren();
    generateRetestButtonEl.hidden = true;
  
    try {
      const payload = {
        notes_response: latestNotesResponse,
        weak_concepts: weakConcepts,
        incorrect_questions: incorrectQuestionContexts,
      };
  
      const response = await generateRevision(payload);
      
      revisionMessageEl.dataset.state = 'success';
      revisionMessageEl.textContent = 'Revision generated successfully.';
      
      renderRevisionResponse(response);
      switchWorkspaceTab('revision');

    } catch (error)`);

js = js.replace(/document\.addEventListener\(\"DOMContentLoaded\", \(\) => \{/, `document.addEventListener("DOMContentLoaded", () => {
  renderNotesResponse(null);
  renderFlashcardsResponse(null);
  renderQuizResponse(null);
  renderRevisionResponse(null);`);

fs.writeFileSync('frontend/js/main.js', js);
console.log('done');
