# MindCraft AI â€” Project Context

## 1. Document Purpose

This document is the primary source of truth for MindCraft AI v1.0.

It defines the product vision, target users, scope, learning workflow, feature requirements, technology stack, AI architecture, API design, frontend expectations, engineering principles, and development constraints.

All AI coding assistants and contributors working on this project must read and follow this document before proposing architecture or writing code.

If a requested change conflicts with this document, the conflict must be identified before implementation.

Do not add features outside the Version 1 scope without explicit approval.

---

# 2. Project Identity

## Product Name

**MindCraft AI**

## Product Description

MindCraft AI is a personalized AI study companion designed primarily for college students.

It transforms user-provided study material into personalized notes and allows students to generate flashcards and interactive quizzes on demand.

After a quiz is submitted, the application evaluates the student's answers, identifies weak concepts, and allows the student to generate focused revision material for those concepts before taking a new targeted quiz.

MindCraft AI is not intended to be a generic chatbot, document summarizer, or collection of unrelated AI tools.

The product is built around one focused learning loop:

**Understand â†’ Study â†’ Test â†’ Identify Weaknesses â†’ Revise â†’ Retest**

---

# 3. Product Vision

The goal of MindCraft AI is to help college students turn raw study material into a structured and personalized learning experience.

Most simple AI study applications stop after generating content.

MindCraft AI should go further by allowing students to:

1. Provide study material.
2. Personalize how they want to learn it.
3. Generate structured notes.
4. Study those notes.
5. Generate an interactive quiz when requested.
6. Test their understanding.
7. Identify concepts associated with incorrect answers.
8. Generate focused revision material for weak concepts.
9. Retest those concepts.

The product should feel focused, useful, fast, and polished.

The intended user reaction is:

> "This is actually useful. I would use this before an exam."

---

# 4. Project Objectives

MindCraft AI has four primary objectives.

## 4.1 Learning Objective

Help college students understand, revise, remember, and test academic material more effectively.

## 4.2 Prompt Engineering Objective

Demonstrate meaningful prompt engineering through dynamic prompt composition based on user-selected learning preferences.

The application must not rely on one generic summarization prompt.

## 4.3 Engineering Objective

Demonstrate the development of a modular full-stack AI application with a Python backend, external LLM API integration, interactive frontend, secure secret management, error handling, and cloud deployment.

## 4.4 Portfolio Objective

Produce a deployed project suitable for:

* IBM AI and Cloud Computing internship submission.
* GitHub portfolio.
* Resume projects section.
* Technical interviews and project demonstrations.

---

# 5. Target Audience

## Primary Users

College students who already have study material and want to convert it into more effective learning resources.

Examples include students studying:

* Computer Science
* Engineering
* Commerce
* Humanities
* Natural Sciences
* Other university-level subjects

## Secondary Users

* University students.
* Competitive examination aspirants.
* Independent learners.

Version 1 must be designed primarily for college students.

---

# 6. Core Product Principles

All product and engineering decisions must follow these principles.

## 6.1 Learning Value Over Feature Count

MindCraft AI should contain a small number of connected features that work well.

Do not add unrelated AI tools merely to increase the feature count.

## 6.2 Personalize Learning, Not Cosmetic Wording

Personalization should change how educational content is created.

Useful personalization includes:

* Learning goal.
* Knowledge level.
* Note length.
* Output format.

Professional/casual tone selectors are intentionally excluded because they provide limited educational value.

## 6.3 AI Calls Must Be User-Initiated

Do not automatically generate quizzes, flashcards, revision notes, or retests.

Each additional AI operation must occur only when the user requests it.

This reduces unnecessary latency and API usage.

## 6.4 One Coherent Learning Loop

All core features must support:

**Understand â†’ Study â†’ Test â†’ Identify Weaknesses â†’ Revise â†’ Retest**

## 6.5 Build the Simplest Architecture That Correctly Solves the Problem

Avoid unnecessary frameworks, databases, authentication systems, microservices, queues, and infrastructure.

## 6.6 Portfolio Quality Over Prototype Quantity

A smaller polished application is preferable to a larger unfinished application.

---

# 7. Version 1 Scope

## 7.1 Required Features

MindCraft AI v1.0 must include:

1. Text input.
2. PDF upload and text extraction.
3. Personalized AI note generation.
4. Learning goal selection.
5. Knowledge level selection.
6. Note length selection.
7. Output format selection.
8. Generated notes display.
9. Copy notes.
10. PDF export of generated notes.
11. Estimated reading time calculated locally.
12. Flashcard generation on demand.
13. Interactive quiz generation on demand.
14. Quiz question count selection.
15. Quiz difficulty selection.
16. Client-side quiz interaction.
17. Quiz scoring.
18. Correct and incorrect answer review.
19. Weak concept identification.
20. Focused revision generation for weak concepts.
21. Targeted retest generation.
22. Responsive Apple-inspired user interface.
23. Secure Gemini API integration.
24. AWS Elastic Beanstalk deployment.

## 7.2 Explicitly Excluded From Version 1

Do not implement:

* User accounts.
* Authentication.
* Database.
* Saved history.
* Persistent user progress.
* Admin dashboard.
* AI chatbot.
* Chat with notes.
* Timetable generator.
* Calendar integration.
* Social features.
* Collaboration.
* Leaderboards.
* Gamification systems.
* Notifications.
* Voice assistant.
* Multiple decorative themes.
* Professional/casual tone selector.
* Analytics dashboard.

These may be documented as future enhancements.

---

# 8. Technology Stack

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript

The frontend must not require React, Vue, Angular, or another frontend framework.

A UI generation tool may be used to create the initial frontend, but exported code must be understandable, maintainable, and compatible with the chosen stack.

## Backend

* Python
* FastAPI

## AI Provider

* Google Gemini API

The Gemini API must be accessed only through the backend.

The frontend must never contain or receive the Gemini API key.

## PDF Input

Use a lightweight Python PDF text extraction library suitable for the final deployment environment.

The implementation should be isolated behind a document extraction service so the library can be replaced without changing API routes.

## PDF Export

Prefer client-side PDF export if it provides acceptable output quality.

Do not use an AI call for PDF export.

## Deployment

* AWS Elastic Beanstalk

## Version Control

* Git
* GitHub

---

# 9. High-Level Architecture

The application follows a simple client-server architecture.

```text
Browser
   |
   | HTTPS Requests
   v
Frontend
HTML + CSS + Vanilla JavaScript
   |
   | REST API
   v
FastAPI Backend
   |
   +---------------------------+
   |                           |
   v                           v
Prompt Builder          Document Extraction Service
   |                           |
   v                           v
Gemini Service              PDF Text
   |
   v
Google Gemini API
   |
   v
Structured AI Response
   |
   v
Response Validation / Parsing
   |
   v
Frontend Rendering
```

The application must remain a single deployable backend service for Version 1.

Do not introduce microservices.

---

# 10. Core User Flow

```text
Landing Page
      |
      v
Study Workspace
      |
      +--> Paste Text
      |
      +--> Upload PDF
      |
      v
Choose Learning Preferences
      |
      +--> Learning Goal
      +--> Knowledge Level
      +--> Note Length
      +--> Output Format
      |
      v
Generate Notes
      |
      v
Study Generated Notes
      |
      +--> Copy Notes
      |
      +--> Export PDF
      |
      +--> Generate Flashcards
      |
      +--> Generate Quiz
                |
                v
           Take Quiz
                |
                v
           Submit Answers
                |
                v
           View Results
                |
                +--> Score
                +--> Correct Answers
                +--> Incorrect Answers
                +--> Weak Concepts
                |
                v
       Teach Me My Weak Topics
                |
                v
       Focused Revision Material
                |
                v
             Retest
                |
                v
       Targeted Quiz on Weak Concepts
```

The quiz, flashcard, revision, and retest operations must never run automatically.

---

# 11. Application Screens and States

MindCraft AI should behave primarily as a focused web application rather than a large multi-page website.

## 11.1 Landing Page

Purpose:

Introduce MindCraft AI and move the user into the study workflow quickly.

Required content:

* MindCraft AI branding.
* Clear value proposition.
* Short explanation of the learning workflow.
* Core feature highlights.
* Primary call-to-action.
* Minimal footer.

Do not create a long marketing website.

## 11.2 Study Workspace

Purpose:

Collect study material and learning preferences.

Required components:

* Large text input area.
* PDF upload control.
* Clear indication of the selected input source.
* Learning goal selector.
* Knowledge level selector.
* Note length selector.
* Output format selector.
* Generate Notes button.
* Input validation.
* Loading state.
* Error state.

## 11.3 Generated Notes State

Purpose:

Display readable, well-structured study notes.

Required components:

* Generated note title.
* Formatted note content.
* Estimated reading time.
* Copy Notes button.
* Export PDF button.
* Generate Flashcards button.
* Generate Quiz button.

## 11.4 Flashcards State

Purpose:

Allow the student to review important concepts.

Required behavior:

* Generated only after explicit user request.
* Interactive card flipping.
* Previous and next navigation.
* Progress indicator.
* Clear question/front and answer/back structure.

Flashcards are a study aid and must not trigger additional automatic AI requests.

## 11.5 Quiz Configuration State

Purpose:

Allow the user to configure a quiz.

Required controls:

Question count:

* 5
* 10
* 20

Difficulty:

* Easy
* Medium
* Hard

The quiz is generated only after the user confirms the configuration.

## 11.6 Quiz State

Purpose:

Provide an interactive assessment.

Required behavior:

* One clearly displayed question at a time or another clean interaction model.
* Multiple-choice answers.
* Selected answer state.
* Question navigation.
* Progress indicator.
* Submit Quiz button.
* Prevent accidental submission when unanswered questions exist without warning the user.

## 11.7 Quiz Results State

Purpose:

Explain performance clearly.

Required content:

* Total score.
* Percentage.
* Correct answers.
* Incorrect answers.
* Correct answer for each incorrect response.
* Brief explanation where available.
* Weak concepts derived from incorrect answers.
* Teach Me My Weak Topics button.

## 11.8 Focused Revision State

Purpose:

Help the student understand concepts associated with incorrect answers.

For each weak concept, revision material should include:

* Concise explanation.
* Relevant example.
* Useful analogy when appropriate.
* Memory trick when appropriate.
* Key facts to remember.
* Common misconception or mistake when relevant.

Required action:

* Retest Me button.

## 11.9 Retest State

Purpose:

Verify whether the student improved after revision.

The retest must focus on previously identified weak concepts.

Questions should be newly generated and should not simply repeat the original quiz questions.

---

# 12. Note Personalization Model

MindCraft AI personalizes note generation using four dimensions.

## 12.1 Learning Goal

Allowed values:

### Academic

Purpose:

Create structured, balanced study notes suitable for learning a subject.

### Exam Revision

Purpose:

Prioritize high-yield concepts, definitions, likely exam-relevant material, and efficient revision.

The model must not claim to know actual exam questions unless such information is present in the source material.

### Deep Understanding

Purpose:

Prioritize conceptual explanation, reasoning, relationships between ideas, examples, and deeper understanding.

### Explain Simply

Purpose:

Explain concepts using accessible language, reduced jargon, and useful analogies without sacrificing factual accuracy.

## 12.2 Knowledge Level

Allowed values:

### Beginner

Assume limited prior knowledge.

Explain terminology and prerequisite concepts.

### Intermediate

Assume basic familiarity.

Balance explanation with technical depth.

### Advanced

Use appropriate domain terminology and emphasize nuance, relationships, limitations, and deeper technical detail.

Do not add unsupported facts merely to make the notes appear advanced.

## 12.3 Note Length

Allowed values:

### Quick Review

Create concise notes containing only the highest-value information.

### Standard

Create balanced notes with sufficient explanation, examples, and revision support.

### Comprehensive

Create detailed notes covering the source material thoroughly while remaining structured and avoiding unnecessary repetition.

Length is a content-detail target, not a guaranteed page count.

Do not promise exact page lengths because rendered pages vary by device, font, and export settings.

## 12.4 Output Format

Allowed values:

### Structured Paragraphs

Use headings, subheadings, concise paragraphs, and supporting lists where useful.

### Bullet Points

Prioritize hierarchical bullet points and concise statements.

### Cornell Notes

Organize content into:

* Cue / Question column content.
* Main Notes content.
* Summary.

The frontend should render Cornell Notes appropriately if this format is selected.

### Outline

Use hierarchical topic and subtopic organization.

The output format must materially change the generated structure.

---

# 13. Generated Notes Requirements

The generated notes must be grounded primarily in the user-provided source material.

The AI should organize, explain, and clarify the material without inventing unsupported facts.

Required note components:

* Title.
* Structured headings and subheadings.
* Key concepts.
* Important definitions when applicable.
* Examples when useful.
* Final summary.
* Key takeaways.
* Memory tricks when genuinely useful.
* Common mistakes or misconceptions when relevant.
* One-Minute Revision section.

A table of contents should only be included for sufficiently long output.

Do not force every optional educational element into every topic.

For example, a memory trick should not be fabricated when it provides no learning value.

---

# 14. Flashcard Requirements

Flashcards must be generated from the source material and/or generated notes.

Each flashcard must contain:

* Front: one clear question, concept, term, or prompt.
* Back: one concise answer or explanation.

Requirements:

* Avoid duplicate cards.
* Avoid trivial cards.
* Prioritize important concepts.
* Keep individual cards focused on one concept.
* Return machine-readable structured data.

The initial Version 1 interface does not require flashcard quantity or difficulty configuration.

The backend may choose an appropriate number based on source length within a safe maximum.

---

# 15. Quiz Requirements

The quiz must be based on the study material and generated notes.

Each question must contain:

* Unique question identifier.
* Question text.
* Four answer options.
* Correct answer.
* Short explanation.
* Concept or topic label.

The concept label is required for weak-topic analysis.

Requirements:

* Exactly one correct answer per question.
* Avoid duplicate questions.
* Avoid ambiguous questions.
* Avoid questions that cannot be answered from the learning material.
* Return machine-readable structured data.

---

# 16. Quiz Evaluation and Weak Concept Logic

Quiz scoring should be deterministic application logic.

Do not use an additional Gemini API call merely to calculate the quiz score.

The backend or frontend may compare submitted answers against the answer key.

The system must:

1. Calculate total correct answers.
2. Calculate percentage score.
3. Identify incorrect questions.
4. Collect the concept labels associated with incorrect questions.
5. Deduplicate weak concepts.
6. Display weak concepts to the user.

The application should retain the current learning session state in the browser for Version 1.

A database is not required.

---

# 17. Focused Revision Requirements

Focused revision is generated only after the user explicitly requests help with weak topics.

The request should include:

* Original source material or a bounded relevant representation.
* Generated notes when useful.
* Weak concept labels.
* Incorrect quiz questions and explanations when useful.
* Original learning preferences when relevant.

The focused revision output should teach weak concepts efficiently.

It should not regenerate the entire original note set.

---

# 18. Retest Requirements

The retest must:

* Be generated only after explicit user request.
* Focus on weak concepts.
* Generate new questions.
* Avoid copying original quiz questions.
* Use an appropriate bounded question count.
* Return the same structured quiz schema used by the original quiz where practical.

For Version 1, one revision-and-retest cycle is sufficient.

Do not build an unlimited autonomous tutoring loop.

---

# 19. Prompt Engineering Architecture

Prompt engineering is a core technical feature of MindCraft AI.

The application must use dynamic prompt composition.

Do not create one static prompt for all note requests.

Do not create a separate full prompt file for every possible combination of selections.

Use reusable prompt components.

Conceptual architecture:

```text
Base System Instruction
        +
Task Instruction
        +
Learning Goal Instruction
        +
Knowledge Level Instruction
        +
Length Instruction
        +
Output Format Instruction
        +
Content Grounding Rules
        +
Required Output Schema
        +
User Source Material
        =
Final Prompt
```

Separate prompt-building functions should exist for:

* Notes.
* Flashcards.
* Quiz.
* Focused revision.
* Retest.

Prompt-building logic must be separate from API route logic and Gemini API client logic.

---

# 20. Structured AI Output

Where the frontend depends on predictable data structures, Gemini responses must use structured JSON output.

This applies particularly to:

* Quiz generation.
* Flashcards.
* Weak-topic revision data where structured rendering is required.
* Retest generation.

Use Pydantic schemas to validate structured backend data where practical.

Do not parse critical application data from arbitrary AI-generated prose using fragile string splitting.

If AI output is invalid:

1. Detect the validation failure.
2. Handle the error safely.
3. Return a clear error response or use a bounded retry strategy where appropriate.

Do not create infinite retry loops.

---

# 21. API Architecture

Use versioned REST API routes.

Base path:

`/api/v1`

Required endpoints:

## Health Check

`GET /api/v1/health`

Purpose:

Verify that the backend service is running.

## Extract PDF

`POST /api/v1/documents/extract`

Purpose:

Upload a PDF and return extracted text.

## Generate Notes

`POST /api/v1/notes/generate`

Purpose:

Generate personalized notes from source material and selected learning preferences.

## Generate Flashcards

`POST /api/v1/flashcards/generate`

Purpose:

Generate flashcards on demand.

## Generate Quiz

`POST /api/v1/quizzes/generate`

Purpose:

Generate a configured interactive quiz.

## Generate Focused Revision

`POST /api/v1/revision/generate`

Purpose:

Generate revision material for weak concepts.

## Generate Retest

`POST /api/v1/quizzes/retest`

Purpose:

Generate new questions focused on weak concepts.

Quiz scoring does not require an AI endpoint.

It should use deterministic application logic.

---

# 22. API Request Principles

All request bodies must be validated.

The backend must enforce reasonable limits on:

* Source text size.
* PDF file size.
* Allowed file type.
* Quiz question count.
* Allowed enum values.

Do not trust frontend validation alone.

Use Pydantic request and response models.

Return appropriate HTTP status codes.

Do not expose stack traces, Gemini API keys, or internal secrets to the client.

---

# 23. Gemini Integration Principles

All Gemini API communication must occur through a dedicated service layer.

API routes must not call the Gemini SDK directly.

Conceptual flow:

```text
API Route
    |
    v
Controller / Use-Case Logic
    |
    v
Prompt Builder
    |
    v
Gemini Service
    |
    v
Response Validation
    |
    v
API Response
```

The Gemini model name must be configurable through environment variables or centralized configuration.

Do not scatter model names throughout the codebase.

The API key must be stored in environment variables.

Never commit secrets to GitHub.

Provide `.env.example` without real secret values.

---

# 24. API Usage and Cost Principles

API efficiency is a design requirement.

Rules:

* Notes are generated only when requested.
* Flashcards are generated only when requested.
* Quizzes are generated only when requested.
* Focused revision is generated only when requested.
* Retests are generated only when requested.
* Quiz scoring must not use Gemini.
* Reading time must not use Gemini.
* PDF export must not use Gemini.
* Do not send unnecessary conversation history.
* Avoid sending redundant source material when a smaller grounded context is sufficient.
* Enforce input size limits.

Do not introduce caching in Version 1 unless API limits become a demonstrated problem.

---

# 25. Frontend Design Direction

MindCraft AI uses an Apple-inspired visual direction.

This means:

* Strong visual hierarchy.
* Generous whitespace.
* Minimal clutter.
* Restrained use of color.
* High-quality typography.
* Subtle borders.
* Soft shadows.
* Carefully used translucency.
* Smooth transitions.
* Clear interaction states.
* Responsive layouts.

Do not attempt to copy Apple's website directly.

Do not sacrifice readability for glassmorphism or visual effects.

Avoid:

* Excessive gradients.
* Neon cyberpunk styling.
* Particle backgrounds.
* Background videos.
* Excessive animation.
* Decorative dashboards.
* Unnecessary charts.
* Multiple visual themes.

One polished visual system is required.

Dark mode is optional and must only be implemented after core functionality is complete.

---

# 26. Frontend Interaction Principles

Every interactive element must have a clear purpose.

Required states include:

* Default.
* Hover where applicable.
* Focus.
* Selected.
* Disabled.
* Loading.
* Success where useful.
* Error.

AI operations must display clear loading feedback.

Do not display fake technical steps claiming that the AI is performing operations that are not actually known.

Loading messages may be user-friendly, but they must not misrepresent backend behavior.

The interface must remain usable on desktop and mobile devices.

Accessibility requirements include:

* Semantic HTML.
* Keyboard-accessible controls.
* Visible focus states.
* Proper labels.
* Sufficient color contrast.
* Reduced-motion consideration for nonessential animation.

---

# 27. State Management

Version 1 does not use a database.

The frontend must manage the current learning session.

Session data may include:

* Source text.
* Input source type.
* Selected learning preferences.
* Generated notes.
* Generated flashcards.
* Quiz data.
* User answers.
* Quiz results.
* Weak concepts.
* Focused revision content.
* Retest data.

Use simple JavaScript state management.

Browser `sessionStorage` may be used for resilience against accidental refreshes if needed.

Do not introduce a frontend state-management library.

---

# 28. Recommended Repository Structure

```text
MindCraft-AI/
|
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |   |-- v1/
|   |   |
|   |   |-- core/
|   |   |   |-- config.py
|   |   |
|   |   |-- prompts/
|   |   |   |-- notes.py
|   |   |   |-- flashcards.py
|   |   |   |-- quizzes.py
|   |   |   |-- revision.py
|   |   |
|   |   |-- schemas/
|   |   |
|   |   |-- services/
|   |   |   |-- gemini_service.py
|   |   |   |-- document_service.py
|   |   |
|   |   |-- utils/
|   |   |
|   |   |-- main.py
|   |
|   |-- requirements.txt
|   |-- .env.example
|
|-- frontend/
|   |-- css/
|   |-- js/
|   |-- assets/
|   |-- index.html
|
|-- docs/
|   |-- PROJECT_CONTEXT.md
|
|-- .gitignore
|-- README.md
```

The exact structure may evolve when implementation reveals a genuine need.

Do not add empty architectural layers merely to make the repository look more professional.

---

# 29. Coding Standards

## Python

* Use clear Python naming conventions.
* Use type hints.
* Use Pydantic models for API validation.
* Prefer small, focused functions.
* Keep routes thin.
* Separate prompt construction from Gemini communication.
* Separate document extraction from route logic.
* Avoid premature abstractions.
* Add docstrings where they provide meaningful value.
* Handle expected exceptions explicitly.
* Use asynchronous endpoints and SDK calls where the chosen libraries support them appropriately.

## JavaScript

* Use modern JavaScript.
* Prefer `const` and `let`.
* Avoid unnecessary global variables.
* Separate API communication, rendering logic, and application state where practical.
* Handle network failures.
* Disable relevant controls during active requests.
* Prevent duplicate submissions.
* Never place secrets in frontend code.

## CSS

* Use reusable design tokens with CSS custom properties.
* Use consistent spacing, radius, typography, and shadow systems.
* Avoid excessive `!important`.
* Keep responsive behavior intentional.
* Do not add visual effects that reduce readability.

---

# 30. Security Requirements

Version 1 must:

* Store the Gemini API key in backend environment variables.
* Never expose secrets to the browser.
* Never commit `.env`.
* Validate all request bodies.
* Validate uploaded file type.
* Enforce file size limits.
* Enforce text size limits.
* Escape or safely render AI-generated content.
* Avoid rendering unsanitized AI output with unrestricted `innerHTML`.
* Configure CORS only for required origins.
* Avoid exposing internal error details in production.
* Use HTTPS through the deployed environment.

Authentication is outside Version 1 scope.

---

# 31. Error Handling Requirements

The user must receive clear messages for:

* Empty input.
* Unsupported PDF.
* PDF extraction failure.
* Input exceeding allowed limits.
* Gemini API failure.
* Invalid AI response.
* Network failure.
* Quiz generation failure.
* Revision generation failure.
* Retest generation failure.
* PDF export failure.

Do not show raw exceptions or stack traces to users.

Errors should be logged appropriately on the backend for debugging.

---

# 32. Testing Requirements

Version 1 must include meaningful testing of core logic.

At minimum, test:

* Prompt builder behavior for different learning preferences.
* Request validation.
* Quiz scoring logic.
* Weak concept extraction and deduplication.
* Invalid structured AI response handling where practical.
* Core API health behavior.

Manual end-to-end testing must verify:

1. Text input to notes.
2. PDF input to notes.
3. Notes to flashcards.
4. Notes to quiz.
5. Quiz submission and scoring.
6. Weak concept identification.
7. Focused revision generation.
8. Retest generation.
9. Copy notes.
10. PDF export.
11. Mobile usability.
12. Production deployment.

Do not chase high test coverage percentages at the expense of finishing the product.

---

# 33. Deployment Requirements

The final application must be deployable to AWS Elastic Beanstalk.

Deployment concerns must be considered during development rather than added at the last moment.

Requirements:

* Production dependency file.
* Correct application entry point.
* Environment-variable configuration.
* Configurable Gemini model.
* Production-safe error handling.
* CORS configuration.
* Health endpoint.
* No hardcoded localhost URLs in production frontend code.
* Clear deployment instructions in README.

Before deployment, confirm the current AWS Elastic Beanstalk Python platform requirements and deployment configuration.

Do not assume local development behavior guarantees production compatibility.

---

# 34. Development Strategy

MindCraft AI must be built vertically in small working increments.

Recommended order:

## Milestone 1 â€” Foundation

* Repository setup.
* Backend skeleton.
* Frontend skeleton.
* Environment configuration.
* Health endpoint.
* Local frontend-backend communication.

## Milestone 2 â€” Notes Vertical Slice

* Text input.
* Learning preference controls.
* Prompt builder.
* Gemini integration.
* Notes generation.
* Notes rendering.
* Error handling.

At the end of this milestone, the application must already perform one complete useful workflow.

## Milestone 3 â€” PDF Input

* PDF validation.
* Text extraction.
* Extracted content to note generation.

## Milestone 4 â€” Notes Utilities

* Reading time.
* Copy notes.
* PDF export.

## Milestone 5 â€” Flashcards

* Structured flashcard generation.
* Validation.
* Interactive flashcard UI.

## Milestone 6 â€” Quiz

* Quiz configuration.
* Structured quiz generation.
* Interactive quiz.
* Deterministic scoring.
* Answer review.
* Weak concept extraction.

## Milestone 7 â€” Adaptive Revision

* Focused revision generation.
* Weak-topic learning UI.
* Retest generation.
* Retest interaction.

## Milestone 8 â€” Polish

* Responsive design.
* Accessibility review.
* Loading states.
* Error states.
* Performance improvements.
* UI consistency.

## Milestone 9 â€” Reading Themes

* Add a new dropdown to the Notes Generation form.
* Apply selected theme class to the notes container.
* Add CSS rules for 5 different themes.
* Switch themes without reloading or regenerating content.

## Milestone 10 â€” Documentation

* README.
* Architecture explanation.
* Screenshots.
* Internship Concept Note.
* Project Report.
* Viva preparation.
* Resume bullets.

Do not build the entire frontend before validating backend integration.

Do not build every backend endpoint before completing the notes vertical slice.

---
## 38.8 Development Workflow

The workflow established during Milestones 1 through 6 becomes the standard engineering process for the remainder of Version 1.

For every future milestone:

1. Read this PROJECT_CONTEXT.md before making implementation decisions.
2. Restrict implementation strictly to the approved milestone scope.
3. Preserve all previously completed milestone functionality.
4. Maintain the existing application architecture unless an approved design change requires otherwise.
5. Add automated tests covering all newly introduced behavior.
6. Execute the complete backend test suite.
7. Verify frontend JavaScript syntax where applicable.
8. Run `git diff --check` before staging changes.
9. Perform manual verification of the new user workflow.
10. Update this PROJECT_CONTEXT.md with a milestone implementation record matching the established documentation format.
11. Review staged changes before committing.

Implementation records must accurately describe the shipped functionality, automated testing, manual verification, architecture, security considerations, and known limitations.

Documentation maintenance must never invent features, tests, implementation details, or verification that are not present in the codebase.
# 35. Acceptance Criteria for Version 1

MindCraft AI v1.0 is complete only when:

1. A user can paste text and generate personalized notes.
2. A user can upload a valid PDF and generate notes from extracted text.
3. Note output changes meaningfully based on learning goal.
4. Note output changes meaningfully based on knowledge level.
5. Note output changes meaningfully based on length selection.
6. Note structure changes meaningfully based on output format.
7. Generated notes are readable and grounded in the source material.
8. A user can copy notes.
9. A user can export notes to PDF.
10. Reading time is calculated without an AI call.
11. A user can request and interact with flashcards.
12. A user can configure and request a quiz.
13. A user can answer and submit quiz questions.
14. Quiz scoring works without an AI call.
15. Correct and incorrect answers are displayed.
16. Weak concepts are identified from incorrect answers.
17. A user can request focused revision material.
18. Focused revision addresses the identified weak concepts.
19. A user can request a new targeted retest.
20. Gemini secrets are never exposed to the frontend or Git repository.
21. The application handles expected errors without crashing.
22. The interface is responsive and usable.
23. The live application is deployed successfully on AWS Elastic Beanstalk.
24. The GitHub repository contains clear setup and usage documentation.

---

# 36. Decision Rules for AI Coding Assistants

When working on MindCraft AI:

1. Read this document before proposing architecture or implementation.

2. Do not add features outside Version 1 scope.

3. Do not change the technology stack without explicit approval.

4. Do not introduce React, databases, authentication, microservices, or unrelated infrastructure.

5. Do not rewrite working files unnecessarily.

6. Before modifying existing code, inspect the relevant files and preserve working behavior.

7. Implement one milestone or clearly bounded task at a time.

8. State which files will be created or modified before producing large changes.

9. Do not generate the entire application in one response.

10. Prefer working vertical slices over large disconnected code generation.

11. Keep routes thin and business logic modular.

12. Keep prompt-building logic separate from Gemini API communication.

13. Use structured validated AI output where application logic depends on predictable data.

14. Do not use Gemini for deterministic operations that normal application code can perform.

15. Never expose API keys or secrets.

16. Do not claim that code has been tested, deployed, or verified unless it actually has been.

17. If a requirement is ambiguous, ask before making a major architectural assumption.

18. If a requested feature conflicts with the frozen Version 1 scope, identify the conflict before implementation.

19. Avoid overengineering.

20. Prioritize completing a polished, reliable Version 1 application within the one-week development schedule.

---

# 37. Final Product Definition

MindCraft AI v1.0 is a focused personalized AI learning application.

It accepts study material, adapts generated notes to the student's learning needs, provides optional flashcards and quizzes, evaluates quiz performance, identifies weak concepts, generates targeted revision material, and retests the student.

Its value comes from the complete learning loop and meaningful prompt personalization, not from having a large number of unrelated AI features.

The final application must be:

* Useful.
* Focused.
* Understandable.
* Maintainable.
* Secure.
* Responsive.
* Deployable.
* Demonstrably relevant to prompt engineering.
* Strong enough to discuss honestly in an AI/ML internship interview.

This document defines the frozen product and engineering scope for MindCraft AI v1.0.



# 38. Current Implementation Status

This section records the verified implementation state of MindCraft AI.

It supplements the frozen Version 1 product and engineering scope defined above.

If the implementation status recorded here differs from an earlier milestone plan, this section describes the actual completed implementation state.

## 38.1 Milestone 1 â€” Foundation

**Status: Complete**

Completed functionality:

* Repository structure established.
* FastAPI backend skeleton implemented.
* Plain HTML, CSS, and JavaScript frontend skeleton implemented.
* Centralized environment configuration implemented.
* Versioned `/api/v1` routing established.
* `GET /api/v1/health` implemented.
* CORS configured through centralized settings.
* Frontend-to-backend health check implemented.
* Local frontend and backend communication verified.

Verification:

* Application imports successfully.
* Health endpoint returns the expected structured response.
* Frontend can communicate with the backend locally.

Git commit:

`12d1d63 milestone 1 completed`

## 38.2 Milestone 2 â€” AI-Powered Personalized Notes Vertical Slice

**Status: Complete**

Milestone 2 implements the first complete AI-powered workflow in MindCraft AI:

**Source Text â†’ Learning Preferences â†’ Dynamic Prompt â†’ Gemini â†’ Validated Structured Notes â†’ Deterministic Reading Time â†’ Frontend Rendering**

Completed functionality:

* User can enter source text.
* User can select a learning goal.
* User can select a knowledge level.
* User can select a note length.
* User can select an output format.
* Frontend sends note-generation requests to `POST /api/v1/notes/generate`.
* Backend validates request data using Pydantic.
* Source text is trimmed before use.
* Source text length limits are enforced by the backend.
* Allowed learning preference values are enforced using enums.
* Notes prompts are dynamically composed from all four personalization settings.
* Prompt construction is separated from Gemini SDK communication.
* Source material is enclosed in explicit delimiters.
* Prompts contain grounding and factuality rules.
* Prompts contain prompt-injection defenses.
* Prompts explicitly instruct Gemini not to expand into unsupported adjacent topics, concepts, terminology, facts, examples, or textbook material.
* Exam Revision instructions were strengthened to emphasize likely-tested distinctions and common misconceptions when supported by the source material.
* Advanced instructions were strengthened to emphasize assumptions, limitations, and tradeoffs when supported by the source material.
* Gemini integration uses the official `google-genai` Python SDK.
* The Gemini model is centrally configurable through `GEMINI_MODEL`.
* The default pinned model is `gemini-2.5-flash`.
* Gemini client initialization is lazy.
* The health endpoint continues to function without Gemini API configuration.
* Gemini generation uses the asynchronous SDK interface.
* Gemini requests are timeout-controlled.
* Gemini structured output is validated using Pydantic schemas.
* Invalid or missing parsed Gemini responses are handled safely.
* Estimated reading time is calculated deterministically by backend application logic.
* Reading time does not require an additional Gemini API call.
* API responses return generated notes, estimated reading time, and `config_used`.
* Frontend safely renders structured generated notes.
* Existing Milestone 1 behavior remains functional.

## 38.3 Milestone 2 Architecture

Milestone 2 added the following backend files:

```text
backend/app/api/v1/notes.py

backend/app/prompts/__init__.py
backend/app/prompts/notes.py

backend/app/schemas/__init__.py
backend/app/schemas/notes.py

backend/app/services/__init__.py
backend/app/services/gemini_errors.py
backend/app/services/gemini_service.py
backend/app/services/notes_service.py

backend/tests/__init__.py
backend/tests/test_notes_endpoint.py
backend/tests/test_notes_prompt.py
backend/tests/test_notes_schema_validation.py
````

The following existing files were modified:

```text
README.md

backend/.env.example
backend/app/api/v1/__init__.py
backend/app/core/config.py
backend/requirements.txt

frontend/css/style.css
frontend/index.html
frontend/js/api.js
frontend/js/main.js
```

Current notes-generation request flow:

```text
Frontend
    |
    v
POST /api/v1/notes/generate
    |
    v
Pydantic Request Validation
    |
    v
Thin API Route
    |
    v
Notes Service
    |
    +--> Dynamic Notes Prompt Builder
    |
    +--> Gemini Service
              |
              v
       Google Gemini API
              |
              v
       Structured Pydantic Output
    |
    v
Deterministic Reading-Time Calculation
    |
    v
Validated Notes Response
    |
    v
Safe Frontend Rendering
```

Architectural decisions established during Milestone 2:

* API routes remain thin.
* Orchestration logic belongs in services.
* Gemini SDK interaction belongs in the Gemini service.
* Prompt construction remains separate from Gemini communication.
* Deterministic calculations remain outside Gemini.
* Configuration remains centralized.
* API routes remain versioned under `/api/v1`.
* Gemini client initialization remains lazy.
* The application remains stateless.
* No database has been introduced.
* No authentication has been introduced.
* No frontend framework has been introduced.
* No unnecessary controller, repository, or dependency-injection layers have been added.

## 38.4 Gemini Error Handling and Logging

Milestone 2 defines four explicit Gemini service error types:

* `GeminiConfigurationError`
* `GeminiTimeoutError`
* `GeminiUpstreamError`
* `GeminiInvalidResponseError`

The API route maps these errors to sanitized HTTP responses:

* `GeminiConfigurationError` â†’ HTTP 500.
* `GeminiTimeoutError` â†’ HTTP 504.
* `GeminiUpstreamError` â†’ HTTP 502.
* `GeminiInvalidResponseError` â†’ HTTP 502.

Gemini SDK API errors are caught specifically rather than through a blanket `Exception` handler.

Unexpected programming exceptions are not mislabeled as Gemini upstream failures.

Backend logging is sanitized.

The application must not log:

* Gemini API keys.
* User source text.
* Full prompts.
* Raw Gemini responses.
* SDK error messages or details that may contain user-provided content.

Client responses must not expose stack traces, raw SDK errors, prompts, source material, API keys, or internal configuration details.

## 38.5 Milestone 2 Testing and Verification

**Automated test result: 24 tests passing.**

Automated tests cover:

* Source-text request validation.
* Source-text trimming.
* Minimum and maximum source-text limits.
* Allowed enum values.
* Distinct prompt instructions for learning goals.
* Distinct prompt instructions for knowledge levels.
* Distinct prompt instructions for note lengths.
* Distinct prompt instructions for output formats.
* Behavioral verification that changing each personalization setting changes the built prompt and selects the correct instruction.
* Source-material delimiters.
* Grounding and factuality instructions.
* Prompt-injection defenses.
* No-topic-expansion grounding rule.
* Gemini exception-to-HTTP status mappings.
* Sanitized client-facing error responses.

Additional verification completed:

* Application import succeeds.
* `google-genai` imports successfully in the project virtual environment.
* `GET /api/v1/health` succeeds.
* The health endpoint works independently of Gemini API configuration.
* A real Gemini notes-generation request succeeds end-to-end.
* The real request used:

  * Learning Goal: Exam Revision.
  * Knowledge Level: Advanced.
  * Note Length: Comprehensive.
  * Output Format: Structured Paragraphs.
* The real Gemini response passed structured-output validation.
* Reading time was calculated by backend application logic.
* The generated output showed stronger personalization.
* The strengthened grounding rules materially reduced unsupported adjacent-topic expansion.
* The frontend successfully generates and renders notes.
* Git whitespace checks passed before the Milestone 2 commit.
* The repository working tree was clean after the Milestone 2 commit.

Git commit:

`8868ecb milestone 2 completed`

## 38.6 Known Grounding Limitation

Prompt-only grounding materially reduced unsupported topic expansion but cannot guarantee perfect source faithfulness.

Gemini may still produce reasonable clarifications, inferred educational phrasing, memory tricks, common-mistake descriptions, or minor elaborations beyond the literal wording of the source material.

Do not endlessly tighten prompt wording in an attempt to guarantee perfect grounding.

If stricter source faithfulness becomes necessary, introduce a more robust grounding, evidence, or citation strategy appropriate to the application's requirements.

Any such change must preserve the simple Version 1 architecture unless a genuine implementation need justifies additional complexity.

# 39. Milestone 3 Implementation Record

Milestone 3 adds PDF input as an isolated document-extraction vertical slice while preserving the existing Notes generation workflow.

## 39.1 Milestone 3 Scope

Milestone 3 implements:

* PDF upload support.
* In-memory PDF text extraction.
* A dedicated document-extraction API endpoint.
* Validation for empty, oversized, invalid, malformed, encrypted, no-text, too-short, and too-long PDF inputs.
* Shared Notes source-text limits used by both Notes request validation and document extraction.
* Frontend PDF upload and explicit Extract Text controls.
* Population of the existing source-text textarea with extracted PDF text.
* An overwrite confirmation guard when source text already exists.
* Automated service-level and endpoint-level tests.
* Manual API and frontend verification.

Milestone 3 does not add:

* OCR support.
* Image-based or scanned-PDF text recognition.
* File persistence.
* Database storage.
* Cloud object storage.
* Automatic Notes generation after extraction.
* Gemini calls during document extraction.
* Additional document formats.

## 39.2 Backend Architecture

PDF extraction is isolated behind the document service.

The backend flow is:

`POST /api/v1/documents/extract -> documents route -> document service -> pypdf -> DocumentExtractResponse`

The endpoint accepts a multipart upload using the field name `file`.

Successful extraction returns:

* `extracted_text`
* `character_count`
* `page_count`

PDF processing is entirely in memory.

Uploaded PDF bytes and extracted text are not persisted to disk, a database, or external storage.

The document-extraction workflow does not call Gemini.

## 39.3 Dependencies and Configuration

Milestone 3 adds:

* `pypdf`
* `python-multipart`

The maximum accepted PDF upload size is configured as 10 MiB through `max_pdf_size_bytes`.

The service performs a bounded read of at most `max_pdf_size_bytes + 1` bytes so oversized uploads can be rejected without reading an arbitrarily large file into memory.

## 39.4 Shared Notes Source-Text Limits

The Notes workflow accepts source text from 50 through 20,000 characters.

These limits are defined once in `backend/app/core/constants.py`.

The shared constants are used by `NotesRequest.source_text` validation and PDF extraction compatibility validation, preventing duplicated limits from drifting out of sync.

## 39.5 PDF Validation and Error Behavior

The document service validates empty uploads, oversized uploads, invalid PDF signatures, malformed PDFs, encrypted PDFs, PDFs with no extractable text, and extracted text outside the Notes workflow limits.

Expected PDF parser failures are converted into document-domain errors.

Unexpected programming errors are not swallowed by broad exception handling and propagate through normal application error handling.

Client-facing error responses are sanitized and do not expose raw parser exceptions, stack traces, file bytes, extracted source text, filenames, or internal implementation details.

## 39.6 Frontend Integration

The Notes workspace includes a PDF file input, an explicit Extract Text button, and a PDF extraction status message.

Selecting a PDF does not automatically upload, extract, or generate notes.

Extraction occurs only after the user clicks Extract Text.

The frontend uses `FormData` and allows the browser to set the multipart boundary.

Existing source text is protected by an overwrite confirmation guard.

Successful extraction populates the existing source-text textarea.

Frontend rendering uses safe text/value assignment rather than `innerHTML`.

## 39.7 Testing and Verification

**Automated test result: 54 tests passing.**

Milestone 3 adds service-level and endpoint-level document-extraction tests while preserving the Milestone 1 and Milestone 2 regression suite.

Automated coverage includes successful extraction, page ordering and formatting, metadata correctness, upload-size enforcement, invalid and malformed PDFs, encrypted PDFs, no-text PDFs, Notes text-limit compatibility, HTTP error mappings, sanitized responses, unexpected-error propagation, and shared-limit consistency.

Additional manual verification completed:

* Application import succeeds.
* `GET /api/v1/health` succeeds.
* The document extraction endpoint appears in FastAPI API documentation.
* A real text-based PDF upload succeeds with HTTP 200.
* The response contains extracted text, character count, and page count.
* A non-PDF upload is rejected with HTTP 422.
* Frontend PDF extraction succeeds.
* Extracted text populates the existing source-text textarea.
* PDF extraction does not automatically generate notes.
* The overwrite guard works for both Cancel and confirmation paths.
* Git whitespace checks passed for the 15-file implementation snapshot.

## 39.8 Known Limitations

Milestone 3 supports text-based PDFs only.

Scanned and image-only PDFs are rejected when no extractable text is available because Version 1 does not include OCR.

PDF extraction may preserve line breaks, hyphenation, or other formatting artifacts produced by the source PDF and `pypdf`.

No file content or extracted text is persisted.

# 40. Milestone 4 Implementation Record

Milestone 4 adds Notes Utilities while preserving the completed Notes generation and PDF input workflows.

Reading time was completed early during Milestone 2 and remains unchanged.

## 40.1 Milestone 4 Scope

Milestone 4 implements the remaining Notes Utilities:

* Copy Notes.
* PDF Export.

Milestone 4 preserves:

* Existing deterministic reading-time calculation.
* Existing Gemini prompt logic.
* Existing Gemini service behavior.
* Existing document extraction behavior.
* Application statelessness.

Milestone 4 does not add:

* Database storage.
* Authentication.
* Notes history.
* Generated-content persistence.
* Additional export formats.
* Notes regeneration during export.
* Custom PDF themes or final visual polish.

## 40.2 Copy Notes

Copy Notes is implemented entirely in the frontend.

The generated notes state includes an explicit Copy Notes button.

The button is disabled until notes have been generated successfully.

The frontend stores the latest successful `NotesResponse` in memory only.

Copy Notes formats the complete generated notes as readable plain text, including:

* Title.
* Estimated reading time.
* Table of contents.
* Every section heading.
* Section content.
* Key points.
* Definitions.
* Examples.
* Memory tricks.
* Common mistakes.
* Summary.
* Key takeaways.
* One-minute revision.

Copying occurs only after explicit user action.

The frontend uses the browser Clipboard API.

The frontend uses safe DOM APIs and does not use `innerHTML`.

Copy success and failure feedback is sanitized.

## 40.3 PDF Export

PDF Export is implemented through:

`POST /api/v1/notes/export/pdf`

The request body reuses the existing `NotesResponse` schema.

The endpoint returns:

* `Content-Type: application/pdf`
* `Content-Disposition: attachment; filename="mindcraft-notes.pdf"`
* Generated PDF bytes.

PDF generation is isolated in:

`backend/app/services/notes_export_service.py`

The export service uses ReportLab Platypus and `io.BytesIO`.

PDF generation is entirely in memory.

No temporary files are written.

Generated notes and PDF bytes are not persisted to disk, a database, object storage, or any other storage layer.

PDF Export does not call Gemini.

PDF Export does not regenerate notes.

Existing reading-time logic is unchanged.

The generated PDF contains the complete `NotesResponse` content:

* Title.
* Estimated reading time.
* Table of contents.
* Every section.
* Section headings.
* Section content.
* Key points.
* Definitions.
* Examples.
* Memory tricks.
* Common mistakes.
* Summary.
* Key takeaways.
* One-minute revision.

The frontend sends the latest successful `NotesResponse` to the export endpoint, receives the PDF response as a `Blob`, creates an object URL, triggers a browser download named `mindcraft-notes.pdf`, and revokes the object URL after starting the download.

## 40.4 Dependencies

Milestone 4 adds:

* `reportlab`

No frontend PDF library is added.

## 40.5 Testing and Verification

Previous automated backend test result before Milestone 4:

**54 tests passing.**

Milestone 4 adds 9 automated tests.

Final automated backend test result after Milestone 4:

**63 tests passing.**

Automated tests cover:

* Successful PDF generation.
* PDF return type as bytes.
* Non-empty PDF output.
* `%PDF-` byte signature.
* PDF parseability using `pypdf`.
* Representative complete PDF content, including title, estimated reading time, table of contents, section content, key points, definitions, examples, memory tricks, common mistakes, summary, key takeaways, and one-minute revision.
* PDF generation isolation from Gemini.
* Unexpected programming-error propagation.
* Export endpoint HTTP 200 success behavior.
* `application/pdf` response content type.
* `Content-Disposition` attachment filename.
* PDF response body signature.
* Native FastAPI/Pydantic HTTP 422 behavior for invalid request bodies.
* Missing required nested content validation.
* Endpoint unexpected-error behavior.

Additional verification completed:

* JavaScript syntax checks passed.
* Application import succeeds.
* `GET /api/v1/health` succeeds.
* Existing Notes endpoint regression verification passed.
* Existing document extraction endpoint regression verification passed.
* `git diff --check` passed with only LF-to-CRLF warnings.

Manual verification completed:

* Real notes generation succeeded.
* Copy Notes button state behavior passed.
* Copy Notes copied complete readable notes successfully.
* Real PDF Export browser download succeeded.
* Exported `mindcraft-notes.pdf` opened successfully and contained readable notes across multiple pages.
* PDF extraction from Milestone 3 still populated the source-text textarea.
* Notes generation from extracted PDF text succeeded.
* Copy Notes and PDF Export worked for notes generated from extracted PDF text.
* PDF extraction did not automatically generate notes.
* Failed subsequent generation preserved the latest successful `NotesResponse`, and Copy Notes and PDF Export continued to operate on that latest successful response.

## 40.6 Architecture and Security

The application remains stateless.

No generated notes or PDF bytes are persisted.

No generated notes or PDF bytes are logged.

No broad exception handling was added to mislabel programming errors.

Unexpected programming errors propagate through normal application error handling.

Native FastAPI/Pydantic HTTP 422 behavior is preserved.

Existing Gemini behavior remains unchanged.

Existing document extraction behavior remains unchanged.

No secrets are exposed.

## 40.7 Known Limitations

PDF presentation is intentionally simple.

Custom PDF themes and final visual polish remain deferred to Milestone 8.

Copy Notes depends on browser Clipboard API availability.

PDF Export exports the current/latest successful `NotesResponse` and does not regenerate notes.


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

## 42. Milestone 6 Implementation Record

Milestone 6 implements the AI-powered Quiz workflow and extends the existing study loop with a deterministic, frontend-driven interactive assessment while preserving the Version 1 architecture and design principles.

## 42.1 Milestone 6 Scope

Milestone 6 implements:

* Structured quiz generation grounded in generated notes.
* A dedicated Quiz API route and thin controller.
* Prompt-building logic for quiz generation.
* A Quiz service that calls Gemini and validates structured output.
* Deterministic question-count selection performed outside Gemini.
* Client-side quiz interaction (one question at a time, MCQs).
* Immutable per-question submission state persisted in browser memory.
* Deterministic scoring calculated by application logic.
* Completion summary and local Restart/Generate-New-Quiz behaviors.

Milestone 6 preserves:

* Existing Notes, Flashcards, and PDF workflows.
* Stateless application architecture (no DB, no auth).
* Prompt construction separated from Gemini communication.

Milestone 6 does not add:

* Persistence or server-side session state.
* Authentication.
* Timers, leaderboards, analytics, gamification, or quiz export.
* Weak-topic Teach Me, Focused Revision, or Retest flows (deferred to Milestone 7).

## 42.2 Backend Architecture

The backend additions follow the established thin-route / service / prompt / Gemini / validation pattern:

* `POST /api/v1/quiz/generate` — thin API route that validates the request and forwards to the quiz service.
* `backend/app/prompts/quiz.py` — prompt builder that grounds the quiz in the latest `NotesResponse` and instructs Gemini to emit structured JSON for each question.
* `backend/app/services/quiz_service.py` — orchestration layer that selects question count deterministically, composes the prompt, calls the Gemini service, parses and validates the structured output, and returns a `QuizResponse`.
* Gemini errors and invalid responses are mapped to sanitized HTTP errors consistent with existing Gemini error conventions.

The backend remains stateless; deterministic logic (question count selection and scoring) is implemented in application code rather than relying on Gemini.

## 42.3 Grounding Strategy

Quiz generation is explicitly grounded in the latest successful `NotesResponse` provided by the frontend. The prompt:

* Supplies the generated notes as the sole grounding material.
* Requests an exact number of multiple-choice questions.
* Requires four answer options per question and a single correct answer.
* Includes brief explanations and a concept/topic label per question for downstream weak-topic analysis (Milestone 7).

## 42.4 Deterministic Question-Count Selection

The target question count is chosen by deterministic application logic (based on notes length/complexity) outside Gemini. Gemini is instructed to return exactly the requested number of questions; no randomness is introduced by the backend prompt composition.

## 42.5 Frontend Integration

Frontend changes are additive and preserve the existing UI architecture:

* `Generate Quiz` is enabled only after a successful `NotesResponse` exists.
* The frontend posts the latest `NotesResponse` to the quiz endpoint to request a `QuizResponse`.
* The latest successful `QuizResponse` is stored in-memory in the browser only.
* The UI presents one question at a time with four answer choices, Previous/Next navigation, progress indicator, and a Submit button.

Immutable per-question submission state:

* Each question maintains its own state object `{ selectedAnswer, submittedAnswer, isCorrect, explanation, isSubmitted }`.
* On first submission the answer is recorded, evaluated against the known `correct_answer`, and the result (correct/incorrect) and explanation are stored on the question object.
* Submitted answers disable further interaction for that question (choices and Submit button) and persist when navigating away and back.

Score tracking and completion behavior:

* Score is calculated deterministically in the frontend and only changes on the first submission for each question.
* After the last unanswered question is submitted the UI enters a quiz-complete state:
    - The question text, answer choices, Submit button, explanation, and navigation controls are hidden.
    - A quiz summary is shown containing final score, percentage, correct count, incorrect count, and controls to Restart Quiz or Generate New Quiz.
* `Restart Quiz` resets per-question answers and score but preserves the existing `QuizResponse` (no Gemini call).
* `Generate New Quiz` requests a fresh `QuizResponse` from the backend, replacing the previous quiz and resetting all quiz state.

Failed quiz generation preserves the latest successful quiz state (no destructive replacement on error).

## 42.6 Testing and Verification

Automated verification performed on Milestone 6:

* Previous backend suite after Milestone 5: **73 tests passing**.
* Milestone 6 added 12 backend tests.
* Final backend suite after Milestone 6: **85 tests passing**.
* Frontend syntax checks: `node --check frontend/js/api.js` and `node --check frontend/js/main.js` completed successfully.
* `git diff --check` ran and returned only the existing LF-to-CRLF warning for `frontend/css/style.css`.

Manual verification completed (representative):

* Notes generation succeeded and was used as grounding for quiz generation.
* Quiz generation succeeded and returned a validated structured `QuizResponse`.
* Correct-answer submission recorded and displayed success feedback and explanation.
* Incorrect-answer submission recorded and displayed the correct answer and explanation.
* Submitted answers became immutable and persisted across navigation.
* Score updated only on first submission per question; revisiting questions did not alter score.
* Completion summary displayed final score, percentage, correct and incorrect counts.
* Completion UI hides question UI and navigation controls so only the summary remains.
* `Restart Quiz` reset answers, score, navigation, and exited the complete state without calling Gemini.
* `Generate New Quiz` replaced the quiz, reset state, and exited the complete state.

## 42.7 Architecture and Security

* The application remains stateless for Version 1; no server-side persistence or user accounts were added.
* Gemini API keys remain backend-only; no secrets were added to the frontend or repository.
* Prompt-building, Gemini calls, and structured-response validation remain inside backend services.
* Deterministic application logic (question-count selection and scoring) runs in application code rather than relying on Gemini.

## 42.8 Known Limitations

Milestone 6 intentionally does NOT add:

* Persistence or server-side session state.
* Weak-topic Teach Me, Focused Revision, or Retest flows (deferred to Milestone 7).
* Spaced repetition, gamification, timers, leaderboards, or analytics.

These adaptive-learning features are in scope for Milestone 7 and were explicitly deferred.

## 42.9 Files Created and Modified During Milestone 6

Files created during Milestone 6:

* `backend/app/api/v1/quiz.py`
* `backend/app/prompts/quiz.py`
* `backend/app/schemas/quiz.py`
* `backend/app/services/quiz_service.py`
* `backend/tests/test_quiz.py`

Files modified during Milestone 6:

* `backend/app/api/v1/__init__.py`
* `frontend/css/style.css`
* `frontend/index.html`
* `frontend/js/api.js`
* `frontend/js/main.js`

These files were added/edited as part of the milestone implementation; according to repository state the new backend quiz files are present in the working tree but not yet committed.

## 38.7 Milestone Plan Status

Current milestone status:

* Milestone 1 â€” Foundation: **Complete**
* Milestone 2 â€” Notes Vertical Slice: **Complete**
* Milestone 3 â€” PDF Input: **Complete**
* Milestone 4 â€” Notes Utilities: **Complete, with reading time completed early during Milestone 2**
* Milestone 5 â€” Flashcards: **Complete**
* Milestone 6 â€” Quiz: **Complete**
* Milestone 7 â€” Adaptive Revision: **Not Started**
* Milestone 8 â€” Polish: **Not Started**
* Milestone 9 — Reading Themes: **Complete**
  * Milestone 10 — Configurable Quiz and Flashcards: **Complete**
  * Milestone 11 — Theme-Aware PDF Export: **Complete**
  * Milestone 10 — Configurable Quiz & Flashcards: **Complete**
  * Milestone 11 — Theme-Aware PDF Export: **Complete**
* Milestone 10 â€” Documentation: **Not Started**

Milestones 1 through 6 are complete.

Do not modify completed milestone functionality during documentation maintenance except to accurately document implemented behavior.

## 38.9 Current Development Rules

All future work must preserve the following verified decisions:

* Keep the application stateless for Version 1.
* Do not add authentication.
* Do not add a database.
* Do not add history storage.
* Do not introduce a frontend framework.
* Do not add unnecessary architectural layers.
* Keep API routes thin.
* Keep AI SDK interaction inside services.
* Keep prompt construction separate from Gemini SDK communication.
* Keep deterministic application logic outside Gemini.
* Preserve centralized configuration.
* Preserve versioned `/api/v1` routing.
* Preserve lazy Gemini client initialization.
* Preserve sanitized client-facing errors.
* Preserve sanitized backend logging.
* Never expose secrets.
* Never log user source material, full prompts, or generated content.
* Inspect existing working code before modifying it.
* Preserve completed Milestone 1 through Milestone 6 behavior.
* Implement one milestone or clearly bounded task at a time.

## 38.10 Current Repository State

Verified completed milestone commits:

```text
12d1d63 milestone 1 completed
8868ecb milestone 2 completed
0c243b6 milestone 3 completed
1b34629 milestone 4 completed
cd43645 milestone 5 completed
```

The repository working tree was clean immediately after the Milestone 5 commit.

Milestone 6 implementation status (working-tree state):

* Milestone 6 (Quiz) implementation and verification are complete in the workspace, but the changes have not been committed yet. The new backend quiz files and frontend edits are present in the working tree (uncommitted) on branch `milestone-6-quiz` according to the local workspace state.

Files added during the Milestone 6 work (uncommitted in the working tree):

* backend/app/api/v1/quiz.py
* backend/app/prompts/quiz.py
* backend/app/schemas/quiz.py
* backend/app/services/quiz_service.py
* backend/tests/test_quiz.py

* Completion summary and local Restart/Generate-New-Quiz behaviors.

Milestone 6 preserves:

* Existing Notes, Flashcards, and PDF workflows.
* Stateless application architecture (no DB, no auth).
* Prompt construction separated from Gemini communication.

Milestone 6 does not add:

* Persistence or server-side session state.
* Authentication.
* Timers, leaderboards, analytics, gamification, or quiz export.
* Weak-topic Teach Me, Focused Revision, or Retest flows (deferred to Milestone 7).

## 42.2 Backend Architecture

The backend additions follow the established thin-route / service / prompt / Gemini / validation pattern:

* `POST /api/v1/quiz/generate` — thin API route that validates the request and forwards to the quiz service.
* `backend/app/prompts/quiz.py` — prompt builder that grounds the quiz in the latest `NotesResponse` and instructs Gemini to emit structured JSON for each question.
* `backend/app/services/quiz_service.py` — orchestration layer that selects question count deterministically, composes the prompt, calls the Gemini service, parses and validates the structured output, and returns a `QuizResponse`.
* Gemini errors and invalid responses are mapped to sanitized HTTP errors consistent with existing Gemini error conventions.

The backend remains stateless; deterministic logic (question count selection and scoring) is implemented in application code rather than relying on Gemini.

## 42.3 Grounding Strategy

Quiz generation is explicitly grounded in the latest successful `NotesResponse` provided by the frontend. The prompt:

* Supplies the generated notes as the sole grounding material.
* Requests an exact number of multiple-choice questions.
* Requires four answer options per question and a single correct answer.
* Includes brief explanations and a concept/topic label per question for downstream weak-topic analysis (Milestone 7).

## 42.4 Deterministic Question-Count Selection

The target question count is chosen by deterministic application logic (based on notes length/complexity) outside Gemini. Gemini is instructed to return exactly the requested number of questions; no randomness is introduced by the backend prompt composition.

## 42.5 Frontend Integration

Frontend changes are additive and preserve the existing UI architecture:

* `Generate Quiz` is enabled only after a successful `NotesResponse` exists.
* The frontend posts the latest `NotesResponse` to the quiz endpoint to request a `QuizResponse`.
* The latest successful `QuizResponse` is stored in-memory in the browser only.
* The UI presents one question at a time with four answer choices, Previous/Next navigation, progress indicator, and a Submit button.

Immutable per-question submission state:

* Each question maintains its own state object `{ selectedAnswer, submittedAnswer, isCorrect, explanation, isSubmitted }`.
* On first submission the answer is recorded, evaluated against the known `correct_answer`, and the result (correct/incorrect) and explanation are stored on the question object.
* Submitted answers disable further interaction for that question (choices and Submit button) and persist when navigating away and back.

Score tracking and completion behavior:

* Score is calculated deterministically in the frontend and only changes on the first submission for each question.
* After the last unanswered question is submitted the UI enters a quiz-complete state:
    - The question text, answer choices, Submit button, explanation, and navigation controls are hidden.
    - A quiz summary is shown containing final score, percentage, correct count, incorrect count, and controls to Restart Quiz or Generate New Quiz.
* `Restart Quiz` resets per-question answers and score but preserves the existing `QuizResponse` (no Gemini call).
* `Generate New Quiz` requests a fresh `QuizResponse` from the backend, replacing the previous quiz and resetting all quiz state.

Failed quiz generation preserves the latest successful quiz state (no destructive replacement on error).

## 42.6 Testing and Verification

Automated verification performed on Milestone 6:

* Previous backend suite after Milestone 5: **73 tests passing**.
* Milestone 6 added 12 backend tests.
* Final backend suite after Milestone 6: **85 tests passing**.
* Frontend syntax checks: `node --check frontend/js/api.js` and `node --check frontend/js/main.js` completed successfully.
* `git diff --check` ran and returned only the existing LF-to-CRLF warning for `frontend/css/style.css`.

Manual verification completed (representative):

* Notes generation succeeded and was used as grounding for quiz generation.
* Quiz generation succeeded and returned a validated structured `QuizResponse`.
* Correct-answer submission recorded and displayed success feedback and explanation.
* Incorrect-answer submission recorded and displayed the correct answer and explanation.
* Submitted answers became immutable and persisted across navigation.
* Score updated only on first submission per question; revisiting questions did not alter score.
* Completion summary displayed final score, percentage, correct and incorrect counts.
* Completion UI hides question UI and navigation controls so only the summary remains.
* `Restart Quiz` reset answers, score, navigation, and exited the complete state without calling Gemini.
* `Generate New Quiz` replaced the quiz, reset state, and exited the complete state.

## 42.7 Architecture and Security

* The application remains stateless for Version 1; no server-side persistence or user accounts were added.
* Gemini API keys remain backend-only; no secrets were added to the frontend or repository.
* Prompt-building, Gemini calls, and structured-response validation remain inside backend services.
* Deterministic application logic (question-count selection and scoring) runs in application code rather than relying on Gemini.

## 42.8 Known Limitations

Milestone 6 intentionally does NOT add:

* Persistence or server-side session state.
* Weak-topic Teach Me, Focused Revision, or Retest flows (deferred to Milestone 7).
* Spaced repetition, gamification, timers, leaderboards, or analytics.

These adaptive-learning features are in scope for Milestone 7 and were explicitly deferred.

## 42.9 Files Created and Modified During Milestone 6

Files created during Milestone 6:

* `backend/app/api/v1/quiz.py`
* `backend/app/prompts/quiz.py`
* `backend/app/schemas/quiz.py`
* `backend/app/services/quiz_service.py`
* `backend/tests/test_quiz.py`

Files modified during Milestone 6:

* `backend/app/api/v1/__init__.py`
* `frontend/css/style.css`
* `frontend/index.html`
* `frontend/js/api.js`
* `frontend/js/main.js`

These files were added/edited as part of the milestone implementation; according to repository state the new backend quiz files are present in the working tree but not yet committed.

## 38.7 Milestone Plan Status

Current milestone status:

* Milestone 1 — Foundation: **Complete**
* Milestone 2 — Notes Vertical Slice: **Complete**
* Milestone 3 — PDF Input: **Complete**
* Milestone 4 — Notes Utilities: **Complete, with reading time completed early during Milestone 2**
* Milestone 5 — Flashcards: **Complete**
* Milestone 6 — Quiz: **Complete**
* Milestone 7 — Adaptive Revision: **Not Started**
* Milestone 8 — Polish: **Not Started**
* Milestone 9 — Reading Themes: **Complete**
  * Milestone 10 — Configurable Quiz and Flashcards: **Complete**
  * Milestone 11 — Theme-Aware PDF Export: **Complete**
  * Milestone 10 — Configurable Quiz & Flashcards: **Complete**
  * Milestone 11 — Theme-Aware PDF Export: **Complete**
* Milestone 10 — Documentation: **Not Started**

Milestones 1 through 6 are complete.

Do not modify completed milestone functionality during documentation maintenance except to accurately document implemented behavior.

## 38.9 Current Development Rules

All future work must preserve the following verified decisions:

* Keep the application stateless for Version 1.
* Do not add authentication.
* Do not add a database.
* Do not add history storage.
* Do not introduce a frontend framework.
* Do not add unnecessary architectural layers.
* Keep API routes thin.
* Keep AI SDK interaction inside services.
* Keep prompt construction separate from Gemini SDK communication.
* Keep deterministic application logic outside Gemini.
* Preserve centralized configuration.
* Preserve versioned `/api/v1` routing.
* Preserve lazy Gemini client initialization.
* Preserve sanitized client-facing errors.
* Preserve sanitized backend logging.
* Never expose secrets.
* Never log user source material, full prompts, or generated content.
* Inspect existing working code before modifying it.
* Preserve completed Milestone 1 through Milestone 6 behavior.
* Implement one milestone or clearly bounded task at a time.

## 38.10 Current Repository State

Verified completed milestone commits:

```text
12d1d63 milestone 1 completed
8868ecb milestone 2 completed
0c243b6 milestone 3 completed
1b34629 milestone 4 completed
cd43645 milestone 5 completed
```

The repository working tree was clean immediately after the Milestone 5 commit.

Milestone 6 implementation status (working-tree state):

* Milestone 6 (Quiz) implementation and verification are complete in the workspace, but the changes have not been committed yet. The new backend quiz files and frontend edits are present in the working tree (uncommitted) on branch `milestone-6-quiz` according to the local workspace state.

Files added during the Milestone 6 work (uncommitted in the working tree):

* backend/app/api/v1/quiz.py
* backend/app/prompts/quiz.py
* backend/app/schemas/quiz.py
* backend/app/services/quiz_service.py
* backend/tests/test_quiz.py

Files modified during the Milestone 6 work (uncommitted changes in the working tree):

* backend/app/api/v1/__init__.py
* frontend/css/style.css
* frontend/index.html
* frontend/js/api.js
* frontend/js/main.js

Do not assume these Milestone 6 changes are recorded in a commit; the implementation record above documents the completed work and verification, but no Milestone 6 commit hash is provided here.

## Milestone 8 - Phase 3

* **Root cause of the workspace bug**: The application uses a two-layer visibility architecture (wrapper panels like `workspace-panel-notes` and internal output sections like `notes-output`). The bug occurred because `*-output` sections were initialized with the `hidden` attribute in HTML, and functions like `clearAdaptiveCycleState` explicitly re-hid some internal sections (`revisionOutputEl.hidden = true`). As a result, switching to a tab like Notes would display the `workspace-panel-notes` wrapper, but because `notes-output` was hidden internally, the screen appeared empty to the user (no content, no empty state).
* **Workspace architecture**: Removed all `hidden` attributes from the inner `*-output` sections in HTML. Tab switching (`switchWorkspaceTab`) is now purely for navigation, managing visibility exclusively on the wrapper `div` panels without ever touching internal state or calling rendering functions.
* **Empty state architecture**: Implemented explicit empty states internally with functions like `renderNotesEmptyState()`, separating them completely from populated response functions (`renderNotesResponse()`). The rule of "No Silent Fallback Rendering" is established: renderers only accept valid populated data, prohibiting them from fabricating UI state or mutating application state.
* **Quiz progress redesign**: Replaced verbose stats during the quiz with Answered, Correct, Wrong, and Remaining. Moved the final score and percentage to `updateQuizSummary()` to display large and centered upon completion.
* **Quiz completion flow**: Quiz summary is strictly gated to display only when `submittedCount == totalQuestions`. Uncompleted quizzes display a warning and a "Go To First Unanswered" button while remaining interactive.
* **Go To First Unanswered**: Added logic to correctly search through the active quiz states (`getActiveQuizStates()`) to locate the first unsubmitted question index and update `quizIndex` accordingly, working across both original quizzes and retests.
* **Keyboard navigation**: Implemented ARIA-compliant left/right arrow key navigation across workspace tabs.
* **Automatic workspace routing**: After successfully generating Notes, Flashcards, Quizzes, or Revision, the Learning Workspace wrapper is automatically revealed and the active tab is switched appropriately.
* **Final summary redesign**: Replaced flat text blocks with a clean score interface and `details`/`summary` collapsible elements for incorrect answer reviews.