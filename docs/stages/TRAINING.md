# Stage: Model Training (Phase 1)

> Learns teacher marking behaviour from historical corrected answer sheets. Produces the trained
> mark-predictor used in Phase 2. **The mark is a model prediction — never an LLM output.**

---

## 1. Objective

Instead of hand-written marking rules, fit a model that reproduces how teachers awarded marks on
past papers, so new answers can be graded the same way — consistently and explainably.

## 2. Inputs

- Previously corrected student answers **with teacher-awarded marks** (the labels).
- Official question papers, model answer keys, marking rubrics, and teacher feedback.

## 3. Steps (`backend/app/training/`)

1. **dataset_builder.py** — pair each historical answer with its answer key + the mark the teacher gave.
2. **features.py** — per answer, compute: semantic similarity to key, key-concept coverage,
   keyword recall, missing/extra-point counts, length ratio, negation cues. *(Same function is
   reused at inference time — one source of truth.)*
3. **trainer.py** — fit a regressor (XGBoost / RandomForest / MLP) mapping features → mark;
   support hyperparameter tuning + feature-importance (bonus scoring). Save to `models_cache/`.
4. **evaluate.py** — on a held-out split, report **RMSE, MAE, R², and accuracy within ±1 mark**.

## 4. Output

`models_cache/mark_predictor.pkl` + a metrics report (`data/metrics/`), surfaced on the Training
dashboard.

## 5. Fallback

If a labeled historical corpus isn't available in time, Phase 2 runs on an **unsupervised
similarity-to-key baseline** (map similarity % → marks directly). The trained model is the upgrade.
