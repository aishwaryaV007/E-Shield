# 1. FILE PURPOSE: Measures how many of the required rubric concepts / key points the student's answer actually contains.
# 2. RESPONSIBILITIES:
#    - For each rubric point, decide covered / partially-covered / missing / contradicted via embedding + optional NLI.
#    - Detect negation ("is not exothermic") so a contradiction is not counted as coverage.
#    - Output the concept-level breakdown that both the scorer and the feedback generator use.
# 3. PLANNED CONTENTS: coverage(student_answer, rubric_points) -> list[{point, status, score}].
# 4. INPUTS / OUTPUTS: Inputs: student answer + rubric points. Outputs: per-point coverage status.
# 5. DEPENDS ON / USED BY: models/embedder.py (optional NLI); used by scorer.py + feedback.py.
