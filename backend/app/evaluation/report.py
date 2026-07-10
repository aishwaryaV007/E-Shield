# 1. FILE PURPOSE: Assemble the evaluated answer sheet — question-wise marks, total, percentage, feedback.
# 2. RESPONSIBILITIES: grade MCQs (exact-match) and short answers (trained model); compute total + %;
#    flag low-confidence answers for human verification.
# 3. DEPENDS ON / USED BY: scorer.py, feedback.py; read by api/routes/results.py.
from app.evaluation.scorer import score_answer
from app.evaluation.feedback import build_feedback


def _grade_mcq(student: str, correct: str, mm: float) -> tuple[dict, dict]:
    """MCQ: exact letter match -> full marks or 0."""
    s = (student or "").strip().upper()[:1]
    c = (correct or "").strip().upper()[:1]
    ok = bool(s) and s == c
    sc = {"predicted_mark": mm if ok else 0.0, "max_marks": mm, "percent": 1.0 if ok else 0.0,
          "similarity": 1.0 if ok else 0.0}
    fb = {"summary": "Correct" if ok else f"Incorrect (chose {s or '—'})",
          "deduction_reasons": [] if ok else [f"correct option is {c}"]}
    return sc, fb


def build_report(script_id: str, answers: dict[str, dict], keys: dict[str, dict],
                 max_marks: float | dict[str, float] = 2.0) -> dict:
    """answers: {qno: {answer, type, ocr_confidence}} from Model A.
    keys: {qno: {"type": "mcq"|"short", "correct": letter_or_text}}. Returns the evaluated sheet."""
    rows, total, max_total = [], 0.0, 0.0
    for qno in sorted(answers, key=lambda q: int(q)):
        a = answers[qno]
        student = a["answer"]
        kinfo = keys.get(qno, {"type": a.get("type", "short"), "correct": ""})
        qtype = kinfo.get("type", "short")
        correct = kinfo.get("correct", "")
        mm = max_marks.get(qno, 2.0) if isinstance(max_marks, dict) else max_marks

        if qtype == "mcq":
            sc, fb = _grade_mcq(student, correct, mm)
        else:
            sc = score_answer(student, correct, mm)
            fb = build_feedback(student, correct, sc)
        ocr_conf = float(a.get("ocr_confidence", 1.0))
        total += sc["predicted_mark"]
        max_total += mm
        rows.append({
            "question_no": qno,
            "type": qtype,
            "student_answer": student,
            "answer_key": correct,
            "predicted_mark": round(sc["predicted_mark"], 2),
            "max_marks": mm,
            "percent": round(sc["percent"], 3),
            "similarity": round(sc["similarity"], 3),
            "ocr_confidence": round(ocr_conf, 3),
            "feedback": fb["summary"],
            "deduction_reasons": fb["deduction_reasons"],
            "low_confidence": ocr_conf < 0.55,
        })
    mcq_rows = [r for r in rows if r["type"] == "mcq"]
    short_rows = [r for r in rows if r["type"] != "mcq"]
    return {
        "script_id": script_id,
        "total_marks": round(total, 2),
        "max_total": round(max_total, 2),
        "percentage": round(100 * total / max_total, 1) if max_total else 0.0,
        "mcq_marks": round(sum(r["predicted_mark"] for r in mcq_rows), 2),
        "mcq_max": round(sum(r["max_marks"] for r in mcq_rows), 2),
        "descriptive_marks": round(sum(r["predicted_mark"] for r in short_rows), 2),
        "descriptive_max": round(sum(r["max_marks"] for r in short_rows), 2),
        "low_confidence_count": sum(r["low_confidence"] for r in rows),
        "answers": rows,
    }
