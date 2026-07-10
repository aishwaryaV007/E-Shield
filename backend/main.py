# 1. FILE PURPOSE: FastAPI application entry point / app factory.
# 2. RESPONSIBILITIES:
#    - Create the FastAPI instance and configure CORS from settings.
#    - Include the API routers (ingestion, training, evaluation, results).
#    - Initialise the SQLite schema on startup and expose a /health check.
# 3. PLANNED CONTENTS: create_app() factory returning FastAPI; module-level `app` for uvicorn; startup hook.
# 4. INPUTS / OUTPUTS: Inputs: Settings + routers. Outputs: ASGI `app` served by `uvicorn main:app`.
# 5. DEPENDS ON / USED BY: fastapi, config.py, app/api/routes/*, app/storage/db.py.
