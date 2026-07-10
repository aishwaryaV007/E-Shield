# ExamShield — AI Handwritten Answer-Sheet Evaluator

> An offline AI system that **learns how teachers grade** from previously corrected answer
> sheets, then **automatically evaluates** new scanned handwritten scripts — assigning
> question-wise marks, a total, a percentage, and per-answer feedback.

**Hackathon track:** 02 — Predictive Analytics (ML / DL)

**Status:** working end-to-end — Model A (reader, TrOCR-large) + Model B (XGBoost marker) + FastAPI
API + Next.js dashboard. Runs fully offline after a one-time model download.

---

## Running the project locally

### Prerequisites
- **Python 3.11+** (3.14 works) · **Node.js 20+** · **git**
- ~3 GB free disk for the cached models · **internet once** (to download TrOCR-large + MiniLM), then offline
- macOS/Linux/Windows. On Apple Silicon it uses MPS automatically.

### 1. Clone
```bash
git clone https://github.com/aishwaryaV007/E-Shield.git
cd E-Shield
```

### 2. Backend (FastAPI + the ML pipeline)
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt                        # first time only (installs torch, xgboost, etc.)

# Start the API (first run downloads ~1.5 GB of models, then caches them):
PYTHONPATH=. python -m uvicorn main:app --host 127.0.0.1 --port 8000
# API is now at http://127.0.0.1:8000  (health: /health, docs: /docs)
```
> ⚠️ Keep `transformers==4.57.6` and `opencv-python==4.11.0.86` (pinned in requirements — newer
> versions break TrOCR / segfault). Do **not** install `surya-ocr` or `paddleocr`.

### 3. Frontend (Next.js dashboard) — in a second terminal
```bash
cd frontend
npm install                                            # first time only
npm run dev
# Dashboard is now at http://localhost:3000
```

### 4. Use it
Open **http://localhost:3000**, then:
1. **Upload** a student answer-script PDF (e.g. `dataset/raw_scripts/Student_Pdf/Student_1.pdf`).
   Optionally upload an answer key (CSV) and question paper.
2. Click **Grade script** (~30–45 s — TrOCR reads the handwriting).
3. See **MCQ + descriptive subtotals**, the total `/50`, per-question marks, the extracted answer,
   and the correct answer. **Edit** any mis-read answer and hit **Re-grade** for the fixed mark.

### Command-line / tests (optional)
```bash
cd backend && source .venv/bin/activate

# Grade one script from the CLI:
PYTHONPATH=. python -c "
from app.pipeline.grade_pipeline import grade_script
s = grade_script('../dataset/raw_scripts/Student_Pdf/Student_1.pdf',
                 '../dataset/answer_keys/answerkey.txt',
                 question_path='../dataset/answer_keys/Question.txt')
print(s['total_marks'], '/', s['max_total'], '=', s['percentage'], '%')
"

# Train Model B (regenerates models_cache/mark_predictor.pkl + metrics):
PYTHONPATH=. python -m app.training.trainer

# Run the test suite (expect 11 passed):
PYTHONPATH=. pytest -q
```

### Troubleshooting
| Symptom | Fix |
|---|---|
| Segfault / `cv2 has no attribute` | one OpenCV only: `pip uninstall -y opencv-python-headless` |
| TrOCR tokenizer error | `pip install "transformers==4.57.6"` (5.x is incompatible) |
| Frontend upload times out | the browser calls the backend directly on `:8000` — make sure the backend is running |
| Marks all look like the similarity baseline | train Model B: `python -m app.training.trainer` |

**Track 02 compliance:** the mark is produced by the trained XGBoost model — never by an LLM.
An LLM is not used anywhere in the grading path.

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
├── dataset/             # ML training data (Track 02): raw_scripts/, answer_keys/, training_csv/, sample/
├── data/                # runtime I/O: corpus/, answer_keys/, raw/, results/, metrics/
├── docs/                # architecture, planning, data-flow, pipeline-stage docs
├── pitch/               # deliverables: validation PDF, pitch guide (md/html), deck (pptx), one-pager (docx)
└── scripts/             # download_models.py, seed_demo_data.py
```

See [SETUP.md](SETUP.md) to run it, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design,
and [docs/PROBLEM_STATEMENT.md](docs/PROBLEM_STATEMENT.md) for the hackathon brief.
