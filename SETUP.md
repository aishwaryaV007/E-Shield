# E-Shield — Setup & Getting Started

> **Single source of truth for setting up E-Shield from scratch.** Clone, follow top to bottom,
> run the full project. If you add a dependency, tool, model, or env var, update this file in the
> same commit.

---

## 1. Project Overview

**E-Shield (ExamShield)** is an **offline AI evaluator for scanned handwritten answer sheets**
(Track 02 — Predictive Analytics / ML-DL). It works in two phases:

- **Phase 1 — Training:** learn teacher marking behaviour from historical corrected scripts +
  answer keys + rubrics + teacher marks → a trained **mark-predictor** model.
- **Phase 2 — Evaluation:** OCR a new script → segment questions → measure semantic similarity to
  the answer key → the trained model assigns **percentage-based marks** → generate feedback.

> **Governing rule:** the mark is produced by the trained model — **never by an LLM.** An LLM may
> only phrase feedback text. Unreadable answers are flagged for human verification, not guessed.

### Tech stack

| Layer | Choice |
|-------|--------|
| Language (backend) | **Python 3.11** |
| Backend API | **FastAPI + Uvicorn** |
| Image processing | **OpenCV**, **Pillow**, **pypdfium2** |
| Handwriting OCR | **TrOCR handwritten / PaddleOCR** |
| Semantic similarity | **sentence-transformers** — `all-MiniLM-L6-v2` |
| **Mark-predictor (trained)** | **XGBoost / scikit-learn** (+ joblib) |
| Numerics / data | **NumPy, pandas, rapidfuzz** |
| Storage | **SQLite** (`aiosqlite`) **+ JSON files** — no server DB |
| Frontend | **Next.js 14 (App Router) + React 18 + TypeScript** |
| Styling / charts | **Tailwind CSS** / **Recharts** |
| Server / client state | **TanStack Query** / **Zustand** |
| HTTP client | **Axios** |

> **Offline-first, no cloud, no paid API, no LLM in the grading path.** Everything runs locally on CPU.

---

## 2. Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| **Git** | 2.30+ | |
| **Python** | **3.11.x** | prefer 3.11 for paddlepaddle/torch wheels |
| **Node.js** | **20.x LTS** | frontend |
| **npm** | 10+ | |
| **Docker + Compose** | 24+ | optional (containerised run) |

**Not required:** Redis, Postgres/MySQL, Firebase, any cloud LLM account.

---

## 3. Environment Setup

```bash
git clone https://github.com/aishwaryaV007/E-Shield.git
cd E-Shield

# Backend
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Frontend
cd ../frontend && npm install
```

**`backend/.env`**
```env
DB_PATH=../data/eshield.sqlite
DATA_DIR=../data
MODEL_DIR=../models_cache      # cached embedder + trained mark_predictor.pkl
CORPUS_DIR=../data/corpus      # Phase-1 historical training corpus
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

**`frontend/.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Required API keys: none.** All models run locally.

---

## 4. Models

| Purpose | Model | Source | Local? |
|---------|-------|--------|--------|
| Handwriting OCR | TrOCR handwritten / PaddleOCR | HuggingFace / PaddlePaddle | ✅ |
| Semantic similarity | all-MiniLM-L6-v2 (~80 MB) | HuggingFace | ✅ |
| **Mark-predictor** | **XGBoost regressor trained in Phase 1** | trained by us on the corpus | ✅ |

**Why no LLM:** Track 02 prohibits LLM-generated predictions. Semantic similarity ranks how close
an answer is to the key; a trained regressor maps those features to a mark — fully explainable and
private (nothing leaves the machine).

One-time OCR/embedding warm-up (needs internet once):
```bash
cd backend && source .venv/bin/activate
python ../scripts/download_models.py
```

Train the mark-predictor (Phase 1):
```bash
python ../scripts/seed_demo_data.py     # generates corpus + a batch to grade
# then POST /train from the UI, or run the training pipeline entrypoint
```

---

## 5. Database

**SQLite + JSON** — nothing to install. DB auto-creates at `DB_PATH` on first start; schema in
[`backend/app/storage/schema.sql`](backend/app/storage/schema.sql) — tables for models, batches,
answer_keys, questions, scripts, pages, and **evaluations** (question-wise predicted marks +
feedback). JSON stores: answer keys in `data/answer_keys/`, evaluated sheets in `data/results/`,
training metrics in `data/metrics/`.

---

## 6. How to Run

```bash
# Backend (from backend/, venv active)
uvicorn main:app --reload --port 8000    # http://localhost:8000/docs

# Frontend (from frontend/)
npm run dev                              # http://localhost:3000
```

Or containerised: `docker compose -f deploy/docker-compose.yml up --build`.

---

## 7. Testing / Linting

```bash
cd backend && pytest            # tests/ (pythonpath = backend)
ruff check . && black . && mypy .
cd ../frontend && npm run lint && npm run type-check
```

---

## 8. Recommended implementation order

1. **Storage** (`storage/db.py`, `schema.sql`) — tables first.
2. **Phase 1 training** (`training/dataset_builder → features → trainer → evaluate`) — get a
   trained model + metrics. Fallback baseline: unsupervised similarity-to-key scoring if no
   labeled corpus is available yet.
3. **Ingestion + OCR** (`ingestion/`, `ocr/`) — scanned script → handwritten text.
4. **Segmentation** (`segmentation/`) — split into questions, match to answer key.
5. **Evaluation** (`evaluation/similarity → concept_coverage → scorer → feedback → report`).
6. **Pipeline orchestrator + services + API**.
7. **Frontend** — Training metrics, Ingestion/upload, Results (evaluated sheets).

---

## 9. Notes & best practices

- **Never let an LLM decide a mark** — the regressor in `evaluation/scorer.py` owns the mark.
- **Feature parity:** `training/features.py` must produce the *same* vector at train and inference time.
- Low-confidence OCR answers → flagged for human verification, never a guessed mark.
- Keep `frontend/src/types` in sync with `backend/app/api/schemas.py`.
- **Nothing leaves the machine** — no third-party API calls, no telemetry. `data/` is gitignored.
- Always `git pull --rebase origin main` before pushing; commits under your own identity (no AI co-author).

---

*Keep this file current — update it in the same commit as any new dependency, model, or env var.*
