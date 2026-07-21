# MindCraft AI

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4.svg?style=flat-square&logo=google-gemini)](https://ai.google.dev/)
[![Playwright](https://img.shields.io/badge/PDF%20Renderer-Playwright-2EAD33.svg?style=flat-square&logo=playwright)](https://playwright.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](#license)

**MindCraft AI** is an AI-powered personalized learning workspace designed to transform standard study materials into structured, adaptive educational assets. By leveraging Google's Gemini LLMs, MindCraft AI goes beyond simple textbook summaries to act as an expert private tutor—tailoring notes, generating quizzes, building flashcards, and identifying knowledge gaps for university-level exam preparation.

---

## 🚀 Key Features

### 📚 Adaptive Study Notes
*   **Dynamic Customization**: Personalize study materials by selecting **Learning Goals** (Academic, Exam Revision, Deep Understanding, Simple Explanations), **Knowledge Levels** (Beginner, Intermediate, Advanced), and **Note Lengths** (Quick Review, Standard, Comprehensive).
*   **Concept-First Teaching**: Structured around university syllabus dimensions: Definition, Mechanism, Application, and Distinctions.
*   **Rich Markdown Support**: Full inline formatting including headings, bold keywords, bullet lists, blockquotes, and code snippets.
*   **Reading Time Estimation**: Dynamic word-count analysis calculated on the backend to plan study sessions.

### 🧪 Active Recall & Practice
*   **Flashcards**: Automated generation of concept-focused flashcards targeting active recall.
*   **Interactive Quizzes**: Multiple-choice testing based directly on the generated notes.
*   **Adaptive Revision**: Analyze incorrect quiz answers to automatically generate targeted revision guides focusing on weak spots.
*   **Retests**: Generate custom follow-up tests specifically targeting previously missed concepts to reinforce learning.

### 🎨 Themes & Export
*   **Reading Themes**: Toggle between multiple study aesthetics (Plain, Academic, Futuristic, Dark, Vintage, Notebook).
*   **Production-Grade PDF Export**: Renders notes with themes faithfully preserved using an in-memory headless Chromium pipeline powered by Playwright.

---

## 📸 Interface Preview

### Home Workspace


### Generated Notes & Active Themes


### Flashcards & Active Recall


### Quiz & Weak Concept Detection


### PDF Export


---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Vanilla JS / CSS3 / HTML5 | Lightweight single-page app with dynamic DOM updates |
| **Markdown** | Marked.js | Fast, secure rendering of markdown in browser |
| **Backend** | FastAPI | High-performance Python ASGI web framework |
| **AI Integration** | Google GenAI SDK | Orchestration and content generation using Gemini 2.5 |
| **Validation** | Pydantic | Strict, structured JSON schema parsing and verification |
| **PDF Extraction** | PyMuPDF (fitz) | Efficient server-side parsing of uploaded study guides |
| **PDF Export** | Playwright (Chromium) | Headless print-to-PDF engine preserving full styles |
| **Telemetry** | Custom Benchmarking | Automated sweep profiling for prompt latency and token consumption |

---

## 📐 Architecture Flow

```text
       [ User Uploads PDF / Paste Text ]
                       │
                       ▼
            [ FastAPI Backend API ]
                       │
                       ▼
       [ Prompt Builder (Personalization) ]
                       │
                       ▼
         [ Gemini Structured Output ]
                       │
                       ▼
       [ Pydantic Schema Validation ]
                       │
                       ▼
    [ Frontend / HTML5 + Theme Render ] ────► [ Playwright PDF Export ]
```

---

## ⚙️ Installation & Setup

### Backend (FastAPI)

1. Navigate to the backend directory and set up a virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Initialize your local configuration:
   ```bash
   cp .env.example .env
   ```

3. Configure your Google AI Studio Gemini API Key inside `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   GEMINI_TIMEOUT_SECONDS=30
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend (Static Client)

1. Launch a static web server from the repository root:
   ```bash
   python -m http.server 5500 --directory frontend
   ```
2. Open `http://127.0.0.1:5500` in your web browser.

---

## 📊 Benchmarking Framework

MindCraft AI includes an automated telemetry profiling suite to run performance matrices. It tests latency, token consumption (input, output, total), validation overhead, and error rates across all supported configurations.

To run the telemetry suite:
```bash
cd backend
python ../scripts/benchmark.py
```
This will automatically generate a detailed Markdown profiling report (`benchmark_report.md`) and a comma-separated database (`benchmark_results.csv`) in the repository root.

---

## 📂 Project Structure

```text
MindCraft-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # Route controllers (notes, documents, export, revision, quiz, flashcards)
│   │   ├── core/         # App configuration settings and constants
│   │   ├── prompts/      # AI prompt templates & custom persona engineering
│   │   ├── schemas/      # Pydantic schema validation models
│   │   └── services/     # Core engines (gemini, doc parser, export, SRS, etc.)
│   ├── tests/            # Test suite (endpoint validation, parsing integrity)
│   └── requirements.txt
├── frontend/
│   ├── css/              # Workspace style sheets & reading themes
│   ├── js/               # API clients and UI handlers (api.js, main.js)
│   └── index.html        # Main app workspace interface
└── scripts/
    └── benchmark.py      # Telemetry & performance sweep benchmarker
```

---

## 🗺️ Project Roadmap

- [x] Core dynamic note personalization (Goal, Level, Format, Length)
- [x] Pydantic structured output validation for LLM responses
- [x] Flashcards and Quiz active recall modules
- [x] Adaptive Revision and weak concept retesting
- [x] Headless Chromium PDF Export using Playwright
- [x] Custom telemetry benchmarking framework
- [ ] Multi-document vector search (RAG)
- [ ] Stateful user profiles and study progress analytics
- [ ] Collaborative group workspaces and shareable notes

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any bug fixes, styling polishes, or feature additions.

---

## 📄 License
This project is licensed under the MIT License. See the placeholder file for details.
