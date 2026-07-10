# 1. FILE PURPOSE: End-to-end grading — a handwritten answer-script PDF -> a fully evaluated sheet.
# 2. FLOW: Model A (read PDF -> per-question answers) -> scorer (trained model -> marks) ->
#    report (question-wise marks, total, %, feedback). The mark is the model's, never an LLM's.
# 3. DEPENDS ON: pipeline/model_a_reader.py, evaluation/report.py.
from app.pipeline.model_a_reader import ModelAReader, load_answer_key
from app.evaluation.report import build_report


def grade_script(pdf_path: str, answer_key_path: str, question_path: str | None = None,
                 max_marks: float = 2.0, script_id: str | None = None) -> dict:
    """Read a script and produce its evaluated sheet."""
    key = load_answer_key(answer_key_path)
    reader = ModelAReader(key, question_path=question_path)
    answers = reader.read_script(pdf_path)
    sid = script_id or pdf_path.split("/")[-1].replace(".pdf", "")
    return build_report(sid, answers, key, max_marks=max_marks)
