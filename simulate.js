const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('frontend/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });

// Mock API functions
dom.window.generateNotes = async () => ({ notes: { title: "Test", summary: "Test", table_of_contents: [], sections: [] } });
dom.window.generateFlashcards = async () => ({ flashcards: [{front: "Q", back: "A"}] });
dom.window.generateQuiz = async () => ({ questions: [{question: "Q", options: ["A", "B"], correct_answer: "A"}] });

const script = fs.readFileSync('frontend/js/main.js', 'utf8');
const scriptEl = dom.window.document.createElement("script");
scriptEl.textContent = script;
dom.window.document.body.appendChild(scriptEl);

async function runTest() {
  const doc = dom.window.document;
  
  // 1. Generate Notes
  doc.getElementById("source-text").value = "A".repeat(60);
  doc.getElementById("notes-form").dispatchEvent(new dom.window.Event("submit"));
  await new Promise(r => setTimeout(r, 100)); // wait for async
  
  console.log("After Notes:");
  console.log("Notes panel hidden:", doc.getElementById("workspace-panel-notes").hasAttribute("hidden"));
  console.log("Notes output hidden:", doc.getElementById("notes-output").hidden);
  
  // 2. Generate Flashcards
  doc.getElementById("generate-flashcards-btn").click();
  await new Promise(r => setTimeout(r, 100));
  
  console.log("After Flashcards:");
  console.log("Flashcards panel hidden:", doc.getElementById("workspace-panel-flashcards").hasAttribute("hidden"));
  console.log("Notes panel hidden:", doc.getElementById("workspace-panel-notes").hasAttribute("hidden"));
  
  // 3. Generate Quiz
  doc.getElementById("generate-quiz-btn").click();
  await new Promise(r => setTimeout(r, 100));
  
  console.log("After Quiz:");
  console.log("Quiz panel hidden:", doc.getElementById("workspace-panel-quiz").hasAttribute("hidden"));
  console.log("Notes panel hidden:", doc.getElementById("workspace-panel-notes").hasAttribute("hidden"));
  
  // 4. Click Notes
  doc.getElementById("workspace-tab-notes").click();
  
  console.log("After Clicking Notes:");
  console.log("Notes panel hidden:", doc.getElementById("workspace-panel-notes").hasAttribute("hidden"));
  console.log("Quiz panel hidden:", doc.getElementById("workspace-panel-quiz").hasAttribute("hidden"));
  console.log("Notes output hidden:", doc.getElementById("notes-output").hidden);
}

runTest().catch(console.error);
