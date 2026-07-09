# 1. FILE PURPOSE: Test suite for the storage layer in backend/app/storage/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/storage/db.py — SQLite connection, table creation, flag persistence.
#    - Test backend/app/storage/json_store.py — template JSON read/write round-trips.
# 3. PLANNED CONTENTS: Tests using a temporary SQLite DB; fixture tears down after each test.
# 4. INPUTS / OUTPUTS: Inputs: Temp DB path + JSON template payloads. Outputs: pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/storage/* (resolved via pyproject.toml pythonpath).
