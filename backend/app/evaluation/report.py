# 1. FILE PURPOSE: Assemble the evaluated answer sheet — question-wise marks, total, percentage, feedback.
# 2. RESPONSIBILITIES: collect per-question scores + feedback; compute total + overall %;
#    flag low-confidence answers for human verification.
# 3. DEPENDS ON / USED BY: scorer.py, feedback.py; read by api/routes/results.py.
from app.evaluation.scorer import score_answer
from app.evaluation.feedback import build_feedback


def build_report(script_id: str, answers: dict[str, dict], answer_key: dict[str, str],
                 max_marks: float | dict[str, float] = 2.0) -> dict:
    """answers: {qno: {answer, similarity}} from Model A. max_marks may be a single value or a
    per-question dict {qno: marks}. Returns the full evaluated sheet."""
    rows, total, max_total = [], 0.0, 0.0
    for qno in sorted(answers, key=lambda q: int(q)):
        student = answers[qno]["answer"]
        key = answer_key.get(qno, "")
        mm = max_marks.get(qno, 2.0) if isinstance(max_marks, dict) else max_marks
        sc = score_answer(student, key, mm)
        fb = build_feedback(student, key, sc)
        # OCR confidence drives the "verify" flag (default 1.0 for human-corrected answers)
        ocr_conf = float(answers[qno].get("ocr_confidence", 1.0))
        total += sc["predicted_mark"]
        max_total += mm
        rows.append({
            "question_no": qno,
            "student_answer": student,
            "answer_key": key,
            "predicted_mark": sc["predicted_mark"],
            "max_marks": mm,
            "percent": sc["percent"],
            "similarity": sc["similarity"],
            "ocr_confidence": round(ocr_conf, 3),
            "feedback": fb["summary"],
            "deduction_reasons": fb["deduction_reasons"],
            "low_confidence": ocr_conf < 0.55,
        })
    return {
        "script_id": script_id,
        "total_marks": round(total, 2),
        "max_total": round(max_total, 2),
        "percentage": round(100 * total / max_total, 1) if max_total else 0.0,
        "low_confidence_count": sum(r["low_confidence"] for r in rows),
        "answers": rows,
    }
