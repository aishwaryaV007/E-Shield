# 1. FILE PURPOSE: Loads and caches the trained mark-predictor model (produced by Phase 1 training) for use during evaluation.
# 2. RESPONSIBILITIES:
#    - Lazy-load the serialised regressor + feature spec from MODEL_DIR (models_cache/mark_predictor.pkl).
#    - Expose predict(features) -> mark and report whether a trained model is available.
#    - Keep a single cached instance; fall back to the unsupervised similarity baseline if no model is trained yet.
# 3. PLANNED CONTENTS: get_mark_model() singleton; predict(features) -> float; is_trained() -> bool.
# 4. INPUTS / OUTPUTS: Inputs: feature vectors. Outputs: predicted marks.
# 5. DEPENDS ON / USED BY: joblib/xgboost; produced by training/trainer.py; used by evaluation/scorer.py.
