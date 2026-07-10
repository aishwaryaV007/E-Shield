# Pipeline Module

Chains the stages of both phases together.

## Phase 1 — Training (`train_pipeline`)
1. **dataset_builder** — assemble labeled rows from the historical corrected corpus.
2. **features** — engineer the feature vector per answer.
3. **trainer** — fit + tune the mark-predictor; save to `models_cache/`.
4. **evaluate** — RMSE / MAE / R² / ±1-mark accuracy on a held-out split.

## Phase 2 — Evaluation (`evaluate_pipeline`)
1. **Ingestion** — load PDF/images, deskew, denoise, binarize.
2. **OCR** — extract handwritten answer text + confidence.
3. **Segmentation** — split into questions, match each to its answer key + rubric.
4. **Evaluation** — semantic similarity + concept coverage → **trained model** predicts marks.
5. **Feedback + Report** — per-answer feedback, deduction reasons, total, percentage.
6. **Storage** — persist evaluated sheets; the API serves them to the frontend.

**Compliance:** marks come from the trained model in `evaluation/scorer.py` — never from an LLM.
