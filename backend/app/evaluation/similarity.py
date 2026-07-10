# 1. FILE PURPOSE: Semantic similarity between a student's answer and the official answer key.
# 2. RESPONSIBILITIES: cosine similarity (meaning, not keyword overlap) via the local embedder;
#    this is the primary "matching score" feature for percentage-based marking.
# 3. DEPENDS ON / USED BY: models/embedder.py; used by training/features.py and evaluation/scorer.py.
import numpy as np
from sentence_transformers import util
from app.models.embedder import get_embedder


def answer_similarity(student: str, key: str) -> float:
    """Cosine similarity in [0, 1] between a student answer and the answer key."""
    if not student or not key:
        return 0.0
    return float(np.clip(get_embedder().cosine(student, key), 0.0, 1.0))


def similarity_matrix(answers: list[str], keys: list[str]) -> np.ndarray:
    """Pairwise cosine similarity (len(answers) x len(keys)) — used for question matching."""
    emb = get_embedder()
    a = emb.encode([x or "" for x in answers])
    k = emb.encode([x or "" for x in keys])
    return util.cos_sim(a, k).cpu().numpy()
