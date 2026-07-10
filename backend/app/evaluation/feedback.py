# 1. FILE PURPOSE: Per-answer feedback + mark-deduction reasons, so the sheet explains itself.
# 2. RESPONSIBILITIES: from the match features + key-term coverage, produce plain-language feedback.
#    An LLM may only phrase this text — the MARK is never decided here.
# 3. DEPENDS ON / USED BY: training/features (key-term overlap); used by evaluation/report.py.
import re

_STOP = set("a an the is are was were be of to in on for and or with as by that this it its at from "
            "into which who what when where how".split())


def _key_terms(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", str(text).lower()) if w not in _STOP and len(w) > 3]


def build_feedback(student_answer: str, answer_key: str, score: dict) -> dict:
    """Feedback from key-term coverage + the predicted percentage. Deterministic, explainable."""
    key_terms = set(_key_terms(answer_key))
    present = {t for t in key_terms if t in set(_key_terms(student_answer))}
    missing = sorted(key_terms - present)
    pct = score["percent"]
    if pct >= 0.9:
        summary = "Strong answer — covers the expected points."
    elif pct >= 0.6:
        summary = "Partially correct — some key points covered, others missing."
    else:
        summary = "Weak match to the expected answer."
    return {
        "summary": summary,
        "covered_points": sorted(present),
        "deduction_reasons": [f"missing: {m}" for m in missing[:5]],
        "low_confidence": score.get("similarity", 1.0) < 0.2,
    }
