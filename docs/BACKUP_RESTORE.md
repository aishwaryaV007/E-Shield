# Local Database Backup & Restore
> Database backing up procedures, script zip archiving, recovery steps, and retention guidelines.

*Design / Planned — Not yet implemented*

---

## 1. Local Backup Strategy

Because ExamShield operates offline as a desktop-and-local-server assistant, backups are managed by copy-archiving the SQLite database file and the raw scanned script directories:

```
┌────────────────────────────────────────────────────────┐
│ Client Desktop PC (Local Storage Drive)                 │
├────────────────────────────────────────────────────────┤
│  [ SQLite db.sqlite3 ] ──► (Copied to backup folder)    │
│  [ Scanned PDFs / PNGs ] ─► (Compressed as ZIP)         │
│                                                        │
│  Backups saved to local disk, external USB, or NAS     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Backup & Restore Procedures

### 1. Database Backup Script (`scripts/backup_db.py`)
To prevent data corruption during backup copying, the script uses SQLite's built-in backup API to make a safe online copy:

```python
# Planned implementation pattern
import sqlite3
import shutil
from datetime import datetime
import os

def backup_local_database(db_path: str, backup_dir: str):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.sqlite3")
    
    # Establish connection and perform backup
    conn = sqlite3.connect(db_path)
    backup_conn = sqlite3.connect(backup_file)
    with backup_conn:
        conn.backup(backup_conn)
        
    backup_conn.close()
    conn.close()
    print(f"Database backup completed: {backup_file}")
```

### 2. Archiving Scanned Scripts
The raw scanned answer booklets and coordinate crop directories are packaged into compressed ZIP files for storage:
```bash
zip -r /data/backups/scripts_backup_$(date +%Y%m%d).zip /data/corpus/
```

### 3. Database Restoration Steps
To restore the application to a previous backup state:
1.  Stop the FastAPI and Streamlit dashboard processes.
2.  Rename the active database file (`db.sqlite3` to `db_corrupted.sqlite3`).
3.  Copy the target backup database file to the workspace directory, renaming it to `db.sqlite3`.
4.  Extract the corresponding script images ZIP archive back to `/data/corpus/`.
5.  Restart the services and verify the data recovery in the dashboard.

---

## 3. Data Retention Guidelines

*   **Active Batches:** Keep scanned script images and extraction results in the main database directory throughout the active semester grading period.
*   **Archiving:** After final results are published and grade cards are exported, archive the SQLite database and compressed script ZIP files to secure local offline storage (e.g., college NAS or external drives).
*   **Deletions:** Delete raw scanned script files from the local application directory after 1 year to free up disk space, retaining the anonymized SQLite audit logs for registration reference.

---

## 4. Related Documents

*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Database Design specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [Disaster Recovery Procedures](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DISASTER_RECOVERY.md)
