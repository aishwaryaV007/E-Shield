# services/ — Application service layer

Business-logic layer that sits **between the API routes and the pipeline/engines**. Routes stay thin (parse request → call a service → return a schema); services coordinate the actual work and persistence.

## Files

- **`batch_service.py`** — the main service. Responsibilities:
  - create a batch and register its calibration template,
  - run the evaluation pipeline for a batch (delegates to `app/pipeline/orchestrator.py`),
  - fetch ranked flags for review,
  - fetch per-script evidence (marks, crops, collusion edges).

## Depends on / used by

- **Depends on:** `app/pipeline/`, `app/storage/` (db + json_store), `app/engines/`.
- **Used by:** `app/api/routes/*`, injected via the `get_batch_service()` dependency in `app/api/deps.py`.

## Principle

Rank and flag evidence; **never accuse, never finalize; the human decides.** Services return ranked/flagged data — they never write a final grade or resolve a flag automatically.
