# E-Shield — Setup & Getting Started

> **Single source of truth for setting up E-Shield from scratch.**
> Follow this file top to bottom. A new developer should be able to clone the repo, follow only this document, and run the full project without asking any questions.
>
> If you add any new dependency, tool, service, model, or env var during development, **update this file in the same commit.**

---

## 1. Project Overview

**E-Shield (ExamShield)** is an **offline evaluation pipeline for scanned handwritten answer sheets.** It ingests scanned scripts, runs OCR on calibrated zones, and runs five verification engines that **rank and flag** integrity/accuracy issues for a human auditor. Governing principle:

> **Rank and flag evidence; never accuse, never finalize; the human decides.**

The five engines:

| Engine | Job |
|--------|-----|
| **MarkSafe** | Digit-OCRs the marks grid, sums per-question marks, compares to the written total; flags mismatches/strikeouts as *Ambiguous — Human Review*. Never auto-corrects. |
| **CopyCatch** | Prose OCR → MiniLM embeddings → O(N²) cosine-similarity → z-score ranking vs class baseline → NetworkX collusion graph (rendered in the UI). |
| **ScriptID** | Digit-OCRs the roll-number box, validates against the class register (duplicates / absentees / misreads). |
| **ReEval Guard** | Flags scripts within 1–2 marks of a grade threshold (e.g. 39/40) into a pre-publication priority queue. |
| **RubricLens** | Retrieval + NLI (deberta-xsmall) to highlight where student text aligns (green) or contradicts (red) the rubric. Never a mark. |

### Tech stack

| Layer | Choice |
|-------|--------|
| Language (backend) | **Python 3.11** |
| Backend API | **FastAPI + Uvicorn** |
| Image processing | **OpenCV**, **Pillow**, **pypdfium2** |
| OCR | **PaddleOCR** (+ paddlepaddle) |
| Embeddings | **sentence-transformers** — `all-MiniLM-L6-v2` |
| NLI | **cross-encoder/nli-deberta-v3-xsmall** (via transformers/torch) |
| Numerics / data | **NumPy, pandas, scikit-learn** |
| Graph | **NetworkX** (compute) → rendered in the UI |
| Storage | **SQLite** (`aiosqlite`) **+ JSON files** — no server DB |
| Frontend | **Next.js 14 (App Router) + React 18 + TypeScript** |
| Styling | **Tailwind CSS** |
| Server state | **TanStack Query** |
| Client state | **Zustand** |
| Calibration canvas | **react-konva / konva** |
| Collusion graph render | **react-force-graph-2d** |
| HTTP client | **Axios** |

> **Offline-first, no cloud, no paid API.** Every model runs locally on CPU. There is **no OpenAI/Gemini/Anthropic dependency and no API key to buy** (see §4).

---

## 2. Prerequisites

| Tool | Required version | Notes |
|------|------------------|-------|
| **Git** | 2.30+ | Version control |
| **Python** | **3.11.x** | Backend + ML pipeline. 3.12 may hit paddlepaddle wheel gaps — prefer 3.11. |
| **pip** | 23+ | Ships with Python |
| **Node.js** | **20.x LTS** | Frontend |
| **npm** | 10+ | Ships with Node 20 (pnpm/yarn also fine) |
| **Docker + Docker Compose** | 24+ | Optional — only for the containerised run (§6) |

**Not required:** Redis, Postgres/MySQL, Firebase, Supabase, Java, Flutter, or any cloud LLM account. E-Shield deliberately avoids all of them.

### Recommended IDE & extensions

- **VS Code** with:
  - Python, Pylance
  - Ruff (`charliermarsh.ruff`)
  - Black Formatter
  - ESLint, Prettier
  - Tailwind CSS IntelliSense

---

## 3. Environment Setup

### 3.1 Clone

```bash
git clone https://github.com/aishwaryaV007/E-Shield.git
cd E-Shield
```

### 3.2 Backend — virtualenv + dependencies

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # tests / linting / formatting
```

### 3.3 Frontend — dependencies

```bash
cd ../frontend
npm install
```

### 3.4 Environment variables

> ⚠️ The committed `backend/.env.example` and `frontend/.env.local.example` were overwritten with placeholder comments during scaffolding. Use the values below as the source of truth until those files are restored.

**`backend/.env`**

```env
# Local paths (relative to repo root)
DB_PATH=../data/eshield.sqlite
DATA_DIR=../data
MODEL_DIR=../models_cache
# API
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

**`frontend/.env.local`**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.5 Required API keys

**None.** All models run locally. There are no secret keys, tokens, or third-party accounts required to run E-Shield. (See §4 and §14.)

---

## 4. LLM & AI Configuration

E-Shield uses **local, CPU-friendly models only — there is no LLM API and no key to obtain.**

| Purpose | Model | Size | Provider / source | Setup |
|---------|-------|------|-------------------|-------|
| OCR (digits + prose) | **PaddleOCR** (`en`, angle-cls on) | ~few hundred MB | PaddlePaddle (downloaded once, cached) | Local |
| Sentence embeddings (CopyCatch) | **all-MiniLM-L6-v2** | ~80 MB | HuggingFace `sentence-transformers` | Local |
| NLI (RubricLens) | **cross-encoder/nli-deberta-v3-xsmall** | small | HuggingFace | Local |

**Why no LLM:** CopyCatch needs *relative similarity ranking*, not comprehension — an 80 MB CPU model does hundreds of pairwise comparisons instantly and stays fully explainable. RubricLens uses an NLI cross-encoder (handles negation) rather than a generative model. This keeps student scripts private (nothing leaves the machine) and removes venue-Wi-Fi / cost risk.

### One-time model warm-up (needs internet **once**; then fully offline)

```bash
cd backend && source .venv/bin/activate
python ../scripts/download_models.py
```

If that script isn't wired yet, warm the caches manually:

```python
from paddleocr import PaddleOCR
from sentence_transformers import SentenceTransformer, CrossEncoder
PaddleOCR(use_angle_cls=True, lang="en")
SentenceTransformer("all-MiniLM-L6-v2")
CrossEncoder("cross-encoder/nli-deberta-v3-xsmall")
```

Weights cache under `models_cache/` (and the default HuggingFace/Paddle cache dirs).

---

## 5. Database Setup

E-Shield uses **SQLite + JSON files** — nothing to install or run as a service.

- **DB file:** created automatically at `DB_PATH` (`data/eshield.sqlite`) on first backend start.
- **Schema:** defined in [`backend/app/storage/schema.sql`](backend/app/storage/schema.sql) — tables for scripts, pages, marks, flags, registers, templates.
- **Migrations:** none needed for the MVP — the app initialises the schema on boot via `backend/app/storage/db.py`. If the schema changes, delete the local `.sqlite` file and let it re-create (no production data yet).
- **JSON stores:** calibration templates in `data/templates/`, results in `data/results/`, class registers (CSV) in `data/registers/`.

### Seed demo data (for the demo / testing)

```bash
cd backend && source .venv/bin/activate
python ../scripts/seed_demo_data.py     # generates 35+ scripts with planted errors
```

---

## 6. Required Services

**No external services are required.** No Redis, Firebase, Supabase, Postgres, or MySQL.

Optional — run both apps in containers:

```bash
docker compose -f deploy/docker-compose.yml up --build
```

`docker-compose.yml` defines two services: **backend** (FastAPI) and **frontend** (Next.js). It is currently a commented stub — fill in before relying on it.

---

## 7. Installation Commands (quick reference)

```bash
# --- Backend ---
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# --- Frontend ---
cd ../frontend
npm install

# --- Models (one-time, needs internet) ---
cd ../backend && source .venv/bin/activate
python ../scripts/download_models.py
```

**Package managers:** `pip` (backend), `npm` (frontend). No global npm packages required — everything is local devDependencies. No `brew`-installed services needed.

---

## 8. Project Structure

```
E-Shield/
├── SETUP.md                 # ← this file (root)
├── README.md                # monorepo overview (root)
├── Makefile                 # install / dev / test / lint targets
├── .gitignore
│
├── deploy/                  # deployment/infra config
│   └── docker-compose.yml   # backend + frontend containers (stub)
│
├── backend/                 # Python / FastAPI backend
│   ├── requirements.txt / requirements-dev.txt / pyproject.toml
│   ├── config.py            # typed settings from .env
│   ├── main.py              # FastAPI app factory
│   └── app/
│       ├── ingestion/       # pdf_loader, preprocess, blankcheck
│       ├── calibration/     # zone template save/load
│       ├── ocr/             # digit_ocr, prose_ocr, ambiguity fallback
│       ├── engines/         # marksafe, copycatch, scriptid, reeval_guard, rubriclens
│       ├── models/          # embedder (MiniLM), nli (deberta)
│       ├── storage/         # db (SQLite), json_store, schema.sql
│       ├── api/             # routes/ (ingestion, calibration, pipeline, results), schemas, deps
│       └── utils/           # logging, image_ops (evidence crops)
│
├── frontend/                # Next.js 14 + React 18 + TS dashboard
│   ├── package.json / tsconfig.json / tailwind.config.ts / next.config.js
│   └── src/
│       ├── app/             # App Router pages: /, /ingestion, /calibration, /review, /scripts/[id]
│       ├── components/      # layout, calibration (ZoneCanvas), review (FlagCard, CollusionGraph…), ui
│       ├── lib/api/         # Axios client + ingestion/pipeline/results calls
│       ├── hooks/           # useFlags, usePipeline (TanStack Query)
│       ├── store/           # batchStore (Zustand)
│       └── types/           # TS types mirroring backend schemas
│
├── data/                    # gitignored inputs/outputs (raw, processed, templates, registers, results)
├── models_cache/            # local model weights
├── tests/                   # pytest suites (target backend/app/*)
├── scripts/                 # download_models.py, seed_demo_data.py
└── docs/                    # ALL project docs live here:
    ├── architecture / planning / security / engine docs
    ├── PROBLEM_STATEMENT.md, ExamShield_Workflow.md   # hackathon brief + workflow
    ├── context.md, plan.md, implementation_plan.md    # planning docs
    └── TECH_STACK.md, TECH_STACK_ORIGINAL.md          # stack rationale
```

> **Root stays clean:** only `README.md` and `SETUP.md` are visible at the top level. Every other `.md` lives in `docs/`, and deployment config lives in `deploy/`.

---

## 9. How to Run

### Development mode

**Backend** (from `backend/`, venv active):

```bash
uvicorn main:app --reload --port 8000
# API at http://localhost:8000  · docs at http://localhost:8000/docs
```

**Frontend** (from `frontend/`):

```bash
npm run dev
# UI at http://localhost:3000
```

Run both in separate terminals. The frontend talks to the backend via `NEXT_PUBLIC_API_URL`.

### Production mode

**Backend:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

**Frontend:**

```bash
npm run build
npm run start          # serves on :3000
```

Or containerised: `docker compose -f deploy/docker-compose.yml up --build`.

**Mobile app:** none — E-Shield is a web dashboard only.

---

## 10. Testing, Linting, Formatting

**Backend tests** (from `backend/`, venv active):

```bash
pytest                 # runs tests/ (configured to see backend/app via pythonpath)
```

**Backend lint / format / types:**

```bash
ruff check .           # lint
black .                # format
mypy .                 # type-check
```

**Frontend:**

```bash
npm run lint           # ESLint (next lint)
npm run type-check     # tsc --noEmit
```

Convenience targets exist in the root `Makefile` (`make install`, `make dev-backend`, `make dev-frontend`, `make test`, `make lint`).

---

## 11. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `paddlepaddle` fails to install | Use **Python 3.11** (not 3.12/3.13). On Apple Silicon install the CPU wheel; avoid the `-gpu` package. |
| PaddleOCR downloads on every run / offline error | Run the model warm-up (§4) once with internet; weights then load from cache. Set `MODEL_DIR`/HF cache env if needed. |
| `torch` install is huge/slow | Expected (transformers pulls it). CPU wheel is fine; no CUDA needed. |
| Frontend can't reach API / CORS error | Ensure backend is on `:8000`, `NEXT_PUBLIC_API_URL=http://localhost:8000`, and `CORS_ORIGINS` includes `http://localhost:3000`. |
| `pytest` can't import `app` | Ensure pytest `pythonpath = ["backend"]` (in `backend/pyproject.toml`) or run pytest from `backend/`. |
| OpenCV `ImportError: libGL.so.1` (Linux) | `sudo apt-get install -y libgl1`. |
| `.DS_Store` keeps reappearing (macOS) | It's gitignored; ignore it. |
| Windows venv activation blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then re-activate. |
| Port already in use | Change `--port` (backend) or `PORT=3001 npm run dev` (frontend). |

---

## 12. Verification Checklist

Run these after setup; expected outputs noted.

```bash
git --version            # → git version 2.30+
python3.11 --version     # → Python 3.11.x
node --version           # → v20.x
npm --version            # → 10.x
docker --version         # → Docker version 24+ (only if using containers)
```

```bash
# Backend deps resolve
cd backend && source .venv/bin/activate
python -c "import fastapi, cv2, paddleocr, sentence_transformers, numpy, pandas, sklearn, networkx; print('backend OK')"
# → backend OK

# Backend package imports
python -c "import sys; sys.path.insert(0,'.'); import app; print('app import OK')"
# → app import OK

# Models cached
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('MiniLM OK')"
# → MiniLM OK (instant if cached)
```

```bash
# Frontend type-checks
cd ../frontend && npm run type-check
# → no errors
```

```bash
# Servers boot
uvicorn main:app --port 8000    # backend, then open http://localhost:8000/docs
npm run dev                     # frontend, then open http://localhost:3000
```

---

## 13. Development Workflow

### Recommended order of implementation

1. **Storage** (`storage/db.py`, `schema.sql`) — tables must exist first.
2. **Ingestion** (`pdf_loader → preprocess → blankcheck`).
3. **Calibration** (`template_io`) + frontend `ZoneCanvas`.
4. **OCR** (`digit_ocr`, `prose_ocr`, `ambiguity`).
5. **Engines** — start with **MarkSafe** (simplest, high value), then **ScriptID**, **ReEval Guard**, **CopyCatch**, **RubricLens** (stretch).
6. **Pipeline orchestrator + services** — chain the stages end to end.
7. **API routes** → **frontend** (review dashboard, evidence crops, collusion graph).

### Branch strategy

- Shared repo (`aishwaryaV007/E-Shield`), everyone works toward `main`.
- **Always `git pull --rebase origin main` before pushing** to stay in sync with teammates.
- Feature branches (`feat/marksafe`, `fix/ocr-ambiguity`) → PR into `main` where possible.

### Commit conventions

- Small, focused commits. Suggested prefixes: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Commits are authored by **your own git identity** — **no AI/Claude co-author trailer.**

---

## 14. Additional Notes

**Assumptions**
- Local development on macOS/Linux/Windows with Python 3.11 and Node 20.
- Scripts arrive as scanned PDFs or images at ~300 DPI.

**Important warnings**
- The `.env.example` files currently hold placeholder comments (scaffolding artifact) — use §3.4 values and restore the real examples.
- Deleting `data/eshield.sqlite` wipes local results — fine pre-production, never in a real deployment.
- Never auto-correct a mark or accuse a student — the system only **flags for human review**.

**Performance**
- CopyCatch is O(N²): ~35 scripts ≈ 600 pairs = milliseconds; a full 300-script batch = 44,850 pairs — keep it **vectorised in NumPy** (one matrix op), never a Python loop.
- All models are CPU-friendly; no GPU required.

**Security & privacy**
- **Nothing leaves the machine** — no third-party API calls, no telemetry. Student scripts and grades stay local (SQLite/JSON).
- Do not commit `data/` contents (real scripts/registers) — it is gitignored.
- Keep `.env` files out of git.

**Best practices**
- Ambiguous OCR (strikeouts, low confidence, bad handwriting) must fall back to *"Ambiguous — Human Review"*, never a guess.
- Keep the frontend/backend API contract in sync: `frontend/src/types` mirrors `backend/app/api/schemas.py`.

---

*Keep this file current. If you introduce a new dependency, service, model, or env var, update the relevant section in the same commit so SETUP.md always reflects the real setup process.*
