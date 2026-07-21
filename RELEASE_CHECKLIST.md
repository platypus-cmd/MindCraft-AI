# MindCraft AI Release Checklist

Use this checklist to verify a successful production deployment.

## Infrastructure
- [ ] Push to GitHub
- [ ] Deploy Render
- [ ] Deploy Vercel
- [ ] Add environment variables (`GEMINI_API_KEY`, `CORS_ALLOWED_ORIGINS`, `PYTHON_VERSION`)

## Core Features (E2E Testing)
- [ ] Verify PDF Upload (Upload a small test PDF and verify text extraction)
- [ ] Verify Notes (Generate notes from the extracted text)
- [ ] Verify PDF Export (Download the generated notes as a PDF)
- [ ] Verify Flashcards (Generate 5 flashcards on normal difficulty)
- [ ] Verify Quiz (Generate a 5-question quiz and complete it)
- [ ] Verify Revision (Ensure weak topics are identified and revision triggers correctly)
- [ ] Verify Retest (Ensure generating a retest focuses on weak topics)

## Cross-Platform Validation
- [ ] Test mobile (Verify responsive layout and navigation on a mobile viewport)
- [ ] Test desktop (Verify grid layouts and hover states on desktop)
- [ ] Test error handling (Trigger an intentional error, e.g. upload a massive non-PDF, verify a toast error message appears rather than a raw stack trace)
- [ ] Verify README (Ensure the repo documentation is clean and ready for public viewing)
- [ ] IBM submission ready (Final sign-off once all tests pass)
