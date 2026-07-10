import pytest
import os
import tempfile
import aiosqlite
import json
from app.storage import db

@pytest.fixture
def temp_db():
    # Use a temporary file for the database
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    yield path
    os.remove(path)

@pytest.fixture
def schema_path():
    return os.path.join(os.path.dirname(__file__), "..", "app", "storage", "schema.sql")

@pytest.mark.asyncio
async def test_init_db(temp_db, schema_path):
    await db.init_db(temp_db, schema_path)
    
    # Verify tables were created
    async with db.get_connection(temp_db) as conn:
        cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in await cursor.fetchall()]
        assert "batches" in tables
        assert "questions" in tables

@pytest.mark.asyncio
async def test_crud_operations(temp_db, schema_path):
    await db.init_db(temp_db, schema_path)
    
    # 1. Create an Answer Key
    ak_id = await db.create_answer_key(temp_db, "Midterm 2024")
    assert ak_id > 0
    
    # 2. Add Questions
    rubric = json.dumps(["mentions AI", "mentions scaling"])
    q_id = await db.add_question(temp_db, ak_id, "Q1", "AI scaling is important", rubric, 5.0)
    assert q_id > 0
    
    # 3. Create a Batch
    batch_id = await db.create_batch(temp_db, "Section A", ak_id)
    assert batch_id > 0
    
    # 4. Create a Script
    script_id = await db.create_script(temp_db, batch_id, "STD001", 2)
    assert script_id > 0
    
    # 5. Add a Page
    page_id = await db.add_page(temp_db, script_id, 0, "/path/to/img.png")
    assert page_id > 0
    
    # 6. Save Evaluation
    eval_id = await db.save_evaluation(
        temp_db,
        script_id=script_id,
        question_id=q_id,
        answer_text="AI scaling matters",
        similarity=0.85,
        predicted_mark=4.5,
        max_marks=5.0,
        percent_match=90.0,
        feedback="Good answer",
        deduction_reasons="",
        low_confidence=0
    )
    assert eval_id > 0
    
    # Verify retrievals
    evals = await db.get_evaluations_for_script(temp_db, script_id)
    assert len(evals) == 1
    assert evals[0]["predicted_mark"] == 4.5
    
    scripts = await db.get_scripts_for_batch(temp_db, batch_id)
    assert len(scripts) == 1
    assert scripts[0]["roll_no"] == "STD001"
