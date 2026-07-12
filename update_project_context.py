from pathlib import Path

path = Path("MindCraft-AI/docs/PROJECT_CONTEXT.md")
text = path.read_text(encoding="utf-8")

marker = "## 38.7 Milestone Plan Status"

if marker not in text:
    raise RuntimeError("Insertion marker not found.")

milestone5 = """
# 41. Milestone 5 Implementation Record

Milestone 5 adds AI-generated Flashcards as the next learning stage after Notes generation while preserving the completed Notes, PDF Input, and Notes Utilities workflows.

## 41.1 Milestone 5 Scope

Milestone 5 implements:

* AI-powered flashcard generation.
* Dedicated Flashcards API endpoint.
* Dedicated Flashcards request and response schemas.
* Dedicated Flashcards prompt builder.
* Dedicated Flashcards service.
* Deterministic flashcard count selection.
* Interactive frontend flashcard viewer.
* Previous and Next navigation.
* Show Answer and Hide Answer interaction.
* Progress indicator.
* Automated backend tests.
* Manual frontend verification.

Milestone 5 preserves:

* Existing Notes generation workflow.
* Existing PDF extraction workflow.
* Existing Copy Notes functionality.
* Existing PDF Export functionality.
* Stateless application architecture.

Milestone 5 does not add:

* Flashcard persistence.
* Database storage.
* Difficulty ratings.
* User scoring.
* Spaced repetition.
* Leitner scheduling.
* Adaptive revision.
* Automatic flashcard generation.
* Flashcard export.
* Authentication.

## 41.2 Backend Architecture

Flashcard generation is isolated behind a dedicated service.

The backend flow is:

POST /api/v1/flashcards/generate
→ Flashcards route
→ Flashcards service
→ Gemini
→ Structured validation
→ FlashcardsResponse

The route remains thin.

Prompt construction is separated from Gemini communication.

Gemini interaction remains isolated inside the service layer.

Structured AI responses are validated before returning them to the client.

## 41.3 Grounding Strategy

Flashcards are generated from the latest successful NotesResponse.

The prompt uses the provided generated notes as the sole grounding material.

The prompt:

* Requests an exact deterministic number of flashcards.
* Prioritizes important concepts.
* Avoids duplicate cards.
* Avoids trivial cards.
* Restricts each card to a single concept.
* Rejects unsupported facts.
* Rejects topic expansion.
* Treats study material as untrusted input.
* Ignores prompt-injection attempts.
* Requires structured output matching the FlashcardsResponse schema.

## 41.4 Flashcard Selection Policy

Version 1 intentionally exposes no flashcard quantity controls.

The backend selects an appropriate deterministic target count based on the amount of study material.

The selection logic is implemented outside Gemini.

Gemini is instructed to generate exactly the selected number of flashcards.

No randomness is used.

## 41.5 Frontend Integration

Flashcards are generated only after explicit user action.

The frontend uses the latest successful NotesResponse already stored in memory.

The Generate Flashcards button remains disabled until a successful NotesResponse exists.

Successful generation stores the latest successful FlashcardsResponse in frontend memory only.

Each flashcard initially displays only the front side.

The answer is revealed only after the user selects Show Answer.

Hide Answer conceals the answer again.

Moving to another flashcard resets the answer to the hidden state.

Previous and Next navigation operate entirely on frontend state without additional AI requests.

A progress indicator displays the current flashcard position.

Failed flashcard generation preserves the latest successful flashcard state.

## 41.6 Testing and Verification

Previous automated backend result:

63 tests passing.

Milestone 5 adds 10 backend tests.

Final automated backend result:

73 tests passing.

Automated coverage includes:

* Flashcards request validation.
* Flashcard schema validation.
* Deterministic target-count selection.
* Prompt grounding.
* Prompt requests exact target count.
* Prompt injection defenses.
* Duplicate-card prevention instructions.
* Endpoint success behavior.
* Native FastAPI/Pydantic HTTP 422 validation.
* Gemini error mappings.

Additional verification completed:

* Application import succeeds.
* GET /api/v1/health succeeds.
* Existing Notes endpoint regression verification passed.
* Existing PDF extraction regression verification passed.
* Existing PDF Export regression verification passed.
* JavaScript syntax checks passed.
* Git whitespace checks passed.

Manual verification completed:

* Notes generation succeeded.
* Flashcards generation succeeded.
* Flashcards remained grounded in generated notes.
* Show Answer and Hide Answer worked correctly.
* Previous and Next navigation worked correctly.
* Progress indicator updated correctly.
* Navigation reset answer visibility correctly.
* New flashcard generation replaced the previous set.
* Failed Notes generation preserved the latest successful NotesResponse.
* Flashcards continued operating on the latest successful NotesResponse.

## 41.7 Architecture and Security

The application remains stateless.

No flashcards are persisted.

No generated notes or flashcards are logged.

Unexpected programming errors continue to propagate through normal application error handling.

Expected Gemini failures return sanitized client-facing responses.

Existing Notes and Document workflows remain unchanged.

## 41.8 Known Limitations

Flashcards are generated from the latest successful NotesResponse only.

Version 1 does not include spaced repetition, adaptive scheduling, user progress tracking, editing, persistence, or export.

Flashcards are intended as lightweight revision material rather than comprehensive study notes.
"""

# Insert before the milestone plan status
text = text.replace(marker, milestone5 + "\n\n" + marker, 1)

old_status = "* Milestone 5 â€” Flashcards: **Not Started**"
new_status = "* Milestone 5 â€” Flashcards: **Complete**"

if old_status not in text:
    raise RuntimeError("Milestone 5 status line not found.")

text = text.replace(old_status, new_status, 1)

old_sentence = "Milestone 5 has not started."
new_sentence = "Milestone 5 is complete."

if old_sentence in text:
    text = text.replace(old_sentence, new_sentence, 1)

path.write_text(text, encoding="utf-8", newline="\n")

print("PROJECT_CONTEXT.md updated successfully.")