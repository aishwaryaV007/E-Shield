import aiosqlite
import json
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any, AsyncGenerator

@asynccontextmanager
async def get_connection(db_path: str) -> AsyncGenerator[aiosqlite.Connection, None]:
    """Provides a transactional database connection."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db
        await db.commit()

async def init_db(db_path: str, schema_path: str) -> None:
    """Initializes the database using the schema file."""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()
    
    async with get_connection(db_path) as db:
        await db.executescript(schema)

# --- Batches ---

async def create_batch(db_path: str, name: str, answer_key_id: Optional[int] = None, model_id: Optional[int] = None) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute(
            "INSERT INTO batches (name, answer_key_id, model_id) VALUES (?, ?, ?)",
            (name, answer_key_id, model_id)
        )
        return cursor.lastrowid

async def update_batch_status(db_path: str, batch_id: int, status: str) -> None:
    async with get_connection(db_path) as db:
        await db.execute(
            "UPDATE batches SET status = ? WHERE id = ?",
            (status, batch_id)
        )

async def get_batch(db_path: str, batch_id: int) -> Optional[aiosqlite.Row]:
    async with get_connection(db_path) as db:
        cursor = await db.execute("SELECT * FROM batches WHERE id = ?", (batch_id,))
        return await cursor.fetchone()

# --- Answer Keys & Questions ---

async def create_answer_key(db_path: str, name: str) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute("INSERT INTO answer_keys (name) VALUES (?)", (name,))
        return cursor.lastrowid

async def add_question(
    db_path: str, 
    answer_key_id: int, 
    question_no: str, 
    key_text: Optional[str], 
    rubric_json: Optional[str], 
    max_marks: float
) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute(
            """INSERT INTO questions (answer_key_id, question_no, key_text, rubric_json, max_marks)
               VALUES (?, ?, ?, ?, ?)""",
            (answer_key_id, question_no, key_text, rubric_json, max_marks)
        )
        return cursor.lastrowid

async def get_questions_for_key(db_path: str, answer_key_id: int) -> List[aiosqlite.Row]:
    async with get_connection(db_path) as db:
        cursor = await db.execute("SELECT * FROM questions WHERE answer_key_id = ?", (answer_key_id,))
        return await cursor.fetchall()

# --- Scripts & Pages ---

async def create_script(db_path: str, batch_id: int, roll_no: Optional[str] = None, page_count: Optional[int] = None) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute(
            "INSERT INTO scripts (batch_id, roll_no, page_count) VALUES (?, ?, ?)",
            (batch_id, roll_no, page_count)
        )
        return cursor.lastrowid

async def add_page(db_path: str, script_id: int, page_index: int, image_path: str) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute(
            "INSERT INTO pages (script_id, page_index, image_path) VALUES (?, ?, ?)",
            (script_id, page_index, image_path)
        )
        return cursor.lastrowid

async def get_scripts_for_batch(db_path: str, batch_id: int) -> List[aiosqlite.Row]:
    async with get_connection(db_path) as db:
        cursor = await db.execute("SELECT * FROM scripts WHERE batch_id = ?", (batch_id,))
        return await cursor.fetchall()

# --- Evaluations ---

async def save_evaluation(
    db_path: str,
    script_id: int,
    question_id: int,
    answer_text: Optional[str],
    similarity: Optional[float],
    predicted_mark: Optional[float],
    max_marks: Optional[float],
    percent_match: Optional[float],
    feedback: Optional[str],
    deduction_reasons: Optional[str],
    low_confidence: int = 0
) -> int:
    async with get_connection(db_path) as db:
        cursor = await db.execute(
            """INSERT INTO evaluations (
                script_id, question_id, answer_text, similarity, predicted_mark,
                max_marks, percent_match, feedback, deduction_reasons, low_confidence
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                script_id, question_id, answer_text, similarity, predicted_mark,
                max_marks, percent_match, feedback, deduction_reasons, low_confidence
            )
        )
        return cursor.lastrowid

async def get_evaluations_for_script(db_path: str, script_id: int) -> List[aiosqlite.Row]:
    async with get_connection(db_path) as db:
        cursor = await db.execute("SELECT * FROM evaluations WHERE script_id = ?", (script_id,))
        return await cursor.fetchall()
