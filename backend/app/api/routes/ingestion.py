# 1. FILE PURPOSE: API routes for ingesting scanned answer scripts.
# 2. RESPONSIBILITIES:
#    - POST /ingest — accept uploaded PDFs/images for a batch and start preprocessing.
#    - POST /blankcheck — run page-count + ink-presence check on a script.
# 3. PLANNED CONTENTS: FastAPI endpoint functions delegating to services/batch_service + app/ingestion/*.
# 4. INPUTS / OUTPUTS: Inputs: multipart uploads, batch id. Outputs: JSON ingest status / blankcheck results.
# 5. DEPENDS ON / USED BY: fastapi, api/schemas.py, services/batch_service.py, app/ingestion/*.
