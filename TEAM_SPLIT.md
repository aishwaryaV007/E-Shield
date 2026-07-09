# E-Shield — Team Work Split

> How the three of us divide E-Shield so we can build in parallel without stepping on each
> other. Ownership is by **workstream** (a coherent vertical slice of the product), with clearly
> defined interfaces where workstreams meet. Read this alongside [`SETUP.md`](SETUP.md)
> (setup + recommended implementation order) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Team:** Gaurav · Aishwarya (Aishu) · Yashwanthi

---

## 1. Principles

- **Own a vertical slice, not scattered files.** Each person owns coherent modules end-to-end
  so responsibility is unambiguous.
- **Contracts before code.** Where two workstreams meet, the interface (a Pydantic schema, a
  function signature, a JSON shape) is agreed first and treated as frozen until both sides
  agree to change it.
- **One full-stack track spans the seam.** The ingestion→OCR path is owned front-to-back by a
  single person (Gaurav), so the calibration/ingestion UI and the backend that powers it move
  together. This keeps Gaurav in daily contact with both the backend (Aishwarya) and the
  frontend shell (Yashwanthi).
- **Rank & flag, never accuse.** Every workstream upholds the project rule: the system ranks
  and flags evidence; it never finalizes a grade. The human decides.

---

## 2. Ownership at a glance

| Track | Owner | Domain | Primary areas |
|-------|-------|--------|---------------|
| **A — Ingestion & OCR (full-stack)** | **Gaurav** | Backend **+** Frontend | `backend/app/ingestion/`, `ocr/`, `utils/` **+** frontend ingestion & calibration UI |
| **B — Backend core: Engines, API & Data** | **Aishwarya** | Backend | `backend/app/engines/`, `pipeline/`, `services/`, `api/`, `storage/`, `models/`, `calibration/`, `main.py`, `config.py` |
| **C — Review dashboard, Integration & QA** | **Yashwanthi** | Frontend + Ops | frontend review/overview UI, `deploy/`, `backend/tests/`, `scripts/seed_demo_data.py` |

> Gaurav and Aishwarya jointly own the backend and meet at the OCR→Engine, Storage, and
> ingestion-API boundaries — they pair continuously. Gaurav also owns the front-end slice that
> drives ingestion, so he works with Yashwanthi on the shared UI shell.

---

## 3. Track A — Ingestion & OCR (full-stack)  ·  Owner: **Gaurav**

A complete vertical slice: the backend that turns scanned scripts into clean OCR data, **and**
the front-end screens the operator uses to feed and calibrate that pipeline.

**Owns — backend**
- `backend/app/ingestion/` — `pdf_loader.py` (PDF→image), `preprocess.py` (deskew/binarize),
  `blankcheck.py` (page count + ink presence).
- `backend/app/ocr/` — `digit_ocr.py`, `prose_ocr.py`, `ambiguity.py` (the "never guess" fallback).
- `backend/app/utils/` — `image_ops.py` (evidence crops), `logging.py`.

**Owns — frontend**
- `frontend/src/app/ingestion/page.tsx` — upload scripts + BlankCheck view.
- `frontend/src/app/calibration/page.tsx` — zone-calibration screen.
- `frontend/src/components/calibration/ZoneCanvas.tsx` — draw marks/total/roll-no/answer zones.
- `frontend/src/lib/api/ingestion.ts` — ingestion + BlankCheck API calls.
- `frontend/src/hooks/usePipeline.ts` — run/trigger + status hooks (shared surface with Track C).

**Delivers**
- Deterministic OCR output per calibrated zone, with confidence + ambiguity flags.
- The operator-facing UI to upload, calibrate, and kick off a batch — wired to the backend above.

**Definition of done:** from the browser, an operator can upload scanned scripts, draw/save a
zone template, run BlankCheck, and produce OCR output — with ambiguous reads marked, not guessed.

---

## 4. Track B — Backend Core: Engines, API & Data  ·  Owner: **Aishwarya**

The intelligence and the data foundation: the five verification engines, the orchestration and
API, plus the storage/model layer everything reads and writes.

**Owns**
- `backend/app/engines/` — `marksafe.py`, `copycatch.py`, `scriptid.py`, `reeval_guard.py`,
  `rubriclens.py`.
- `backend/app/pipeline/` — `orchestrator.py` (ingest → OCR → engines → persist → rank).
- `backend/app/services/` — `batch_service.py` (routes ↔ pipeline/engines).
- `backend/app/api/` — `routes/*` (ingestion, calibration, pipeline, results), `schemas.py`, `deps.py`.
- `backend/app/storage/` — `db.py` (SQLite), `json_store.py`, `schema.sql`.
- `backend/app/models/` — `embedder.py` (MiniLM), `nli.py` (deberta) loaders, cached & local.
- `backend/app/calibration/` — `template_io.py` (save/load zone-template JSON, backend side).
- `backend/main.py`, `backend/config.py`, `scripts/download_models.py`.

**Delivers**
- Five engines that consume Track A's OCR output and emit ranked flags (never verdicts).
- The end-to-end pipeline run, the persistence layer, and a documented REST API + schemas.

**Definition of done:** given OCR output from Track A, the pipeline persists it, runs all
engines, ranks flags against the class baseline, and exposes them through the API.

---

## 5. Track C — Review Dashboard, Integration & QA  ·  Owner: **Yashwanthi**

Everything the auditor reviews, the app shell, and the glue that proves the system works
end-to-end.

**Owns — frontend**
- `frontend/src/app/` shell + review side — `layout.tsx`, `globals.css`, `page.tsx` (overview),
  `review/page.tsx`, `scripts/[id]/page.tsx`.
- `frontend/src/components/` — `layout/` (Sidebar, Header), `review/` (FlagCard, FlagList,
  CollusionGraph, EvidenceCrop), `ui/` (Button, Card, Badge, Spinner), `Providers.tsx`.
- `frontend/src/lib/api/` — `client.ts`, `pipeline.ts`, `results.ts`.
- `frontend/src/hooks/useFlags.ts`, `frontend/src/store/`, `frontend/src/types/`.

**Owns — ops & QA**
- `deploy/` — `docker-compose.yml`.
- `backend/tests/` — test strategy and suites across the pipeline.
- `scripts/seed_demo_data.py` — the 35+ script demo corpus with planted errors.

**Delivers**
- The review dashboard: ranked flag list, side-by-side evidence crops, and the interactive
  collusion graph, on top of the shared app shell + client.
- A repeatable demo dataset and the integration/e2e path from run → flags on screen.

**Definition of done:** an auditor can open the app, review ranked flags with evidence and the
collusion graph, and the demo dataset reproduces all flag types.

---

## 6. Shared interfaces (where tracks meet)

| Boundary | Between | Contract to agree first |
|----------|---------|-------------------------|
| OCR output → Engine input | Gaurav ↔ Aishwarya | Shape of OCR results per zone (value, confidence, `is_ambiguous`). |
| Ingestion/pipeline API | Gaurav ↔ Aishwarya | `api/routes/ingestion.py` + `pipeline` endpoints vs. `lib/api/ingestion.ts` / `usePipeline`. |
| Calibration template | Gaurav ↔ Aishwarya | Zone-template JSON: `ZoneCanvas` (UI) ↔ `template_io.py` (backend). |
| API schema ↔ Frontend types | Aishwarya ↔ Yashwanthi | `api/schemas.py` mirrored by `frontend/src/types/index.ts`. |
| App shell ↔ ingestion pages | Gaurav ↔ Yashwanthi | Shared `layout.tsx`, `Providers`, `store`, `ui/` used by Gaurav's pages. |
| Demo data ↔ Pipeline | Yashwanthi ↔ Aishwarya | Input format the seed script produces vs. what ingestion expects. |

**Rule:** if you need to change a shared contract, both owners agree in the PR before merging.

---

## 7. Git workflow

Single shared repo, everyone targets `main`.

- Branch per workstream: `feat/gaurav-<topic>`, `feat/aishu-<topic>`, `feat/yashwanthi-<topic>`.
- **Always `git pull --rebase origin main` before pushing** so nobody overwrites another's work.
- Open a PR into `main`; the owner of any shared interface you touched reviews it.
- Small, focused commits (`feat:`, `fix:`, `docs:`, `test:`). Commits authored under your own identity.

---

## 8. Milestone alignment

Maps the SETUP.md build order onto owners so the critical path stays unblocked.

| Phase | Focus | Lead | Support |
|-------|-------|------|---------|
| 1 | Storage schema + DB layer + models | Aishwarya | Gaurav (OCR data needs) |
| 2 | Ingestion + calibration (backend + UI) | Gaurav | Yashwanthi (app shell) |
| 3 | OCR (digit + prose + ambiguity) | Gaurav | Aishwarya (engine inputs) |
| 4 | Engines (MarkSafe → ScriptID → ReEval → CopyCatch → RubricLens) | Aishwarya | Gaurav (OCR/data) |
| 5 | Pipeline orchestrator + services + API | Aishwarya | Gaurav (ingestion API) |
| 6 | Review dashboard + API integration | Yashwanthi | Aishwarya (API), Gaurav (shell) |
| 7 | Demo data, tests, e2e polish | Yashwanthi | all |

> Gaurav runs the full ingestion→OCR slice across backend and frontend (Phases 2–3), pairs with
> Aishwarya on the backend seam (Phases 1, 4–5), and shares the frontend shell with Yashwanthi
> (Phase 6). Aishwarya anchors the backend core; Yashwanthi anchors the review UI and QA.

---

*Update this file if ownership shifts. It should always reflect who owns what right now.*
