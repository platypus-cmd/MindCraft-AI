# MindCraft AI — Project Context

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

**Understand → Study → Test → Identify Weaknesses → Revise → Retest**

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

**Understand → Study → Test → Identify Weaknesses → Revise → Retest**

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

## Milestone 1 — Foundation

* Repository setup.
* Backend skeleton.
* Frontend skeleton.
* Environment configuration.
* Health endpoint.
* Local frontend-backend communication.

## Milestone 2 — Notes Vertical Slice

* Text input.
* Learning preference controls.
* Prompt builder.
* Gemini integration.
* Notes generation.
* Notes rendering.
* Error handling.

At the end of this milestone, the application must already perform one complete useful workflow.

## Milestone 3 — PDF Input

* PDF validation.
* Text extraction.
* Extracted content to note generation.

## Milestone 4 — Notes Utilities

* Reading time.
* Copy notes.
* PDF export.

## Milestone 5 — Flashcards

* Structured flashcard generation.
* Validation.
* Interactive flashcard UI.

## Milestone 6 — Quiz

* Quiz configuration.
* Structured quiz generation.
* Interactive quiz.
* Deterministic scoring.
* Answer review.
* Weak concept extraction.

## Milestone 7 — Adaptive Revision

* Focused revision generation.
* Weak-topic learning UI.
* Retest generation.
* Retest interaction.

## Milestone 8 — Polish

* Responsive design.
* Accessibility review.
* Loading states.
* Error states.
* Performance improvements.
* UI consistency.

## Milestone 9 — Deployment

* AWS Elastic Beanstalk configuration.
* Production environment variables.
* Deployment.
* Live application testing.

## Milestone 10 — Documentation

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
