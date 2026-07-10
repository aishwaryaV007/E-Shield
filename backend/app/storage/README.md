# Storage Module

Persistence for both phases.

- `db.py` — SQLite connection + schema init + CRUD helpers.
- `json_store.py` — JSON artefacts (answer keys, evaluated-sheet exports, training metrics).
- `schema.sql` — tables for batches, scripts, questions, answer keys, and per-question evaluations.
