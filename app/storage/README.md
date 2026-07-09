# ExamShield Storage Module
> Specifications for local data storage, schema definitions, and JSON serialization.

*Design / Planned — Not yet implemented*

---

## 1. Storage Strategy

ExamShield is designed to run offline on local machines. It avoids high-latency external servers, database clusters, or cloud authentication systems, storing all data in a single local **SQLite database** file and local **JSON template** logs.

```
                      ┌────────────────────────────────┐
                      │   ExamShield local Package      │
                      └───────────────┬────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
    ┌────────────▼────────────┐               ┌────────────▼────────────┐
    │   SQLite Database       │               │   JSON Templates File   │
    │   (db.sqlite3)          │               │   (templates/)          │
    │   • Batches & Scripts   │               │   • Bounding box zones  │
    │   • Extracted Marks     │               │   • Calibration layout  │
    │   • Similarity matrix   │               │   • System configs      │
    │   • Audit Flag logs     │               │                         │
    └─────────────────────────┘               └─────────────────────────┘
```

---

## 2. SQLite Database Schema (`schema.sql`)

The database contains tables for processing logs, OCR extraction data, audit flags, and manual overrides.

```sql
-- Planned database schema
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,          -- UUID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,         -- 'processing', 'completed', 'failed'
    script_count INTEGER
);

CREATE TABLE IF NOT EXISTS scripts (
    id TEXT PRIMARY KEY,          -- UUID
    batch_id TEXT REFERENCES batches(id) ON DELETE CASCADE,
    roll_number TEXT,             -- Extracted ID
    original_file_path TEXT,
    page_count INTEGER,
    blank_pages TEXT,             -- JSON list of page indexes
    is_borderline INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS parsed_marks (
    id TEXT PRIMARY KEY,
    script_id TEXT REFERENCES scripts(id) ON DELETE CASCADE,
    question_number TEXT NOT NULL,
    marks_extracted REAL,         -- OCR result
    marks_resolved REAL,          -- User override value
    confidence REAL,
    bounding_box TEXT             -- JSON coordinates array
);

CREATE TABLE IF NOT EXISTS audit_flags (
    id TEXT PRIMARY KEY,
    script_id TEXT REFERENCES scripts(id) ON DELETE CASCADE,
    engine_name TEXT NOT NULL,     -- 'MarkSafe', 'CopyCatch', 'ScriptID'
    flag_type TEXT NOT NULL,       -- 'SUM_MISMATCH', 'DUPLICATE_ID'
    evidence_payload TEXT,         -- JSON crop URLs and matching values
    status TEXT DEFAULT 'PENDING'  -- 'PENDING', 'RESOLVED'
);

CREATE TABLE IF NOT EXISTS similarity_matrix (
    script_a_id TEXT REFERENCES scripts(id) ON DELETE CASCADE,
    script_b_id TEXT REFERENCES scripts(id) ON DELETE CASCADE,
    similarity_score REAL NOT NULL,
    PRIMARY KEY (script_a_id, script_b_id)
);
```

---

## 3. Serialization Structures

*   **Calibration Templates (`templates/*.json`):** Coordinates-based layout JSON schemas map coordinates relative to image scale ratios, as detailed in the [Calibration Module Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/calibration/README.md).
*   **Result Backups:** During batch processing, intermediate analysis results are serialized to JSON files in `data/results/` to prevent data loss in the event of an application crash.

---

## 4. Related Documents

*   [Calibration Coordinates Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/calibration/README.md)
*   [Database Schema Design spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [Database Concepts](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DBMS_CONCEPTS.md)
