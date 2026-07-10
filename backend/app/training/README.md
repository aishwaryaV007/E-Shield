# Training Module (Phase 1)

The heart of the Track 02 idea: instead of hand-written marking rules, we **learn** how
teachers grade from previously corrected answer sheets.

Pipeline: `dataset_builder` → `features` → `trainer` → `evaluate`.

- `dataset_builder.py` — assemble labeled rows (student answer, answer key, teacher mark) from the historical corpus.
- `features.py` — engineer the feature vector (semantic similarity, concept coverage, …); shared with Phase 2.
- `trainer.py` — fit + tune the mark-predictor regressor, save to `models_cache/`.
- `evaluate.py` — RMSE / MAE / R² / ±1-mark accuracy on a held-out split.

**Compliance:** the mark is always the output of this trained model — never an LLM prompt.
