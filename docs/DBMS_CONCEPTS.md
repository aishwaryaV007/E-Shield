# ExamShield DBMS Concepts
> Details on local database transactions, write-ahead logging (WAL), Python thread-safety models, and normalization boundaries.

*Design / Planned — Not yet implemented*

---

## 1. Local Transactional Design & ACID Compliance

ExamShield implements **ACID-compliant transactions** locally via SQLite to ensure data integrity during execution. If an OCR thread fails mid-batch due to a file read error, all operations for that script rollback to prevent partial or corrupted records.

```
                    ┌──────────────────────────────┐
                    │  FastAPI / Ingestion Thread  │
                    └──────────────┬───────────────┘
                                   │
                ┌──────────────────▼──────────────────┐
                │ BEGIN EXCLUSIVE TRANSACTION         │
                ├─────────────────────────────────────┤
                │ • Insert script row                 │
                │ • Insert parsed marks fields        │
                │ • Insert similarity scores          │
                │ • Raise validation audit flags      │
                └──────────────────┬──────────────────┘
                                   │
                       ┌───────────┴───────────┐
                       │   Execution status?   │
                       └─────┬───────────┬─────┘
                             │           │
                     Success │           │ Exception / Failure
                             ▼           ▼
                      [ COMMIT ]    [ ROLLBACK ]
```

### ACID Rules
*   **Atomicity:** If a single sheet binarization or OCR extraction fails, the database rolls back all marks records for that sheet.
*   **Consistency:** Foreign key constraints prevent orphans (e.g., deleting a batch automatically deletes all related script and similarity matrix records).
*   **Isolation:** Exclusive locks prevent concurrent write operations during batch processing, while allowing read access for dashboard views.
*   **Durability:** Data commits directly to the local storage drive (`db.sqlite3`).

---

## 2. Concurrency & Performance Optimization

To prevent backend write processes from blocking Streamlit dashboard read queries, the engine configures SQLite with optimized database modes:

```sql
-- Planned database performance configurations
-- Enable Write-Ahead Logging (WAL) mode to support concurrent reads and writes
PRAGMA journal_mode = WAL;

-- Set synchronous flag to NORMAL to reduce disk writes while ensuring database safety
PRAGMA synchronous = NORMAL;

-- Configure database lock timeout (5000 milliseconds) to prevent busy exceptions
PRAGMA busy_timeout = 5000;

-- Enforce foreign key constraints
PRAGMA foreign_keys = ON;
```

*   **Write-Ahead Logging (WAL):** Allows writers to append changes to a separate WAL log file, enabling readers to query the database concurrently without locks.
*   **Connection Pool Thread Safety:** Because Python’s SQLite module restricts connections to the thread that created them, the engine uses thread-local storage or a thread-safe connection pool wrapper, establishing `check_same_thread=False` only when managing thread access safely.

---

## 3. Data Normalization Boundaries

*   **Structured Tables:** Marks extraction tables (`parsed_marks`) and similarity matrices are stored as normalized relational columns to support SQL aggregations and fast index lookups.
*   **JSON Serialization (Document Store Model):** Coordinates-based coordinates, page-specific layout boxes, and audit evidence payloads are stored as serialized JSON text strings. This approach avoids schema complexity and simplifies JSON exports for the dashboard UI.

---

## 4. Related Documents

*   [Database Schema Design spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [Performance & Scalability Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
*   [Local Storage Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
