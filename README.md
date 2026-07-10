# ExamShield — AI Handwritten Answer-Sheet Evaluator

> An offline AI system that **learns how teachers grade** from previously corrected answer
> sheets, then **automatically evaluates** new scanned handwritten scripts — assigning
> question-wise marks, a total, a percentage, and per-answer feedback.

**Hackathon track:** 02 — Predictive Analytics (ML / DL)

*Design / Planned — Not yet implemented*

---

## 1. Project Overview

Universities manually evaluate lakhs of handwritten answer scripts every semester — slow,
inconsistent, and error-prone. ExamShield replaces hand-written marking rules with a model that
**learns marking behaviour from real teacher-corrected papers** and then grades new scripts with
human-like consistency, fairness, and transparency.

### Core idea — two phases

**Phase 1 — Model Training.** Learn from historical evaluations:
previously corrected scripts + teacher-awarded marks, official question papers, model answer
keys, marking rubrics, and teacher feedback → a trained **mark-predictor** model.

**Phase 2 — Automated Evaluation.** For each new scanned script:
OCR the handwriting → detect each question & answer → measure **semantic similarity** to the
answer key → apply the trained model → assign **percentage-based marks** → generate feedback and
mark-deduction reasons → produce a fully evaluated answer sheet.

### Compliance principle
> **Marks are always produced by the trained model — never by prompting an LLM.**
> Track 02 prohibits LLM-generated predictions; an LLM may only phrase feedback text, never
> decide a mark. Unreadable (low-confidence) answers are flagged for human verification, not guessed.

---

## 2. How marks are assigned (percentage-based)

The mark is proportional to how closely the student's answer matches the expected answer,
considering semantic meaning, key-concept coverage, correctness, and missing/extra points.
Illustrative bands on an 8-mark question:

| Match | Marks |
|-------|-------|
| 90–100% | 8 / 8 |
| 80–89% | 6–7 |
| 70–79% | 5–6 |
| 60–69% | 4–5 |
| 50–59% | 3–4 |
| < 50% | scaled down by quality & completeness |

---

## 3. Pipeline

```mermaid
graph TD
    subgraph Phase 1 — Training
    H[Historical corrected scripts + teacher marks] --> DB[dataset_builder]
    K[Question papers / answer keys / rubrics] --> DB
    DB --> FE[features] --> TR[trainer] --> EV[evaluate: RMSE / MAE / R² / ±1-acc]
    TR --> M[(trained mark-predictor)]
    end
    subgraph Phase 2 — Evaluation
    S[Scanned answer scripts] --> ING[ingestion: deskew/binarize]
    ING --> OCR[handwriting OCR]
    OCR --> SEG[segment questions + match answer key]
    SEG --> SIM[semantic similarity + concept coverage]
    SIM --> SC[scorer: trained model → marks]
    M --> SC
    SC --> FB[feedback + deduction reasons]
    FB --> RPT[report: question-wise marks, total, %]
    end
```

---

## 4. Final output per script

Question-wise marks · total marks · percentage · per-answer feedback · mark-deduction reasons ·
low-confidence answers flagged for optional human verification — a fully evaluated sheet
resembling one corrected by a human examiner.

---

## 5. Tech stack (offline, CPU-only)

Python 3.11 · FastAPI · OpenCV / pypdfium2 (image prep) · TrOCR/PaddleOCR (handwriting OCR) ·
sentence-transformers `all-MiniLM-L6-v2` (semantic similarity) · **XGBoost / scikit-learn**
(the trained mark-predictor) · SQLite + JSON storage · Next.js 14 + React + TypeScript (dashboard).

No cloud, no paid API, **no LLM in the grading path**.

---

## 6. Project structure

```
E-Shield/
├── backend/app/
│   ├── training/        # Phase 1: dataset_builder, features, trainer, evaluate
│   ├── ingestion/       # Phase 2 input: pdf_loader, preprocess
│   ├── ocr/             # handwriting_ocr, confidence
│   ├── segmentation/    # question_segmenter, answer_matcher
│   ├── evaluation/      # similarity, concept_coverage, scorer, feedback, report
│   ├── models/          # embedder (MiniLM), mark_model (trained regressor)
│   ├── pipeline/        # orchestrator (train_pipeline + evaluate_pipeline)
│   ├── services/ · storage/ · api/
├── frontend/            # Next.js dashboard (Overview, Training, Ingestion, Results)
├── data/                # corpus/ (Phase 1), answer_keys/, raw/, results/, metrics/
├── docs/                # architecture, planning, data-flow, engine-stage docs
└── scripts/             # download_models.py, seed_demo_data.py
```

See [SETUP.md](SETUP.md) to run it, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design,
and [docs/PROBLEM_STATEMENT.md](docs/PROBLEM_STATEMENT.md) for the hackathon brief.
