# 1. What Is Already Implemented

> **ExamShield (E-Shield)** — an offline AI system that grades handwritten answer sheets using a
> trained ML model (XGBoost), **never an LLM**. Working end-to-end and committed to `main`.
>
> **Repo:** https://github.com/aishwaryaV007/E-Shield · **Track:** 02 — Predictive Analytics (ML/DL)

---

## Two-model core

### Model A — Reader (pretrained, reads the paper)
- **TrOCR-large-handwritten** for handwriting OCR.
- **OpenCV** line/region segmentation to split a page into questions and answers.
- **MiniLM (`all-MiniLM-L6-v2`)** sentence embeddings for semantic similarity.
- **Hungarian / dynamic-programming** matching to align each student answer to the correct key entry.
- Output: per-question student text + a matching/similarity score.

### Model B — Marker (our trained model, decides the mark)
- **XGBoost** regressor trained on the **Mohler ASAG dataset** (2,442 graded answers).
- Predicts `mark_percentage` (0–1), scaled to each question's max marks; marks rounded to nearest 0.5.
- Engineered features: semantic similarity, key-concept coverage, keyword recall, missing/extra points.
- Metrics: **RMSE ≈ 0.19**, **R² ≈ +0.12** on a held-out split.

## Backend — FastAPI (`:8000`)
- `POST /api/v1/grade` — upload answer PDF (+ optional answer key / question paper) → evaluated sheet.
- `POST /api/v1/rescore` — re-grade after a human edits the extracted text (no OCR re-run).
- `GET /health`, `POST /api/v1/auth/token`.
- Handles both **CSV answer keys** and **prose (.txt) answer keys** (format-agnostic grader).
- Security utilities: JWT auth (bypass-able for demo via `DISABLE_AUTH`), rate limiting, DB backup helper, centralized logging.

## Frontends
- **Web (Next.js):** class-roster dashboard — add/rename students, per-student PDF upload, grade one / grade all, class statistics, letter-grade badges, CSV export, per-question edit + re-grade.
- **Mobile (`examshield-mobile2`, React Native / Expo SDK 54):** the same roster dashboard on mobile, wired to the backend, auto-detecting the API host. **This is the canonical mobile app.**

## Engineering & quality
- End-to-end test + backend test suite (pytest) passing.
- **GitHub Actions CI** (install + tests).
- Runs **fully offline** on CPU/MPS after a one-time model download.

## Live-verified result
A real test script graded **23.5 / 25 = 94% (Grade A+)** across 5 questions in ~30 s (first grade includes the one-time OCR model load).

---
*See also: [02_TO_BE_IMPLEMENTED](02_TO_BE_IMPLEMENTED.md) · [04_WORKING_PROCESS](04_WORKING_PROCESS.md)*
