# 1. FILE PURPOSE: Local sentence-embedding model (all-MiniLM-L6-v2) for semantic similarity.
# 2. RESPONSIBILITIES: load the model once (cached), encode text, expose cosine similarity.
# 3. DEPENDS ON / USED BY: sentence-transformers; used by evaluation/similarity.py and training/features.py.
import os
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util

DEFAULT_MODEL = "all-MiniLM-L6-v2"


class Embedder:
    """Wraps a local sentence-transformer. Offline: weights are cached under models_cache/."""

    def __init__(self, model_name: str = DEFAULT_MODEL, cache_dir: str | None = None):
        if cache_dir is None:
            default = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../models_cache"))
            cache_dir = os.environ.get("MODEL_DIR", default)
        self.model = SentenceTransformer(model_name, cache_folder=cache_dir)

    def encode(self, texts, batch_size: int = 64):
        return self.model.encode(texts, batch_size=batch_size, convert_to_tensor=True,
                                 show_progress_bar=False)

    def cosine(self, a: str, b: str) -> float:
        ea, eb = self.encode([a or ""]), self.encode([b or ""])
        return float(util.cos_sim(ea, eb)[0][0])


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    """Process-wide singleton so the model loads only once."""
    return Embedder()
