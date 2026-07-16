const fs = require('fs'); let js = fs.readFileSync('frontend/js/main.js', 'utf8');

js = js.replace(/function updateQuizScoreDisplay\(\) \{[\s\S]*?\}\n/m, `function updateQuizScoreDisplay() {
  const stats = getQuizStats();
  if (stats.submittedCount === stats.total && stats.total > 0) {
    quizScoreEl.textContent = "";
  } else {
    quizScoreEl.innerHTML = \`Answered: \${stats.submittedCount}/\${stats.total}<br>Correct: \${stats.correctCount}<br>Wrong: \${stats.incorrectCount}<br>Remaining: \${stats.total - stats.submittedCount}\`;
  }
}
`);

js = js.replace(/quizSummaryScoreEl\.textContent = [\s\S]*?;/m, `quizSummaryScoreEl.innerHTML = \`
    <h2 style="text-align: center;">Final Score</h2>
    <p style="font-size: 2em; text-align: center; margin: 10px 0;">\${stats.correctCount} / \${stats.total}</p>
    <p style="font-size: 1.5em; text-align: center; font-weight: bold; margin: 0;">\${stats.percentage}%</p>
  \`;`);

js = js.replace(/quizSummaryDetailsEl\.textContent = [\s\S]*?;/m, `quizSummaryDetailsEl.innerHTML = \`<p style="text-align: center;">Correct: \${stats.correctCount} | Wrong: \${stats.incorrectCount}</p>\`;`);

fs.writeFileSync('frontend/js/main.js', js);
