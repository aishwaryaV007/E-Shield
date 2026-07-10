# ExamShield — Tech Stack

**Track:** 02 — Predictive Analytics (ML / DL) | **Format:** 24-hour hackathon

Guiding rule for every pick: **boring, offline, pip-installable in one shot.** No GPU cluster, no
paid API, **no LLM in the grading path.** Download and test every model **before** the event.

---

## 🧱 Stack at a Glance

| Layer | Choice | Used by |
|-------|--------|---------|
| Language | **Python 3.11** | Everything |
| Image preprocessing | **OpenCV** (`opencv-python`) | Ingestion (deskew/denoise/binarize) |
| PDF input | **pypdfium2** (PDF pages → images) | Ingestion |
| Handwriting OCR | **TrOCR handwritten / PaddleOCR** (with confidence) | Reading student answers |
| Semantic similarity | **sentence-transformers** — `all-MiniLM-L6-v2` | Similarity + features |
| Concept coverage (opt) | **cross-encoder/nli-deberta-v3-xsmall** | Negation / contradiction detection |
| **Mark-predictor (trained)** | **XGBoost** (fallback: RandomForest / sklearn MLP) + **joblib** | The scorer — assigns marks |
| Feature engineering / stats | **NumPy + scikit-learn + pandas** | Training + inference features |
| Answer↔question matching | **rapidfuzz** | Segmentation |
| Backend API | **FastAPI + Uvicorn** | Dashboard ↔ pipeline |
| Data store | **SQLite + JSON files** — no server DB | Answer keys, scripts, evaluations, metrics |
| Frontend | **Next.js 14 + React 18 + TypeScript** | Training + Results dashboard |
| Charts | **Recharts** | Metrics + score charts |

---

## 🔍 Per-Phase Breakdown

### Phase 1 — Training (`backend/app/training/`)
- **dataset_builder** — assemble (student answer, answer key, features, teacher mark) rows from the
  historical corpus (pandas).
- **features** — semantic similarity (MiniLM cosine), key-concept coverage, keyword recall,
  missing/extra-point counts, length ratio, negation cues. *Same function used at inference.*
- **trainer** — **XGBoost regressor** mapping features → mark; hyperparameter tuning +
  feature-importance (bonus scoring). Persist to `models_cache/mark_predictor.pkl` (joblib).
- **evaluate** — RMSE / MAE / R² / accuracy within ±1 mark on a held-out split (sklearn.metrics).

### Phase 2 — Evaluation
- **Ingestion** — OpenCV deskew/denoise/binarize; pypdfium2 for PDFs.
- **OCR** — handwriting recognition + per-answer confidence.
- **Segmentation** — split into questions; match each answer to its key + rubric (rapidfuzz/regex).
- **Similarity + coverage** — MiniLM embeddings; optional NLI for negation.
- **Scorer** — build the same feature vector, run the **trained model**, apply percentage bands,
  clamp to `[0, max]`.
- **Feedback + report** — deduction reasons + question-wise marks, total, percentage.

---

## 📦 One-Shot Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install opencv-python pypdfium2 pillow \
    paddleocr paddlepaddle transformers \
    sentence-transformers scikit-learn xgboost joblib numpy pandas rapidfuzz \
    fastapi uvicorn aiosqlite python-dotenv httpx
```

**Pre-event warm-up (once with internet):**

```python
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2")     # semantic similarity
# + handwriting OCR model (TrOCR/PaddleOCR) weights
```

Then train the mark-predictor on the historical corpus (Phase 1).

---

## ⚖️ Deliberate Choices (judge-Q&A ready)

- **XGBoost regressor over an LLM for marks** — Track 02 prohibits LLM-generated predictions. A
  trained regressor on engineered features is explainable, fast on CPU, and reports real metrics
  (RMSE/±1-accuracy) against teacher marks.
- **Semantic similarity (MiniLM) over keyword matching** — differently-worded correct answers
  score correctly; an 80 MB CPU model runs instantly and stays fully explainable.
- **NLI cross-encoder for coverage** — solves negation ("is not exothermic" → contradiction).
- **SQLite/JSON over Postgres** — nothing to install at the venue, portable between laptops.
- **Local OCR over cloud OCR** — student data never leaves the machine; no venue-Wi-Fi risk.
