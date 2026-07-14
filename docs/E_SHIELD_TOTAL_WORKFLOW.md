# ExamShield (E-Shield) — Total Workflow & Project Overview

> **ExamShield** is an **offline AI system** that learns how teachers grade from previously
> corrected answer sheets, then automatically evaluates new scanned **handwritten** scripts —
> assigning question-wise marks, a total, a percentage, and per-answer feedback.
>
> **Hackathon track:** 02 — Predictive Analytics (ML / DL)
> **Repo:** https://github.com/aishwaryaV007/E-Shield
> **Core principle:** the mark is always produced by a **trained ML model (XGBoost) — never an LLM.**

---

## Table of contents
1. [What is already implemented](#1-what-is-already-implemented)
2. [What should be implemented](#2-what-should-be-implemented)
3. [Business model](#3-business-model)
4. [Working process (end-to-end)](#4-working-process-end-to-end)
5. [Feature enhancements](#5-feature-enhancements)
6. [Important information (metrics, stack, limitations)](#6-important-information)

---

## 1. What is already implemented

**Two-model core — working end-to-end and committed to `main`.**

### Model A — Reader (pretrained, reads the paper)
- **TrOCR-large-handwritten** for handwriting OCR.
- **OpenCV** line/region segmentation to split a page into questions and answers.
- **MiniLM (`all-MiniLM-L6-v2`)** sentence embeddings for semantic similarity.
- **Hungarian / dynamic-programming** matching to align each student answer to the right key entry.
- Produces per-question student text + a matching/similarity score.

### Model B — Marker (our trained model, decides the mark)
- **XGBoost** regressor trained on the **Mohler ASAG dataset** (2,442 graded answers).
- Predicts a `mark_percentage` (0–1), scaled to each question's max marks; marks rounded to nearest 0.5.
- Engineered features: semantic similarity, key-concept coverage, keyword recall, missing/extra points.

### Backend — FastAPI (`:8000`)
- `POST /api/v1/grade` — upload answer PDF (+ optional answer key / question paper) → evaluated sheet.
- `POST /api/v1/rescore` — re-grade after a human edits the extracted text (no OCR re-run).
- `GET /health`, `POST /api/v1/auth/token`.
- Handles both **CSV answer keys** and **prose (.txt) answer keys** (format-agnostic grader).
- Security utilities in place: JWT auth (bypass-able for demo via `DISABLE_AUTH`), rate limiting, DB backup helper, centralized logging.

### Frontends
- **Web (Next.js):** class-roster dashboard — add/rename students, per-student PDF upload, grade one / grade all, class statistics, letter-grade badges, CSV export, per-question edit + re-grade.
- **Mobile (`examshield-mobile2`, React Native / Expo SDK 54):** the same roster dashboard ported to mobile, wired to the backend, auto-detecting the API host. **This is the canonical mobile app.**

### Engineering & quality
- End-to-end test + backend test suite (pytest) passing.
- **GitHub Actions CI** (install + tests).
- Runs **fully offline** on CPU/MPS after a one-time model download.

---

## 2. What should be implemented

Not blockers — production-hardening and reach:

- **Throughput / parallelism** — currently single-process (~4–5 scripts/min). Add batching or a worker queue.
- **Prediction caching** — skip re-OCR/re-scoring for identical scripts.
- **Real MCQ OCR** — MCQ answers currently fall back to the digital record because scan bleed-through defeats OCR; improve preprocessing for double-sided scans.
- **More exam formats** — tune segmentation for varied layouts; assign marks to synthetic booklets so they become trainable.
- **Better Model B accuracy** — larger/cleaner training data; the current R² is modest (see §6).
- **Monitoring & alerting** — metrics dashboards on top of the existing logging.
- **Backups / disaster recovery** runbook, **RBAC**, and **role-based dashboards**.
- **Cloud/on-prem deployment packaging** (Docker) and an installer for non-technical staff.
- **Analytics** — class/cohort trends, question-difficulty analysis, examiner-consistency reports.

---

## 3. Business model

ExamShield is **offline and privacy-first**, which shapes the model toward **on-premise licensing** rather than data-in-the-cloud SaaS.

**Target customers**
- Schools, colleges, and universities (semester + internal exams)
- Government exam boards and public service commissions
- Coaching / test-prep chains (rapid mock-test grading)
- Professional certification bodies
- EdTech platforms (embed as a grading engine)

**Revenue streams**
1. **On-premise institutional license** — annual per-institution or per-campus license (fits the offline, privacy-first design; student data never leaves the site).
2. **Per-exam / per-script tier** — usage-based pricing for boards and coaching chains during exam seasons.
3. **Support & customization** — training Model B on an institution's own corrected scripts, onboarding, SLAs.
4. **Freemium / pilot** — free tier for small departments or a limited script count to drive adoption, upsell to paid.
5. **Integration licensing** — API/engine licensing to existing LMS/EdTech vendors.

**Why customers pay**
- Cuts the most labour-intensive part of evaluation (examiner time and cost).
- One learned marking standard → consistency, fewer re-evaluation disputes.
- Runs on ordinary CPU hardware (no GPU / no paid API), so low deployment cost.
- Offline operation meets data-privacy and compliance needs.

**Market pull:** India alone grades crores of handwritten scripts per year; examiner shortage, inconsistent marking, and slow turnaround are persistent, well-funded pain points.

---

## 4. Working process (end-to-end)

### Phase 1 — Training (one-time, offline)
```
Historical corrected scripts + teacher marks
+ question papers + answer keys + rubrics
        → Feature engineering (similarity, concept coverage, keyword recall, missing/extra points)
        → Train XGBoost mark-predictor
        → Evaluate (RMSE / MAE / R² / ±1-mark accuracy)
        → Save trained mark-predictor model
```

### Phase 2 — Evaluation (per new script)
```
Scanned handwritten answer PDF
        → Handwriting OCR (TrOCR)
        → Segment into questions + match to answer key
        → Semantic similarity + concept coverage
        → Trained model predicts marks  ⟵ (uses the saved model from Phase 1)
        → Feedback + mark-deduction reasons
        → Flag low-confidence answers for human review
        → Fully evaluated sheet: question-wise marks, total, percentage
```

### How a teacher uses it
1. Start backend (`:8000`) and open the web dashboard (`:3000`) or the Expo mobile app.
2. Optionally upload a shared **answer key** and **question paper**.
3. Add students, upload each student's answer-script **PDF**, click **Grade** (or **Grade all**).
4. Review the evaluated sheet: MCQ + descriptive subtotals, total, percentage, per-question marks, extracted answer vs. correct answer, OCR confidence.
5. **Edit** any mis-read answer and **Re-grade** instantly (no OCR re-run). Export results as CSV.

> Low-confidence (unreadable) answers are **flagged for human verification — never guessed.**

---

## 5. Feature enhancements

Planned / candidate improvements to raise accuracy, usability, and reach:

- **Handwriting accuracy** — fine-tune OCR on domain handwriting; better deskew/binarize for noisy scans.
- **Layout robustness** — support multi-column, diagram-heavy, and mixed MCQ+descriptive sheets.
- **Confidence UX** — inline highlighting of low-confidence words for faster teacher correction.
- **Rubric-aware scoring** — let teachers define per-question rubrics that feed the feature set.
- **Batch/queue mode** — grade an entire class folder in the background with progress tracking.
- **Analytics dashboard** — cohort averages, pass rates, per-question difficulty, examiner-consistency.
- **Multi-language answers** — extend OCR + similarity to regional languages.
- **Role-based access** — admin / teacher / operator roles with audit logs.
- **One-click deployment** — Docker image + desktop installer for non-technical staff.
- **Model retraining loop** — feed teacher corrections back to continuously improve Model B.

---

## 6. Important information

### Live-verified result
A real test script graded **23.5 / 25 = 94% (Grade A+)** across 5 questions in ~30 s (first grade includes the one-time OCR model load).

### Model B metrics (trained on Mohler ASAG, 2,442 answers)
- **RMSE ≈ 0.19**, **R² ≈ +0.12** on a held-out split.
- Note: local student data is too skewed to train on, so Mohler ASAG is the real training set. Improving these metrics is an active next step.

### Tech stack (offline, CPU-only)
Python · FastAPI · TrOCR-large-handwritten (OCR) · OpenCV (image prep / segmentation) ·
sentence-transformers `all-MiniLM-L6-v2` (similarity) · **XGBoost / scikit-learn** (trained mark-predictor) ·
Next.js + React + TypeScript (web) · React Native / Expo (mobile) · SQLite + JSON storage.
**No cloud, no paid API, no LLM in the grading path.**

### Honest limitations
- **MCQ OCR** fails on double-sided scans (bleed-through) → MCQ answers come from the digital record for known students, or a dropdown. Not real OCR yet.
- **OCR accuracy** ~90% characters on real scans (garbles on bleed-through); ~98% on clean/synthetic PDFs.
- **Throughput** — single-process, CPU/MPS-bound (~4–5 scripts/min); no parallelism yet.

### Environment notes (critical)
- Pin `transformers==4.57.6` and `opencv-python==4.11.0.86` (newer versions break TrOCR / segfault).
- Do **not** install `surya-ocr` or `paddleocr` (they force incompatible `transformers`).
- Canonical mobile app is **`examshield-mobile2/`** (Expo SDK 54).

### Team (Team Falcons)
Gaurav Ganesh Teegulla · Yashwanthi Nagapuri · Aishwarya Vollala

---

*Compliance (Track 02): the mark is produced by the trained XGBoost model — never by prompting an LLM.
An LLM is not used anywhere in the grading path.*
