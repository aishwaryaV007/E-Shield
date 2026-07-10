# 1. FILE PURPOSE: (Phase 1) Measures how well the trained mark-predictor reproduces the teachers' marks — the Track 02 "measurable performance" requirement.
# 2. RESPONSIBILITIES:
#    - Predict on a held-out test split and compare against teacher-awarded marks.
#    - Report RMSE, MAE, R2, and "accuracy within +/-1 mark" per question and overall.
#    - Persist a metrics report (JSON) surfaced on the training dashboard.
# 3. PLANNED CONTENTS: evaluate(model, test_df) -> metrics dict; write_report(metrics, path).
# 4. INPUTS / OUTPUTS: Inputs: trained model + test set. Outputs: RMSE/MAE/R2/±1-accuracy metrics report.
# 5. DEPENDS ON / USED BY: scikit-learn.metrics, numpy; used after trainer.py, read by api/routes/training.py.
