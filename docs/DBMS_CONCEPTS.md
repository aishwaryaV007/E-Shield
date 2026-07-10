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
                │ • Insert per-question evaluations   │
                │ • Store predicted marks + feedback  │
                │ • Update script total + percentage  │
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
*   **Atomicity:** If OCR or scoring fails mid-script, the database rolls back all evaluation records for that script.
*   **Consistency:** Foreign key constraints prevent orphans (e.g., deleting a batch removes its scripts and their evaluation rows).
*   **Isolation:** Exclusive locks prevent concurrent write operations during batch processing, while allowing read access for dashboard views.
*   **Durability:** Data commits directly to the local storage drive (`db.sqlite3`).

---

## 2. Concurrency & Performance Optimization

To prevent backend write processes from blocking dashboard read queries, the app configures SQLite with optimized database modes:

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

*   **Structured Tables:** Per-question `evaluations` (predicted mark, similarity, max marks, percentage) and `questions` are stored as normalized relational columns for SQL aggregations and fast lookups.
*   **JSON Serialization (Document Store Model):** Rubric key-points, feedback, deduction reasons, and training metrics are stored as serialized JSON text strings — avoiding schema churn and simplifying exports to the dashboard UI.

---

## 4. Related Documents

*   [Database Schema Design spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [Performance & Scalability Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
*   [Local Storage Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
