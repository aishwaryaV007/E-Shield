# 1. FILE PURPOSE: Exposes the main FastAPI endpoints to trigger the evaluation pipeline (Scan -> Preprocess -> OCR -> Features) and check batch status.
# 2. RESPONSIBILITIES:
#    - POST /run to start processing.
#    - GET /status to poll progress.
#    - Coordinate engine execution.
# 3. PLANNED CONTENTS: FastAPI APIRouter. Maps HTTP requests to background tasks.
# 4. INPUTS / OUTPUTS: Inputs: batch IDs. Outputs: status updates.
# 5. DEPENDS ON / USED BY: FastAPI, pipeline modules.
