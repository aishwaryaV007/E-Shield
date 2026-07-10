# ExamShield — AI Handwritten Answer-Sheet Evaluator

> An offline AI system that **learns how teachers grade** from previously corrected answer
> sheets, then **automatically evaluates** new scanned handwritten scripts — assigning
> question-wise marks, a total, a percentage, and per-answer feedback.

**Hackathon track:** 02 — Predictive Analytics (ML / DL)

**Status:** Model A (the Reader) implemented & tested (~90% char accuracy). Model B (the trained
mark-predictor) in progress.

---

## Running Model A (the Reader)

Model A reads a handwritten answer-script PDF, extracts each question's answer with **TrOCR-large**,
and matches it to the answer key with a semantic **matching score**. One-time setup caches the
models (needs internet once); after that it runs fully offline.

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate     # first time only
pip install -r requirements.txt                        # first time only

# Run Model A on a script (Student_1 .. Student_50):
PYTHONPATH=. python -c "
from app.pipeline.model_a_reader import ModelAReader, load_answer_key
key = load_answer_key('../dataset/answer_keys/answerkey.txt')
reader = ModelAReader(key, question_path='../dataset/answer_keys/Question.txt')
res = reader.read_script('../dataset/raw_scripts/Student_Pdf/Student_1.pdf')
for q in sorted(res, key=int):
    print(f\"Q{q} (match {res[q]['similarity']:.2f}): {res[q]['answer'][:100]}\")
print(f'{len(res)}/15 answers')
"
```

**Reading it:** each line prints the question, its matching score (0–1), and the extracted answer;
the last line shows how many of the 15 questions were found. Scores below ~0.2 flag a likely
mis-read/mis-assignment. First run is slower (loads TrOCR-large ~1.3 GB from cache).

Run the tests: `cd backend && PYTHONPATH=. pytest -q` (expect **11 passed**).

**Note (Track 02 compliance):** Model A only *reads*. Marks are decided later by the trained model
in `evaluation/scorer.py` (Model B) — never by an LLM.

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
