# services/ — Application service layer

Business-logic layer between the API routes and the two pipelines. Routes stay thin
(parse request → call a service → return a schema); the service coordinates the work.

## Files

- **`evaluation_service.py`** — the main service. Responsibilities:
  - create a batch and register its answer key + rubric,
  - run **Phase 1** training (delegates to `app/training/*`) and expose metrics,
  - run **Phase 2** evaluation for a batch (delegates to `app/pipeline/orchestrator.py`),
  - fetch evaluated sheets (question-wise marks, totals, feedback) for the frontend.

## Depends on / used by

- **Depends on:** `app/training/`, `app/pipeline/`, `app/evaluation/`, `app/storage/`.
- **Used by:** `app/api/routes/*`, injected via `get_evaluation_service()` in `app/api/deps.py`.

## Principle

The mark for every answer is produced by the **trained model** in `app/evaluation/scorer.py`
— never by an LLM prompt (Track 02 rule). Low-confidence OCR answers are flagged for optional
human verification before results are published.
