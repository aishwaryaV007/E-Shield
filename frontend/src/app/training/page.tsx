/*
 1. FILE PURPOSE: Training page (Phase 1) — upload the historical corrected corpus, train the mark-predictor, and view metrics.
 2. RESPONSIBILITIES:
    - Upload past scripts + answer keys + rubrics + teacher marks; trigger training.
    - Show training progress and the resulting RMSE / MAE / R² / ±1-mark accuracy.
    - Display feature importance (which signals drive the predicted mark).
 3. PLANNED CONTENTS: TrainingPage() using hooks/useTraining + lib/api/training.
 4. INPUTS / OUTPUTS: Inputs: corpus upload. Outputs: trained-model metrics UI.
 5. DEPENDS ON / USED BY: hooks/useTraining, lib/api/training, ui/*.
*/
