# 1. FILE PURPOSE: Loads and caches the sentence-embedding model (all-MiniLM-L6-v2) for CopyCatch.
# 2. RESPONSIBILITIES:
#    - Lazy-load SentenceTransformer('all-MiniLM-L6-v2') from local cache (MODEL_DIR).
#    - Provide embed(texts) -> dense embedding vectors on CPU.
#    - Keep a single cached model instance.
# 3. PLANNED CONTENTS: get_embedder() singleton; embed(texts: list[str]) -> np.ndarray.
# 4. INPUTS / OUTPUTS: Inputs: prose strings. Outputs: dense embedding matrix.
# 5. DEPENDS ON / USED BY: sentence-transformers, numpy; used by engines/copycatch.py.
