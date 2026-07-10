# 1. FILE PURPOSE: (Phase 1) Measure how well the mark-predictor reproduces professor marks —
#    the Track 02 "measurable performance" requirement.
# 2. RESPONSIBILITIES: grouped 80/20 holdout (unseen questions); report RMSE, MAE, R2,
#    ±1-mark accuracy, and the same on partial-credit answers + a predict-mean baseline.
# 3. DEPENDS ON / USED BY: scikit-learn, xgboost; used by trainer.py, read by api/routes/training.py.
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

MAX_MARKS_REF = 5.0


def _pack(y_true, y_pred, max_marks=MAX_MARKS_REF) -> dict:
    return {
        "rmse": round(float(mean_squared_error(y_true, y_pred) ** 0.5), 4),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 4),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "accuracy_within_1_mark": round(float(np.mean(np.abs((y_true - y_pred) * max_marks) <= 1.0)), 4),
    }


def grouped_metrics(X, y, groups, params: dict) -> dict:
    """80/20 split grouped by question (unseen questions in test). Model vs mean baseline,
    plus a focused view on the partial-credit answers where grading actually matters."""
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42).split(X, y, groups))
    model = XGBRegressor(subsample=0.9, colsample_bytree=0.9, random_state=42, **params).fit(X[tr], y[tr])
    pred = np.clip(model.predict(X[te]), 0, 1)
    base = np.full(len(te), y[tr].mean())
    out = {
        "n_train": int(len(tr)), "n_test": int(len(te)),
        "unseen_questions": int(len(set(groups[te]))),
        "model": _pack(y[te], pred),
        "baseline_mean": _pack(y[te], base),
    }
    partial = y[te] < 1.0
    if partial.sum() > 5:
        out["partial_credit_model"] = _pack(y[te][partial], pred[partial])
        out["partial_credit_model"]["corr"] = round(float(np.corrcoef(pred[partial], y[te][partial])[0, 1]), 3)
        out["partial_credit_baseline_acc1"] = round(
            float(np.mean(np.abs((y[te][partial] - base[partial]) * MAX_MARKS_REF) <= 1.0)), 4)
    return out
