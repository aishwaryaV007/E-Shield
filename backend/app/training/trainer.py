# 1. FILE PURPOSE: (Phase 1) Trains the mark-predictor model that learns teacher marking behaviour from historical data.
# 2. RESPONSIBILITIES:
#    - Fit a regressor (XGBoost / RandomForest / small MLP) mapping answer features -> awarded mark.
#    - Support hyperparameter tuning and feature-importance reporting (bonus-scoring items).
#    - Persist the fitted model + feature spec to MODEL_DIR (models_cache/mark_predictor.pkl).
#    - NOTE: the mark is produced by this trained model, never by prompting an LLM (Track 02 rule).
# 3. PLANNED CONTENTS: train(dataset) -> model; save_model(model, path); tune_hyperparams(...).
# 4. INPUTS / OUTPUTS: Inputs: labeled DataFrame + features. Outputs: serialised trained model artifact.
# 5. DEPENDS ON / USED BY: xgboost/scikit-learn, joblib; consumes dataset_builder + features; evaluated by evaluate.py.
