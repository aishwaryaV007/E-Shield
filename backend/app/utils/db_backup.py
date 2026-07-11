import os
import sqlite3
import shutil
from datetime import datetime

def backup_db(db_path: str, backup_dir: str) -> str:
    """Performs an online, non-blocking backup of the active SQLite database."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Source database not found at {db_path}")
        
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"db_backup_{timestamp}.sqlite"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Establish source and destination connections
    src_conn = sqlite3.connect(db_path)
    dst_conn = sqlite3.connect(backup_path)
    try:
        with dst_conn:
            # Performs incremental backup safely
            src_conn.backup(dst_conn)
    finally:
        dst_conn.close()
        src_conn.close()
        
    return backup_path

def restore_db(backup_path: str, target_db_path: str):
    """Verifies a backup's integrity and safely replaces the active database."""
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup file not found at {backup_path}")
        
    # 1. Health check backup integrity before overwrite
    conn = sqlite3.connect(backup_path)
    try:
        result = conn.execute("PRAGMA integrity_check;").fetchone()
        if not result or result[0] != "ok":
            raise ValueError(f"Backup integrity check failed: {result}")
    except sqlite3.DatabaseError as e:
        raise ValueError("Backup file is corrupted. Restore aborted.") from e
    finally:
        conn.close()
        
    # 2. Safe transaction swap
    temp_target = target_db_path + ".tmp"
    shutil.copy2(backup_path, temp_target)
    
    if os.path.exists(target_db_path):
        rollback_target = target_db_path + ".rollback"
        if os.path.exists(rollback_target):
            os.remove(rollback_target)
        shutil.move(target_db_path, rollback_target)
        try:
            shutil.move(temp_target, target_db_path)
            os.remove(rollback_target)
        except Exception as e:
            # Rollback target to original
            if os.path.exists(rollback_target):
                shutil.move(rollback_target, target_db_path)
            raise e
    else:
        shutil.move(temp_target, target_db_path)
