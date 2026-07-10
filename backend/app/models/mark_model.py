# 1. FILE PURPOSE: Load the trained mark-predictor (Phase 1 output) and predict a mark PERCENTAGE.
# 2. RESPONSIBILITIES: lazy-load models_cache/mark_predictor.pkl; predict a percentage (0-1);
#    fall back to the unsupervised similarity baseline if no model has been trained yet.
# 3. COMPLIANCE: the mark is this model's prediction — never an LLM. Percentage x max_marks = mark.
# 4. DEPENDS ON / USED BY: joblib/xgboost; produced by training/trainer.py; used by evaluation/scorer.py.
import os
from functools import lru_cache

import joblib
import numpy as np

from app.training.features import FEATURE_NAMES, to_vector

DEFAULT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../models_cache/mark_predictor.pkl"))


class MarkModel:
    def __init__(self, path: str | None = None):
        self.path = path or os.environ.get("MARK_MODEL_PATH", DEFAULT_PATH)
        self.model = None
        self.features = FEATURE_NAMES
        if os.path.exists(self.path):
            bundle = joblib.load(self.path)
            self.model = bundle["model"]
            self.features = bundle.get("features", FEATURE_NAMES)

    def is_trained(self) -> bool:
        return self.model is not None

    def predict_percentage(self, feats: dict) -> float:
        """Predict fraction of marks (0-1). Falls back to similarity if untrained."""
        if self.model is None:
            return float(np.clip(feats.get("similarity", 0.0), 0.0, 1.0))  # baseline
        x = np.array([to_vector(feats)], dtype=float)
        return float(np.clip(self.model.predict(x)[0], 0.0, 1.0))


@lru_cache(maxsize=1)
def get_mark_model() -> MarkModel:
    return MarkModel()
