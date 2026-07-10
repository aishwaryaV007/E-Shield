# NOTE: Phase 1 endpoints — build dataset, train the mark-predictor, expose metrics.
# 1. FILE PURPOSE: API routes to run Phase-1 model training and read the resulting evaluation metrics.
# 2. RESPONSIBILITIES:
#    - POST /train — build the dataset from the historical corpus and fit the mark-predictor (background task).
#    - GET /train/status — training progress.
#    - GET /train/metrics — RMSE/MAE/R2/±1-accuracy of the trained model.
# 3. PLANNED CONTENTS: FastAPI APIRouter delegating to app/training/* via services/evaluation_service.
# 4. INPUTS / OUTPUTS: Inputs: corpus path / config. Outputs: training status + metrics JSON.
# 5. DEPENDS ON / USED BY: fastapi, api/schemas.py, app/training/*; called by the frontend Training page.
