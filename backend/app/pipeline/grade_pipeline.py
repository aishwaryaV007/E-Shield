# 1. FILE PURPOSE: End-to-end grading — a handwritten answer-script PDF -> a fully evaluated sheet.
# 2. FLOW: Model A (read PDF -> per-question answers) -> report (MCQs exact-match + short answers
#    scored by the trained model -> question-wise marks, total, %). The mark is the model's / the key.
# 3. DEPENDS ON: pipeline/model_a_reader.py, evaluation/report.py.
from app.pipeline.model_a_reader import (
    ModelAReader, load_answer_key, load_mcq_key, parse_max_marks,
)
from app.evaluation.report import build_report


def _typed_keys(short_key: dict[str, str], mcq_key: dict[str, str]) -> dict[str, dict]:
    keys = {q: {"type": "mcq", "correct": v} for q, v in mcq_key.items()}
    keys.update({q: {"type": "short", "correct": v} for q, v in short_key.items()})
    return keys


def grade_script(pdf_path: str, answer_key_path: str, question_path: str | None = None,
                 max_marks: float = 2.0, script_id: str | None = None) -> dict:
    """Read a script and produce its evaluated sheet (MCQs + short answers). Per-question max marks
    are parsed from the question paper (MCQs default 1, short answers default `max_marks`)."""
    short_key = load_answer_key(answer_key_path)
    mcq_key = load_mcq_key(answer_key_path)
    per_q = parse_max_marks(answer_key_path, question_path, short_key, default=max_marks)
    per_q.update(parse_max_marks(answer_key_path, question_path, mcq_key, default=1.0))

    reader = ModelAReader(short_key, mcq_key=mcq_key, question_path=question_path)
    answers = reader.read_script(pdf_path)
    sid = script_id or pdf_path.split("/")[-1].replace(".pdf", "")
    return build_report(sid, answers, _typed_keys(short_key, mcq_key), max_marks=per_q)


def rescore(corrections: list[dict], script_id: str = "corrected") -> dict:
    """Re-grade human-corrected answers WITHOUT OCR (fast). Each item:
    {question_no, student_answer, answer_key, max_marks, type}."""
    answers = {c["question_no"]: {"answer": c["student_answer"], "type": c.get("type", "short"),
                                  "ocr_confidence": 1.0} for c in corrections}
    keys = {c["question_no"]: {"type": c.get("type", "short"), "correct": c.get("answer_key", "")}
            for c in corrections}
    mm = {c["question_no"]: float(c.get("max_marks", 2.0)) for c in corrections}
    return build_report(script_id, answers, keys, max_marks=mm)
