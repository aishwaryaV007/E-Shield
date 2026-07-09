# 1. FILE PURPOSE: SQLite persistence layer (via aiosqlite).
# 2. RESPONSIBILITIES:
#    - Open/close the SQLite connection at DB_PATH.
#    - Initialise the schema from schema.sql on startup.
#    - Provide CRUD helpers for scripts, marks, flags, registers, templates.
# 3. PLANNED CONTENTS: init_db(); get_connection(); insert/query helpers per table.
# 4. INPUTS / OUTPUTS: Inputs: SQL params. Outputs: rows / cursors.
# 5. DEPENDS ON / USED BY: aiosqlite, config.py, schema.sql; used by services + engines for persistence.
