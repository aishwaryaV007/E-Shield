# FastAPI entry point for E-Shield. Serves the grading API used by the Next.js dashboard.
import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANSWER_KEY = os.path.join(REPO, "dataset/answer_keys/answerkey.txt")
QUESTIONS = os.path.join(REPO, "dataset/answer_keys/Question.txt")

app = FastAPI(title="ExamShield API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/grade")
async def grade(file: UploadFile = File(...), max_marks: float = 2.0):
    """Upload a handwritten answer-script PDF -> evaluated sheet (question-wise marks, total, %)."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF answer script.")
    # import here so the heavy ML libs load lazily (not at app import time)
    from app.pipeline.grade_pipeline import grade_script

    data = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    try:
        sheet = grade_script(tmp_path, ANSWER_KEY,
                             question_path=QUESTIONS if os.path.exists(QUESTIONS) else None,
                             max_marks=max_marks,
                             script_id=file.filename.replace(".pdf", ""))
    finally:
        os.unlink(tmp_path)
    return sheet
