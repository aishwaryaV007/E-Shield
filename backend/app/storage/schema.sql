-- E-Shield SQLite schema. Executed by app/storage/db.py on startup (init_db()).
-- Stores answer keys, scanned scripts, and the auto-graded evaluations (question-wise marks + feedback).
-- All timestamps are ISO-8601 text (SQLite has no native datetime type).

PRAGMA foreign_keys = ON;

-- Registry of trained mark-predictor models (Phase 1 output).
CREATE TABLE IF NOT EXISTS models (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,
    artifact_path TEXT NOT NULL,                              -- models_cache/mark_predictor.pkl
    metrics_json TEXT,                                        -- RMSE / MAE / R2 / ±1-accuracy
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per uploaded batch of scripts to be graded.
CREATE TABLE IF NOT EXISTS batches (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    answer_key_id INTEGER REFERENCES answer_keys(id),
    model_id      INTEGER REFERENCES models(id),
    status        TEXT NOT NULL DEFAULT 'created',            -- created|ingested|evaluated
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- The official question paper + answer key + rubric for a batch.
CREATE TABLE IF NOT EXISTS answer_keys (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per question in an answer key (with its model answer + max marks).
CREATE TABLE IF NOT EXISTS questions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_key_id INTEGER NOT NULL REFERENCES answer_keys(id),
    question_no   TEXT NOT NULL,
    key_text      TEXT,                                       -- model answer text
    rubric_json   TEXT,                                       -- list of rubric key-points
    max_marks     REAL NOT NULL
);

-- One row per physical answer script in a batch.
CREATE TABLE IF NOT EXISTS scripts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id     INTEGER NOT NULL REFERENCES batches(id),
    roll_no      TEXT,
    page_count   INTEGER,
    total_marks  REAL,                                        -- filled after evaluation
    percentage   REAL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per scanned page of a script.
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id   INTEGER NOT NULL REFERENCES scripts(id),
    page_index  INTEGER NOT NULL,
    image_path  TEXT
);

-- The auto-grader's output: one row per (script, question) evaluated answer.
CREATE TABLE IF NOT EXISTS evaluations (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id         INTEGER NOT NULL REFERENCES scripts(id),
    question_id       INTEGER NOT NULL REFERENCES questions(id),
    answer_text       TEXT,                                   -- OCR'd student answer
    similarity        REAL,                                   -- semantic similarity to key
    predicted_mark    REAL,                                   -- from the trained model
    max_marks         REAL,
    percent_match     REAL,
    feedback          TEXT,                                   -- per-answer feedback
    deduction_reasons TEXT,                                   -- why marks were lost
    low_confidence    INTEGER NOT NULL DEFAULT 0,             -- 1 => OCR unreadable, verify before publishing
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_scripts_batch    ON scripts(batch_id);
CREATE INDEX IF NOT EXISTS idx_questions_key     ON questions(answer_key_id);
CREATE INDEX IF NOT EXISTS idx_evals_script      ON evaluations(script_id);
CREATE INDEX IF NOT EXISTS idx_evals_question    ON evaluations(question_id);
CREATE INDEX IF NOT EXISTS idx_pages_script      ON pages(script_id);
