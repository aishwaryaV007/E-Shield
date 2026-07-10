# 1. FILE PURPOSE: (Phase 1) Train the mark-predictor — XGBoost mapping matching features ->
#    mark PERCENTAGE (0-1), so one model generalises to any max-mark scheme.
# 2. RESPONSIBILITIES: tune (GroupKFold), fit, save model + feature spec + metrics.
#    The mark is produced by this trained model, never by an LLM (Track 02).
# 3. USAGE: python -m app.training.trainer  (reads the Model B training table, writes mark_predictor.pkl)
import json
import os

import numpy as np
import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import GroupKFold

from app.training.features import FEATURE_NAMES
from app.training.evaluate import grouped_metrics

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
TABLE = os.path.join(REPO, "dataset/processed/model_b_train_table.csv")
OUT = os.path.join(REPO, "models_cache/mark_predictor.pkl")
METRICS = os.path.join(REPO, "dataset/processed/model_b_metrics.json")
_GRID = [dict(n_estimators=n, max_depth=d, learning_rate=lr)
         for n in (200, 400) for d in (3, 4) for lr in (0.03, 0.05)]


def train(table_path: str = TABLE, out_path: str = OUT, metrics_path: str = METRICS) -> dict:
    df = pd.read_csv(table_path)
    X, y, g = df[FEATURE_NAMES].values, df["mark_percentage"].values, df["question_id"].values

    # tune by GroupKFold RMSE (test on unseen questions)
    gkf = GroupKFold(n_splits=5)
    best, best_rmse = None, 9e9
    for p in _GRID:
        r = []
        for tri, tei in gkf.split(X, y, g):
            m = XGBRegressor(subsample=0.9, colsample_bytree=0.9, random_state=42, **p).fit(X[tri], y[tri])
            r.append(float(np.sqrt(np.mean((np.clip(m.predict(X[tei]), 0, 1) - y[tei]) ** 2))))
        if np.mean(r) < best_rmse:
            best_rmse, best = float(np.mean(r)), p

    metrics = grouped_metrics(X, y, g, best)
    metrics["cv_rmse"] = round(best_rmse, 4)
    metrics["params"] = best

    final = XGBRegressor(subsample=0.9, colsample_bytree=0.9, random_state=42, **best).fit(X, y)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    joblib.dump({"model": final, "features": FEATURE_NAMES, "max_marks_ref": 5.0, "params": best}, out_path)
    metrics["feature_importance"] = dict(zip(FEATURE_NAMES, [round(float(i), 3) for i in final.feature_importances_]))
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    json.dump(metrics, open(metrics_path, "w"), indent=2)
    return metrics


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))
