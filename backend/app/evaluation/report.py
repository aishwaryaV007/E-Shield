# 1. FILE PURPOSE: Assembles the final evaluated answer sheet for a script — question-wise marks, total, percentage, and feedback.
# 2. RESPONSIBILITIES:
#    - Collect per-question marks (scorer) + feedback (feedback) into one script report.
#    - Compute total marks and overall percentage.
#    - Mark low-confidence / unreadable answers for optional human verification before publishing.
#    - Persist the evaluation to storage and expose it to the results API.
# 3. PLANNED CONTENTS: build_report(script_id, scored_units) -> ScriptEvaluation; save + serialise.
# 4. INPUTS / OUTPUTS: Inputs: scored units + feedback. Outputs: full evaluated sheet (marks/total/%/feedback).
# 5. DEPENDS ON / USED BY: scorer.py, feedback.py, ocr/confidence.py, storage; read by api/routes/results.py.
