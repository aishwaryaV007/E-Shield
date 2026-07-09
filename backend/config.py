# 1. FILE PURPOSE: Central typed configuration for the backend, loaded from environment variables (.env).
# 2. RESPONSIBILITIES:
#    - Define a Settings class (pydantic-settings BaseSettings) holding all runtime config.
#    - Expose DB_PATH, DATA_DIR, MODEL_DIR, CORS_ORIGINS, LOG_LEVEL with sensible defaults.
#    - Provide a cached get_settings() accessor used across the app.
# 3. PLANNED CONTENTS: Settings(BaseSettings) with env binding; get_settings() lru_cache factory.
# 4. INPUTS / OUTPUTS: Inputs: backend/.env + process env. Outputs: a validated Settings singleton.
# 5. DEPENDS ON / USED BY: pydantic-settings; used by main.py, api/deps.py, storage/db.py, models/*.
