# Backend Application

AI answer-sheet evaluator (Track 02 — Predictive Analytics / ML-DL).

## Setup & Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Module Map
- `app/api`: HTTP routes (ingestion, training, evaluation, results).
- `app/training`: **Phase 1** — build dataset + train the mark-predictor + report metrics.
- `app/ingestion` & `app/ocr`: **Phase 2 input** — PDF→image, handwriting OCR.
- `app/segmentation`: split scripts into questions and match them to the answer key.
- `app/evaluation`: **Phase 2 core** — semantic similarity + trained model → marks + feedback.
- `app/models`: local model loaders (embedder + trained mark-predictor).
- `app/pipeline`: end-to-end orchestration for both phases.
- `app/services`: business logic between routes and pipelines.
- `app/storage`: SQLite & JSON persistence.

**Compliance:** marks are produced by the trained model in `app/evaluation/scorer.py` — never
by prompting an LLM (Track 02 prohibits LLM-generated predictions).
