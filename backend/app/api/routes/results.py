# NOTE: Calls services/batch_service.py to fetch flags and evidence
# 1. FILE PURPOSE: Provides the API contract for the frontend review dashboard to fetch ranked flags, single-script evidence crops, and CopyCatch graph JSON.
# 2. RESPONSIBILITIES:
#    - GET /flags for ranked review queue.
#    - GET /scripts/{id} for evidence.
#    - GET /graph for collusion data.
# 3. PLANNED CONTENTS: FastAPI APIRouter. Returns results from SQLite/JSON store.
# 4. INPUTS / OUTPUTS: Inputs: HTTP GET parameters. Outputs: structured JSON evidence.
# 5. DEPENDS ON / USED BY: FastAPI, SQLite, JSON store.
