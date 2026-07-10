# 1. FILE PURPOSE: Test suite for the training + evaluation modules (the auto-grading brain).
# 2. RESPONSIBILITIES:
#    - Test backend/app/training/features.py — feature vector is identical at train + inference time.
#    - Test backend/app/training/trainer.py + evaluate.py — model trains and reports RMSE/MAE/R2/±1-accuracy.
#    - Test backend/app/evaluation/similarity.py — higher similarity for closer answers.
#    - Test backend/app/evaluation/scorer.py — marks come from the trained model, clamped to [0, max].
#    - Test backend/app/evaluation/feedback.py — deduction reasons reference missing rubric points.
# 3. PLANNED CONTENTS: One test function per module; uses mock answers, keys, and a tiny trained model.
# 4. INPUTS / OUTPUTS: Inputs: mock (answer, key, mark) data. Outputs: pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/training/* + app/evaluation/* (via pyproject.toml pythonpath).
