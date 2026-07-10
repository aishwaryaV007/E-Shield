# 1. FILE PURPOSE: Shared FastAPI dependencies injected into route handlers.
# 2. RESPONSIBILITIES:
#    - Provide an aiosqlite DB connection dependency.
#    - Provide a settings dependency (get_settings).
#    - Provide the evaluation service dependency used by routes.
# 3. PLANNED CONTENTS: get_db() async generator; get_settings_dep(); get_evaluation_service().
# 4. INPUTS / OUTPUTS: Inputs: settings + DB path. Outputs: yielded db connection / service instances.
# 5. DEPENDS ON / USED BY: fastapi.Depends; config.py, storage/db.py, services/evaluation_service.py; used by all routes.
