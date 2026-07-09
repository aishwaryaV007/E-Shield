-- E-Shield SQLite schema. Executed by app/storage/db.py on startup (init_db()).
-- Principle: the DB stores ranked flags and evidence; it never stores a verdict.
-- All timestamps are ISO-8601 text (SQLite has no native datetime type).

PRAGMA foreign_keys = ON;

-- Calibrated zone templates per sheet format (drawn once via the calibration canvas).
CREATE TABLE IF NOT EXISTS templates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    zones_json  TEXT NOT NULL,                               -- marks/total/roll-no/answer bboxes
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per uploaded batch of scripts.
CREATE TABLE IF NOT EXISTS batches (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    template_id INTEGER REFERENCES templates(id),
    status      TEXT NOT NULL DEFAULT 'created',             -- created|ingested|processed|reviewed
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per physical answer script in a batch.
CREATE TABLE IF NOT EXISTS scripts (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id          INTEGER NOT NULL REFERENCES batches(id),
    roll_no_ocr       TEXT,
    page_count        INTEGER,
    blankcheck_status TEXT,                                  -- ok|missing_pages|blank
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per scanned page of a script.
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id   INTEGER NOT NULL REFERENCES scripts(id),
    page_index  INTEGER NOT NULL,
    image_path  TEXT,
    ink_present INTEGER                                      -- 0/1 (BlankCheck)
);

-- Per-question marks extracted by MarkSafe (+ sum-verification fields).
CREATE TABLE IF NOT EXISTS marks (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id      INTEGER NOT NULL REFERENCES scripts(id),
    question_no    TEXT,
    mark_value     REAL,
    is_ambiguous   INTEGER NOT NULL DEFAULT 0,               -- 1 => 'Ambiguous — Human Review'
    written_total  REAL,
    computed_total REAL
);

-- Imported class-register rows (from CSV) used by ScriptID.
CREATE TABLE IF NOT EXISTS registers (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id     INTEGER NOT NULL REFERENCES batches(id),
    roll_no      TEXT NOT NULL,
    student_name TEXT,
    seat_no      TEXT
);

-- Every ranked flag raised by any engine. A flag is evidence, never a verdict.
CREATE TABLE IF NOT EXISTS flags (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    script_id      INTEGER NOT NULL REFERENCES scripts(id),
    engine         TEXT NOT NULL,                            -- marksafe|copycatch|scriptid|reeval|rubric
    severity_score REAL NOT NULL DEFAULT 0,
    reason         TEXT,
    evidence_ref   TEXT,                                     -- path/id of an evidence crop or graph node
    status         TEXT NOT NULL DEFAULT 'open',             -- open|reviewed
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_scripts_batch ON scripts(batch_id);
CREATE INDEX IF NOT EXISTS idx_flags_script  ON flags(script_id);
CREATE INDEX IF NOT EXISTS idx_marks_script  ON marks(script_id);
CREATE INDEX IF NOT EXISTS idx_pages_script  ON pages(script_id);
