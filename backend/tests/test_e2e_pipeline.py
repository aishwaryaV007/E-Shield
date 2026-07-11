import os
import pytest
from fastapi.testclient import TestClient

# Adjust path to find backend main
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

# Resolve test file paths
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PDF_PATH = os.path.join(REPO_DIR, "dataset/Test Data/page-1.pdf")
CSV_KEY_PATH = os.path.join(REPO_DIR, "dataset/answer_keys/answerkey.txt")
PROSE_KEY_PATH = os.path.join(REPO_DIR, "dataset/Test Data/answer_key.txt")
QUESTION_PATH = os.path.join(REPO_DIR, "dataset/Test Data/question_paper.txt")

def test_health_check():
    """Verify that the health check endpoint returns OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rate_limiting():
    """Verify that hitting /health (bypassed) doesn't rate limit, but many calls to health does not block."""
    # The rate limiter middleware ignores health check in our implementation, 
    # but let's confirm multiple requests to health return 200.
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200

def test_auth_token_login():
    """Verify that authenticating with correct credentials yields a JWT token."""
    response = client.post("/api/v1/auth/token", json={
        "username": "teacher",
        "password": "teacher123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_auth_token_invalid():
    """Verify that invalid credentials yield a 401 Unauthorized error."""
    response = client.post("/api/v1/auth/token", json={
        "username": "teacher",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

@pytest.mark.skipif(not os.path.exists(PDF_PATH), reason="Test PDF not found")
def test_e2e_grading_pipeline_csv_key():
    """Verify that the full end-to-end grading pipeline works with a CSV answer key."""
    # Ensure test files exist
    assert os.path.exists(PDF_PATH)
    assert os.path.exists(CSV_KEY_PATH)
    
    with open(PDF_PATH, "rb") as pdf_file, open(CSV_KEY_PATH, "rb") as key_file, open(QUESTION_PATH, "rb") as q_file:
        files = {
            "file": (os.path.basename(PDF_PATH), pdf_file, "application/pdf"),
            "answer_key": (os.path.basename(CSV_KEY_PATH), key_file, "text/plain"),
            "question_paper": (os.path.basename(QUESTION_PATH), q_file, "text/plain")
        }
        response = client.post(
            "/api/v1/grade",
            files=files,
            data={"max_marks": 2.0}
        )
        
    assert response.status_code == 200
    report = response.json()
    
    # Assert structural compliance
    assert "script_id" in report
    assert "total_marks" in report
    assert "max_total" in report
    assert "answers" in report
    assert len(report["answers"]) > 0
    
    # Validate report contents
    for answer in report["answers"]:
        assert "question_no" in answer
        assert "predicted_mark" in answer
        assert "max_marks" in answer
        assert "ocr_confidence" in answer
        assert "low_confidence" in answer

@pytest.mark.skipif(not os.path.exists(PDF_PATH), reason="Test PDF not found")
def test_e2e_grading_pipeline_prose_key():
    """Verify that the full end-to-end grading pipeline works with a plain text (prose) answer key."""
    assert os.path.exists(PDF_PATH)
    assert os.path.exists(PROSE_KEY_PATH)
    
    with open(PDF_PATH, "rb") as pdf_file, open(PROSE_KEY_PATH, "rb") as key_file, open(QUESTION_PATH, "rb") as q_file:
        files = {
            "file": (os.path.basename(PDF_PATH), pdf_file, "application/pdf"),
            "answer_key": (os.path.basename(PROSE_KEY_PATH), key_file, "text/plain"),
            "question_paper": (os.path.basename(QUESTION_PATH), q_file, "text/plain")
        }
        response = client.post(
            "/api/v1/grade",
            files=files,
            data={"max_marks": 2.0}
        )
        
    assert response.status_code == 200
    report = response.json()
    assert "script_id" in report
    assert "total_marks" in report
    assert len(report["answers"]) > 0
