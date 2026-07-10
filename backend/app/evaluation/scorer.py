# 1. FILE PURPOSE: Assigns marks to each answer by applying the trained mark-predictor to the answer's features — the automated grading step.
# 2. RESPONSIBILITIES:
#    - Build the feature vector (via training/features.py) for each (student_answer, key, rubric) unit.
#    - Run the loaded trained model to predict a mark, scaled to the question's max marks.
#    - Apply percentage-based marking bands (e.g. 90-100% -> full) and clamp to [0, max].
#    - The mark comes ONLY from the trained model — never from an LLM prompt (Track 02 rule).
# 3. PLANNED CONTENTS: score_answer(unit) -> {mark, max, percent, features}; score_script(units) -> list.
# 4. INPUTS / OUTPUTS: Inputs: grading units + trained model. Outputs: predicted marks per question.
# 5. DEPENDS ON / USED BY: models/mark_model.py, training/features.py, evaluation/similarity.py; used by report.py.
