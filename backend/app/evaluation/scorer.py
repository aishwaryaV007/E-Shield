# 1. FILE PURPOSE: Assign a mark to each answer by applying the trained mark-predictor to its
#    features — the automated grading step. The mark comes ONLY from the model, never an LLM.
# 2. RESPONSIBILITIES: build features (training/features.py), predict a PERCENTAGE (models/mark_model.py),
#    scale to the question's max_marks, clamp to [0, max].
# 3. DEPENDS ON / USED BY: models/mark_model.py, training/features.py; used by evaluation/report.py.
from app.training.features import extract_features
from app.models.mark_model import get_mark_model


def score_answer(student_answer: str, answer_key: str, max_marks: float) -> dict:
    """Grade one answer. Returns predicted mark + the features/percentage behind it."""
    feats = extract_features(student_answer, answer_key)
    pct = get_mark_model().predict_percentage(feats)      # trained model (or similarity baseline)
    raw = min(max(pct * max_marks, 0.0), max_marks)
    mark = round(raw * 2) / 2                              # round to the nearest half mark (0, 0.5, 1, ...)
    return {
        "predicted_mark": mark,
        "max_marks": max_marks,
        "percent": round(pct, 3),
        "similarity": feats["similarity"],
        "features": feats,
        "model_trained": get_mark_model().is_trained(),
    }
