# E-Shield — Team Work Split

> How the three of us divide E-Shield so we can build in parallel. Ownership is by **workstream**
> (a coherent vertical slice), with agreed interfaces where workstreams meet. Read alongside
> [`SETUP.md`](SETUP.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Team:** Gaurav · Aishwarya (Aishu) · Yashwanthi

---

## 1. Principles

- **Own a vertical slice, not scattered files.**
- **Contracts before code.** Where two workstreams meet, agree the interface (a Pydantic schema,
  a function signature, the feature-vector spec) first and treat it as frozen until both agree to change.
- **The mark comes from the trained model, never an LLM.** Every workstream upholds this Track 02 rule.

---

## 2. Ownership at a glance

| Track | Owner | Domain | Primary areas |
|-------|-------|--------|---------------|
| **A — Ingestion, OCR & Segmentation (full-stack)** | **Gaurav** | Backend **+** Frontend | `backend/app/ingestion/`, `ocr/`, `segmentation/`, `utils/` **+** the Ingestion/upload UI |
| **B — Training + Evaluation core, API & Data** | **Aishwarya** | Backend | `backend/app/training/`, `evaluation/`, `models/`, `pipeline/`, `services/`, `api/`, `storage/`, `main.py`, `config.py` |
| **C — Results dashboard, Integration & QA** | **Yashwanthi** | Frontend + Ops | Overview / Training / Results UI, `deploy/`, `backend/tests/`, `scripts/seed_demo_data.py` |

---

## 3. Track A — Ingestion, OCR & Segmentation · **Gaurav**

**Backend:** `ingestion/` (pdf_loader, preprocess), `ocr/` (handwriting_ocr, confidence),
`segmentation/` (question_segmenter, answer_matcher), `utils/`.
**Frontend:** `app/ingestion/page.tsx` (upload scripts + answer key), `lib/api/ingestion.ts`,
`hooks/useEvaluation.ts` (shared with Track C).
**Done when:** an operator can upload scripts + an answer key, and the backend turns a scanned
script into ordered (question, student-answer, key) units ready for scoring — unreadable answers flagged.

---

## 4. Track B — Training + Evaluation core, API & Data · **Aishwarya**

**Owns:** `training/` (dataset_builder, features, trainer, evaluate), `evaluation/` (similarity,
concept_coverage, scorer, feedback, report), `models/` (embedder, mark_model), `pipeline/`
(orchestrator: train + evaluate), `services/evaluation_service.py`, `api/` (routes/training,
evaluation, results, ingestion; schemas; deps), `storage/`, `main.py`, `config.py`,
`scripts/download_models.py`.
**Done when:** the model trains on the corpus and reports RMSE/MAE/R²/±1-accuracy, and Phase 2
produces evaluated sheets (question-wise marks + feedback) exposed via the API — marks from the
trained model, never an LLM.

---

## 5. Track C — Results dashboard, Integration & QA · **Yashwanthi**

**Frontend:** app shell (`layout.tsx`, `page.tsx` overview), `app/training/page.tsx` (metrics),
`app/results/page.tsx`, `app/scripts/[id]/page.tsx` (evaluated sheet), `components/results/*`
(ScoreSummary, AnswerCard, AnswerList, AnswerCompare), `components/layout/*`, `ui/*`,
`lib/api/client.ts`, `lib/api/training.ts`, `hooks/useResults.ts`, `hooks/useTraining.ts`,
`store/`, `types/`.
**Ops & QA:** `deploy/docker-compose.yml`, `backend/tests/`, `scripts/seed_demo_data.py`.
**Done when:** a user can train a model and see metrics, upload a batch, and view fully evaluated
sheets with question-wise marks and feedback; the demo dataset reproduces the full flow.

---

## 6. Shared interfaces

| Boundary | Between | Contract |
|----------|---------|----------|
| OCR/segmentation → scorer | Gaurav ↔ Aishwarya | shape of a grading unit (student_answer, key, rubric, max_marks). |
| Feature spec | Aishwarya (owns) ↔ all | `training/features.py` FEATURE_NAMES — identical at train + inference. |
| Ingestion/evaluation API | Gaurav ↔ Aishwarya | `api/routes/ingestion+evaluation` vs `lib/api/ingestion+evaluation`. |
| API schema ↔ FE types | Aishwarya ↔ Yashwanthi | `api/schemas.py` mirrored by `frontend/src/types/index.ts`. |
| Demo data ↔ pipeline | Yashwanthi ↔ Aishwarya | corpus + batch format the seed script produces. |

---

## 7. Git workflow

Single shared repo, everyone targets `main`. Branch per workstream
(`feat/gaurav-…`, `feat/aishu-…`, `feat/yashwanthi-…`). **Always `git pull --rebase origin main`
before pushing.** Small, focused commits under your own identity (no AI co-author trailer).

---

## 8. Milestone alignment

| Phase | Focus | Lead | Support |
|-------|-------|------|---------|
| 1 | Storage schema + DB layer | Aishwarya | Gaurav |
| 2 | Phase-1 training (dataset→features→trainer→evaluate) | Aishwarya | Yashwanthi (metrics UI) |
| 3 | Ingestion + OCR + segmentation | Gaurav | Aishwarya |
| 4 | Evaluation (similarity→scorer→feedback→report) | Aishwarya | Gaurav (OCR/units) |
| 5 | Pipeline orchestrator + services + API | Aishwarya | Gaurav |
| 6 | Results dashboard + integration | Yashwanthi | Aishwarya, Gaurav |
| 7 | Demo data, tests, e2e polish | Yashwanthi | all |

---

*Update this file if ownership shifts.*
