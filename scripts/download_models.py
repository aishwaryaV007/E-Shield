# 1. FILE PURPOSE: Pre-fetches the required ML model weights to the local models_cache/ directory
#    so the pipeline runs fully offline at the venue with no Wi-Fi dependency.
# 2. RESPONSIBILITIES:
#    - Download a handwriting OCR model (TrOCR handwritten / PaddleOCR) weights.
#    - Download sentence-transformers all-MiniLM-L6-v2 (used by backend/app/models/embedder.py).
#    - Verify each model loads successfully and report the cache path.
#    - NOTE: this does NOT download any LLM — marks are produced by the trained regressor, not an LLM.
# 3. PLANNED CONTENTS: download_all() function, one download_<model>() helper per model.
# 4. INPUTS / OUTPUTS: Inputs: Internet connection (run once pre-event). Outputs: Cached weights in models_cache/.
# 5. DEPENDS ON / USED BY: transformers/paddleocr, sentence-transformers; consumed offline by backend/app/models/*.
