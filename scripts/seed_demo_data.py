# 1. FILE PURPOSE: Generates the 35+ script demo corpus with planted errors for evaluation testing
#    and live judging demo (per ExamShield_Workflow.md pre-event checklist).
# 2. RESPONSIBILITIES:
#    - Generate synthetic answer-sheet images with marks grids and prose answers.
#    - Plant exactly 2 colluder pairs (near-identical prose answers) detectable by backend/app/engines/copycatch.py.
#    - Plant totaling errors detectable by backend/app/engines/marksafe.py.
#    - Plant 1 duplicate roll-no, 1 absentee-with-sheet, 1 present-without-sheet for backend/app/engines/scriptid.py.
#    - Plant borderline totals (39 when pass=40) for backend/app/engines/reeval_guard.py.
#    - Write output images to data/raw/ and register CSV to data/registers/.
# 3. PLANNED CONTENTS: seed_batch() function; per-engine error-planting helpers.
# 4. INPUTS / OUTPUTS: Inputs: Config (batch size, error counts). Outputs: data/raw/ images + data/registers/register.csv.
# 5. DEPENDS ON / USED BY: Pillow, NumPy, pandas; output consumed by the backend ingestion pipeline.
