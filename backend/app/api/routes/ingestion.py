# 1. FILE PURPOSE: API routes for ingesting scanned answer scripts and reference material.
# 2. RESPONSIBILITIES:
#    - POST /ingest — accept uploaded PDFs/images for a batch and start preprocessing.
#    - POST /answer-key — upload the question paper + answer key + rubric for a batch.
# 3. PLANNED CONTENTS: FastAPI endpoint functions delegating to services/evaluation_service + app/ingestion/*.
# 4. INPUTS / OUTPUTS: Inputs: multipart uploads, batch id. Outputs: JSON ingest status / stored key metadata.
# 5. DEPENDS ON / USED BY: fastapi, api/schemas.py, services/evaluation_service.py, app/ingestion/*.
