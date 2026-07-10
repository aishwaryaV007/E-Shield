# API Module

Contains FastAPI routes, grouped by domain:

- `routes/ingestion.py` — upload scanned scripts + answer keys (Phase 2 input).
- `routes/training.py` — Phase 1: train the mark-predictor and read metrics.
- `routes/evaluation.py` — Phase 2: run the auto-grading pipeline on a batch.
- `routes/results.py` — fetch evaluated sheets (question-wise marks, total, %, feedback).
