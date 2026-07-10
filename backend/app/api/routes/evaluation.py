# NOTE: Phase 2 endpoints — run the auto-grading pipeline on a batch of scanned scripts.
# 1. FILE PURPOSE: API routes to trigger automated evaluation (OCR -> segment -> score -> feedback) and poll its status.
# 2. RESPONSIBILITIES:
#    - POST /evaluate — start grading an ingested batch against a question paper + answer key.
#    - GET /evaluate/status — progress of the evaluation run.
# 3. PLANNED CONTENTS: FastAPI APIRouter delegating to pipeline/orchestrator.evaluate_pipeline via the service.
# 4. INPUTS / OUTPUTS: Inputs: batch id + answer-key id. Outputs: run ack + status payloads.
# 5. DEPENDS ON / USED BY: fastapi, api/schemas.py, services/evaluation_service.py; called by the frontend.
