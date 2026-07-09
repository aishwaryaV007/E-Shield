# E-Shield — Team Work Split

> How the three of us divide E-Shield so we can build in parallel without stepping on each
> other. Ownership is by **workstream** (a coherent slice of the architecture), with clearly
> defined interfaces where workstreams meet. Read this alongside [`SETUP.md`](SETUP.md)
> (setup + recommended implementation order) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Team:** Gaurav · Aishwarya (Aishu) · Yashwanthi

---

## 1. Principles

- **Own a workstream, not scattered files.** Each person owns whole modules end-to-end so
  responsibility is unambiguous.
- **Contracts before code.** Where two workstreams meet, the interface (a Pydantic schema, a
  function signature, a JSON shape) is agreed first and treated as frozen until both sides
  agree to change it.
- **Backend is one team, split in two.** The backend is deliberately divided into two
  tightly-coupled tracks — **Data & OCR** and **Engines & API** — owned by Gaurav and
  Aishwarya. They share the same codebase and meet at the OCR→Engine and Storage↔Engine
  boundaries, so they pair closely day-to-day.
- **Rank & flag, never accuse.** Every workstream upholds the project rule: the system ranks
  and flags evidence; it never finalizes a grade. The human decides.

---

## 2. Ownership at a glance

| Track | Owner | Domain | Primary folders |
|-------|-------|--------|-----------------|
| **A — Data & OCR spine** | **Gaurav** | Backend | `backend/app/ingestion/`, `calibration/`, `ocr/`, `models/`, `storage/`, `utils/` |
| **B — Engines, Pipeline & API** | **Aishwarya** | Backend | `backend/app/engines/`, `pipeline/`, `services/`, `api/`, `backend/main.py`, `config.py` |
| **C — Dashboard, Integration & QA** | **Yashwanthi** | Frontend + Ops | `frontend/`, `deploy/`, `backend/tests/`, `scripts/seed_demo_data.py` |

> Tracks A and B together make up the backend and are built as a pair. Track C consumes the
> API that Track B exposes.

---

## 3. Track A — Data & OCR Spine  ·  Owner: **Gaurav**

The foundation everything else consumes: turn scanned scripts into clean, structured data and
persist it. If Track A's output is solid, the engines just read from it.

**Owns**
- `backend/app/ingestion/` — `pdf_loader.py` (PDF→image), `preprocess.py` (deskew/binarize),
  `blankcheck.py` (page count + ink presence).
- `backend/app/calibration/` — `template_io.py` (save/load zone-template JSON).
- `backend/app/ocr/` — `digit_ocr.py`, `prose_ocr.py`, `ambiguity.py` (the "never guess" fallback).
- `backend/app/models/` — `embedder.py` (MiniLM), `nli.py` (deberta) loaders, cached & local.
- `backend/app/storage/` — `db.py` (SQLite), `json_store.py`, `schema.sql`.
- `backend/app/utils/` — `image_ops.py` (evidence crops), `logging.py`.
- `scripts/download_models.py` — one-time model warm-up.

**Delivers**
- Deterministic OCR output per calibrated zone, with confidence + ambiguity flags.
- A working SQLite layer that Track B writes marks/flags into.
- Cached models that Track B's engines call.

**Definition of done:** a batch of scanned scripts can be ingested, preprocessed, OCR'd on
calibrated zones, and persisted — with ambiguous reads correctly marked, not guessed.

---

## 4. Track B — Engines, Pipeline & API  ·  Owner: **Aishwarya**

The intelligence and the interface: the five verification engines, the orchestration that runs
them, and the API the dashboard talks to. Built directly on top of Track A's OCR + storage.

**Owns**
- `backend/app/engines/` — `marksafe.py`, `copycatch.py`, `scriptid.py`, `reeval_guard.py`,
  `rubriclens.py`.
- `backend/app/pipeline/` — `orchestrator.py` (ingest → OCR → engines → persist → rank).
- `backend/app/services/` — `batch_service.py` (routes ↔ pipeline/engines).
- `backend/app/api/` — `routes/*` (ingestion, calibration, pipeline, results), `schemas.py`, `deps.py`.
- `backend/main.py`, `backend/config.py`.

**Delivers**
- Five engines that consume Track A's OCR/storage and emit ranked flags (never verdicts).
- The end-to-end pipeline run for a batch.
- A documented REST API + Pydantic schemas that Track C's dashboard consumes.

**Definition of done:** given persisted OCR data, the pipeline runs all engines, ranks flags
against the class baseline, and exposes them through the API.

---

## 5. Track C — Dashboard, Integration & QA  ·  Owner: **Yashwanthi**

Everything the auditor sees, plus the glue that proves the whole system works together.

**Owns**
- `frontend/` — the entire Next.js 14 dashboard:
  - `src/app/` pages (overview, ingestion, calibration, review, script detail),
  - `src/components/` (ZoneCanvas, FlagCard/FlagList, CollusionGraph, EvidenceCrop, layout, ui),
  - `src/lib/api/`, `src/hooks/`, `src/store/`, `src/types/`.
- `deploy/` — `docker-compose.yml` for running both apps.
- `backend/tests/` — test strategy and suites across the pipeline.
- `scripts/seed_demo_data.py` — the 35+ script demo corpus with planted errors.

**Delivers**
- The review dashboard: zone calibration canvas, ranked flag list, side-by-side evidence
  crops, and the interactive collusion graph.
- A repeatable demo dataset and the integration/e2e path from upload → flags on screen.

**Definition of done:** an auditor can upload scanned scripts, run the pipeline, and review
ranked flags with evidence in the browser — end to end.

---

## 6. Shared interfaces (where tracks meet)

| Boundary | Between | Contract to agree first |
|----------|---------|-------------------------|
| OCR output → Engine input | Gaurav ↔ Aishwarya | Shape of OCR results per zone (value, confidence, `is_ambiguous`). |
| Storage schema ↔ Engine writes | Gaurav ↔ Aishwarya | `schema.sql` tables (`marks`, `flags`) and the `db.py` write helpers. |
| Model loaders → Engines | Gaurav ↔ Aishwarya | `embedder.embed()` / `nli.classify()` signatures. |
| API schema ↔ Frontend types | Aishwarya ↔ Yashwanthi | `backend/app/api/schemas.py` mirrored by `frontend/src/types/index.ts`. |
| Demo data ↔ Pipeline | Yashwanthi ↔ Aishwarya | Input format the seed script produces vs. what ingestion expects. |

**Rule:** if you need to change a shared contract, both owners agree in the PR before merging.

---

## 7. Git workflow

Single shared repo, everyone targets `main`.

- Branch per workstream: `feat/gaurav-<topic>`, `feat/aishu-<topic>`, `feat/yashwanthi-<topic>`.
- **Always `git pull --rebase origin main` before pushing** so nobody overwrites another's work.
- Open a PR into `main`; the owner of any shared interface you touched reviews it.
- Small, focused commits (`feat:`, `fix:`, `docs:`, `test:`). Commits authored under your own
  identity.

---

## 8. Milestone alignment

Maps the SETUP.md build order onto owners so the critical path stays unblocked.

| Phase | Focus | Lead | Support |
|-------|-------|------|---------|
| 1 | Storage schema + DB layer | Gaurav | Aishwarya (schema review) |
| 2 | Ingestion + calibration | Gaurav | Yashwanthi (calibration UI) |
| 3 | OCR (digit + prose + ambiguity) | Gaurav | — |
| 4 | Engines (MarkSafe → ScriptID → ReEval → CopyCatch → RubricLens) | Aishwarya | Gaurav (OCR/data) |
| 5 | Pipeline orchestrator + services + API | Aishwarya | — |
| 6 | Dashboard + API integration | Yashwanthi | Aishwarya (API contract) |
| 7 | Demo data, tests, e2e polish | Yashwanthi | all |

> Track A leads early phases (the spine), Track B leads the middle (intelligence + API), and
> Track C leads the finish (dashboard + demo). Because A and B share the backend, Gaurav and
> Aishwarya pair continuously from Phase 1.

---

*Update this file if ownership shifts. It should always reflect who owns what right now.*
