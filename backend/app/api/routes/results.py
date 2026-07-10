# NOTE: Calls services/evaluation_service.py to fetch evaluated sheets.
# 1. FILE PURPOSE: API contract for the frontend to fetch the evaluated answer sheets produced by Phase 2.
# 2. RESPONSIBILITIES:
#    - GET /results — list evaluated scripts in a batch with totals + percentages.
#    - GET /results/{script_id} — full evaluated sheet: question-wise marks, feedback, deduction reasons.
#    - GET /results/{script_id}/answers — per-answer detail (student text, key, similarity, mark).
# 3. PLANNED CONTENTS: FastAPI APIRouter. Returns ScriptEvaluation / AnswerResult from SQLite/JSON store.
# 4. INPUTS / OUTPUTS: Inputs: HTTP GET parameters. Outputs: structured evaluated-sheet JSON.
# 5. DEPENDS ON / USED BY: FastAPI, SQLite, JSON store; consumed by the frontend Results pages.
