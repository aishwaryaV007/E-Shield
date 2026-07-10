# 1. FILE PURPOSE: Feature engineering — (student_answer, answer_key) -> the numeric matching
#    features the mark-predictor learns from and scores on. SAME function at train + inference.
# 2. RESPONSIBILITIES: semantic similarity, keyword recall, word overlap, length ratio, negation.
# 3. DEPENDS ON / USED BY: evaluation/similarity.py; used by trainer.py AND evaluation/scorer.py.
import re

from app.evaluation.similarity import answer_similarity

FEATURE_NAMES = ["similarity", "keyword_recall", "word_overlap", "length_ratio", "negation_flag"]

_STOP = set("a an the is are was were be been being of to in on for and or with as by that this it "
            "its at from into which who what when where how can could will would should may might "
            "must do does did has have had not no".split())
_NEG = re.compile(r"\b(not|no|never|none|cannot|can't|don't|doesn't|isn't|aren't|won't|n't)\b", re.I)


def _words(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", str(s).lower()) if w not in _STOP]


def extract_features(student_answer: str, answer_key: str) -> dict:
    """Return the fixed feature dict (keys == FEATURE_NAMES). Identical at train + inference."""
    s, k = set(_words(student_answer)), set(_words(answer_key))
    kw_recall = len(s & k) / len(k) if k else 0.0
    overlap = len(s & k) / len(s | k) if (s | k) else 0.0
    lr = min(len(_words(student_answer)) / max(1, len(_words(answer_key))), 3.0)
    return {
        "similarity": round(answer_similarity(student_answer, answer_key), 4),
        "keyword_recall": round(kw_recall, 4),
        "word_overlap": round(overlap, 4),
        "length_ratio": round(lr, 4),
        "negation_flag": 1 if _NEG.search(str(student_answer)) else 0,
    }


def to_vector(feats: dict) -> list[float]:
    """Order a feature dict into the canonical FEATURE_NAMES vector for the model."""
    return [feats[name] for name in FEATURE_NAMES]
