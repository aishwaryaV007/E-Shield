# Local Disaster Recovery Procedures
> Procedures for database corruption recovery, OCR pipeline crash resolution, and layout template restoration.

---

## 1. System Failure Vectors

Because ExamShield runs entirely on local machines, operational failures are typically caused by hardware issues, file system corruption, or software process crashes rather than network drops:

```
                  ┌──────────────────────────────┐
                  │ System Failure Event         │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   [ Vector 1: DB Lock ]   [ Vector 2: OCR Crash ] [ Vector 3: Spec Loss ]
   • SQLite db locked      • Memory page faults    • JSON layout missing
   • WAL recovery run      • Pipeline restart      • Import backup template
```

---

## 2. Failure Recovery Steps

### 1. SQLite Database Lock & Corruption Recovery
*   **Symptoms:** Dashboard queries time out; FastAPI returns `database is locked` error codes.
*   **Recovery Actions:**
    1.  Terminate the FastAPI server process to release active database locks.
    2.  Check for and delete SQLite lock files (`db.sqlite3-shm` and `db.sqlite3-wal`) if they persist after the process ends.
    3.  If the database file is corrupted, run the integrity check command:
        ```bash
        sqlite3 db.sqlite3 "PRAGMA integrity_check;"
        ```
    4.  If the database is unrecoverable, restore the database to its last clean state using the most recent backup copy, as detailed in the [Backup & Restore Guide](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/BACKUP_RESTORE.md).

### 2. OCR Pipeline Memory & Crash Recovery
*   **Symptoms:** Large batch runs freeze; the system runs out of RAM; the console logs Python segmentation faults.
*   **Recovery Actions:**
    1.  Restart the FastAPI server backend to release memory.
    2.  Check that the thread pool sizes in `preprocess.py` match the host machine's hardware configuration (reduce thread counts if running on machines with less than 8 GB of RAM).
    3.  Rerun the failed batch. The pipeline skips previously processed scripts by verifying existing rows in SQLite, resuming execution from the last unprocessed file.

### 3. Layout Calibration Template Restoration
*   **Symptoms:** Scanned scripts are misaligned; OCR extraction bounding boxes are shifted.
*   **Recovery Actions:**
    1.  Open the Calibration UI Canvas tab.
    2.  Re-align bounding box coordinate areas on a clean scanned script and save the updated configuration template.
    3.  Run a template update command to apply the updated coordinates to the batch:
        ```bash
        python scripts/reprocess_batch.py --batch-id {id} --template-id {template_id}
        ```
        This recalculates bounding box crops and updates the database records using the new alignment configurations.

---

## 3. Related Documents

*   [Application Monitoring Reference](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/MONITORING.md)
*   [Local Database Backup & Restore](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/BACKUP_RESTORE.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)

## To-Do List

- [ ] Define failover strategies
- [ ] Test disaster recovery plan locally
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
