<div align="center">
  <!-- TODO: Insert Logo Image Here -->
  <img src="frontend/favicon.svg" alt="MindCraft AI Logo" width="120" />
  
  <h1>MindCraft AI</h1>
  
  <p>
    <strong>Transform static study material into interactive, AI-powered learning experiences.</strong>
  </p>
  
  <p>
    <a href="https://github.com/yourusername/MindCraft-AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
    <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi" alt="FastAPI"></a>
    <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat&logo=javascript&logoColor=black" alt="Vanilla JS"></a>
    <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=flat&logo=google&logoColor=white" alt="Powered by Gemini"></a>
  </p>
  
  <p>
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#installation">Installation</a> •
    <a href="#deployment">Deployment</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## 📖 Overview

**MindCraft AI** is an intelligent educational workspace designed to solve the problem of passive reading. By leveraging Google's Gemini LLMs and Native Structured Outputs, MindCraft AI instantly parses uploaded academic texts and textbook chapters, generating highly structured study notes, interactive flashcards, dynamic quizzes, and adaptive revision paths targeting weak concepts.

Built with a blazing-fast stateless architecture, it pairs a pure Vanilla JS frontend with a robust FastAPI backend, ensuring maximum performance without framework bloat.

---

## ✨ Features

- **📄 Intelligent PDF Extraction:** Robust parsing of academic PDFs to extract raw study material.
- **📝 Structured Notes Generation:** LLM-generated study guides broken down into headings, key points, definitions, examples, and memory tricks.
- **📇 Active Recall Flashcards:** Interactive, flippable flashcards with adjustable difficulty levels.
- **🧠 Dynamic Quizzing & Weak Concept Detection:** Multiple-choice quizzes that evaluate your answers in real-time, extracting your "weak topics" based on incorrect responses.
- **🔄 Adaptive Revision & Retesting:** Automatically generates targeted revision prompts and new quizzes specifically focused on the topics you struggled with.
- **🖨️ PDF Export:** Export your generated notes to beautifully formatted PDFs via headless Chromium (Playwright).
- **🎨 Theming System:** Built-in Academic and Dark themes for comfortable long-form reading.

---

## 📸 Screenshots

*(Replace with actual URLs once hosted)*

- **Workspace Dashboard:** `![Dashboard Screenshot](link)`
- **Interactive Flashcards:** `![Flashcards Screenshot](link)`
- **Dynamic Quizzes:** `![Quiz Screenshot](link)`
- **PDF Export Preview:** `![PDF Export Screenshot](link)`

---

## 🏗️ Architecture & Tech Stack

MindCraft AI uses a **stateless, monolithic architecture** optimized for AI generation. 

- **Frontend:** Vanilla HTML5, CSS3 (CSS Variables for theming), and ES6 JavaScript. No bundlers, no complex state management libraries—just pure performance.
- **Backend:** Python 3.11+ running **FastAPI**. Heavily utilizes **Pydantic** for rigid validation of LLM outputs.
- **AI Integration:** Google Gemini (`gemini-3.1-flash-lite`) integrated via the official GenAI SDK, using Strict JSON Schemas for deterministic responses.
- **PDF Generation:** Playwright (Headless Chromium) for high-fidelity HTML-to-PDF rendering.

*For a deep dive into the system design, see [ARCHITECTURE.md](ARCHITECTURE.md).*

---

## 📂 Folder Structure

```text
MindCraft-AI/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # FastAPI Route Controllers
│   │   ├── core/           # Configuration & CORS
│   │   ├── prompts/        # Prompt Engineering & System Instructions
│   │   ├── schemas/        # Pydantic Output Schemas
│   │   └── services/       # Business Logic & LLM Integration
│   ├── requirements.txt
│   └── build.sh            # Production build script
├── frontend/
│   ├── css/style.css       # Design System & Theming
│   ├── js/
│   │   ├── api.js          # Fetch API Wrappers
│   │   └── main.js         # DOM Manipulation & State
│   └── index.html          # SPA Entry Point
├── DEPLOYMENT_GUIDE.md     # CI/CD Instructions
├── PROJECT_SHOWCASE.md     # Technical Showcase Document
└── ARCHITECTURE.md         # Detailed System Architecture
```

---

## 🚀 Installation & Local Development

### Prerequisites
- Python 3.11+
- Google Gemini API Key

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/MindCraft-AI.git
cd MindCraft-AI/backend

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Playwright dependencies for PDF export
playwright install chromium

# Configure Environment
cp .env.example .env
# Edit .env and insert your GEMINI_API_KEY
```

### 2. Start the Backend Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*The API documentation will be available at `http://127.0.0.1:8000/docs`.*

### 3. Start the Frontend Server
Open a new terminal window in the repository root:
```bash
cd frontend
python -m http.server 5500
```
*Navigate to `http://127.0.0.1:5500` in your browser.*

---

## 🌍 Deployment

MindCraft AI is fully configured for automated CI/CD:
- **Frontend:** Deploy to **Vercel** (uses `vercel.json` for API rewrites).
- **Backend:** Deploy to **Render** via Blueprint (`render.yaml`).

Please read the complete [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

---

## 🔮 Future Roadmap

- **User Authentication:** Save generated study decks via PostgreSQL / Supabase.
- **Spaced Repetition System (SRS):** Implement Anki-style algorithms for flashcards.
- **Multi-modal Support:** Analyze diagrams and images from PDFs.
- **Streaming Responses:** Implement SSE for real-time generation feedback.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**[Your Name / Alias]**  
*Lead Product Engineer*  
[LinkedIn Profile] • [GitHub Profile] • [Portfolio Link]
