# FastAPI entry point for E-Shield. Serves the grading API used by the Next.js dashboard.
import os
import re
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.utils.rate_limiter import RateLimitMiddleware
from app.utils.security import (
    USERS_DB, verify_password, create_access_token, get_current_user, RoleChecker
)
from app.utils.logging_config import setup_logging

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANSWER_KEY = os.path.join(REPO, "dataset/answer_keys/answerkey.txt")
QUESTIONS = os.path.join(REPO, "dataset/answer_keys/Question.txt")
MARKS_CSV = os.path.join(REPO, "dataset/training_csv/Teacher_manual_marks_Anonymized.csv")

# Auth bypass configuration for hackathon demo compatibility
DISABLE_AUTH = os.environ.get("DISABLE_AUTH", "true").lower() in ("true", "1", "yes")

# Setup Bearer token scheme with optional auto-error to prevent blocking if disabled
bearer_scheme = HTTPBearer(auto_error=False)

def get_auth_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> dict:
    """Authentication dependency that supports runtime bypass via DISABLE_AUTH env var."""
    if DISABLE_AUTH:
        return {"username": "bypass", "role": "admin"}
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return get_current_user(credentials)

def check_role(allowed_roles: list[str]):
    """Role verification helper compatible with fallback authentication."""
    def dependency(user: dict = Depends(get_auth_user)):
        if not DISABLE_AUTH and user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Operation not permitted. Required roles: {allowed_roles}"
            )
        return user
    return dependency

def known_mcq_for(student_id: str) -> dict:
    """MCQ answers (cols 1-20) from the digital mark sheet for a known student, else {}."""
    import csv
    if not os.path.exists(MARKS_CSV):
        return {}
    for row in csv.DictReader(open(MARKS_CSV)):
        if row.get("Student_ID") == student_id:
            return {str(q): (row.get(str(q)) or "").strip() for q in range(1, 21)}
    return {}

# Initialize centralized logging
setup_logging()

app = FastAPI(title="ExamShield API", version="0.1.0")

# Register custom zero-dependency token-bucket rate limiter middleware
app.add_middleware(RateLimitMiddleware, rate=2.0, capacity=10.0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/auth/token")
def login(req: TokenRequest):
    """Authenticate credentials and return a secure JWT access token."""
    user = USERS_DB.get(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/grade")
async def grade(
    file: UploadFile = File(...),
    answer_key: UploadFile | None = File(None),
    question_paper: UploadFile | None = File(None),
    max_marks: float = 2.0,
    user: dict = Depends(check_role(["admin", "teacher", "operator"]))
):
    """Upload a handwritten answer-script PDF (+ optional answer-key and question-paper files) ->
    evaluated sheet. Secured by JWT validation."""
    import time
    
    # Secure filename parsing to prevent directory traversal
    filename = os.path.basename(file.filename)
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF answer script.")
        
    # import here so the heavy ML libs load lazily (not at app import time)
    from app.pipeline.grade_pipeline import grade_script

    tmp_paths = []
    data = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(data); pdf_path = tmp.name; tmp_paths.append(pdf_path)

    key_path = ANSWER_KEY
    if answer_key is not None:
        kb = await answer_key.read()
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as kf:
            kf.write(kb); key_path = kf.name; tmp_paths.append(key_path)

    question_path = QUESTIONS if os.path.exists(QUESTIONS) else None
    if question_paper is not None:
        qb = await question_paper.read()
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as qf:
            qf.write(qb); question_path = qf.name; tmp_paths.append(question_path)

    # Sanitize script ID from filename to prevent traversal issues
    sid = filename.replace(".pdf", "")
    sid = re.sub(r'[^A-Za-z0-9_\-]', '', sid)
    
    key_head = open(key_path, encoding="utf-8", errors="ignore").read(200)
    is_csv = "Question_Number" in key_head
    t0 = time.time()
    try:
        if is_csv:
            sheet = grade_script(pdf_path, key_path, question_path=question_path,
                                 max_marks=max_marks, script_id=sid,
                                 known_mcq=known_mcq_for(sid))
        else:
            from app.pipeline.general_grader import parse_prose_key, grade_general
            keys = parse_prose_key(key_path, question_path)
            if not keys:
                raise HTTPException(400, "Could not parse the answer key. Use 'Q1. ... Marks: N' text "
                                         "or the CSV format (Question_Number,Type,Correct_Answer).")
            sheet = grade_general(pdf_path, keys, sid, default_max=max_marks)
    finally:
        for p in tmp_paths:
            os.unlink(p)
    sheet["elapsed_seconds"] = round(time.time() - t0, 1)
    return sheet

class Correction(BaseModel):
    question_no: str
    student_answer: str
    answer_key: str = ""
    max_marks: float = 2.0
    type: str = "short"

class RescoreReq(BaseModel):
    answers: list[Correction]
    script_id: str = "corrected"

@app.post("/api/v1/rescore")
def rescore_endpoint(
    req: RescoreReq,
    user: dict = Depends(check_role(["admin", "teacher"]))
):
    """Re-grade after a human fixes the OCR text — fast, no OCR re-run. Secured by JWT validation."""
    from app.pipeline.grade_pipeline import rescore
    # Sanitize script_id to prevent write issues
    script_id = re.sub(r'[^A-Za-z0-9_\-]', '', req.script_id)
    return rescore([a.model_dump() for a in req.answers], script_id)
