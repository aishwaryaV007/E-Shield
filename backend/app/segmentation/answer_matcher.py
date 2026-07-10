# 1. FILE PURPOSE: Aligns each detected student answer block with the correct question in the question paper + answer key.
# 2. RESPONSIBILITIES:
#    - Match a segmented answer to its question number (handles skipped / out-of-order answers).
#    - Attach the official answer-key text, rubric points, and max marks to each student answer.
#    - Produce the (student_answer, answer_key, rubric, max_marks) tuples the scorer consumes.
# 3. PLANNED CONTENTS: AnswerMatcher class; match(answer_blocks, answer_key) -> list[GradingUnit].
# 4. INPUTS / OUTPUTS: Inputs: answer blocks + answer key. Outputs: grading units ready for scoring.
# 5. DEPENDS ON / USED BY: rapidfuzz/regex; used by pipeline (Phase 2) before evaluation/scorer.
