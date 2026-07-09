# 1. FILE PURPOSE: Pre-fetches all required ML model weights to the local models_cache/ directory
#    so the pipeline runs fully offline at the venue with no Wi-Fi dependency.
# 2. RESPONSIBILITIES:
#    - Download PaddleOCR weights (text detection + recognition networks) via paddleocr warm-up.
#    - Download sentence-transformers all-MiniLM-L6-v2 to models_cache/ (used by backend/app/engines/copycatch.py).
#    - Download cross-encoder/nli-deberta-v3-xsmall to models_cache/ (used by backend/app/engines/rubriclens.py).
#    - Verify each model loads successfully and report download path.
# 3. PLANNED CONTENTS: download_all() function, one download_<model>() helper per model.
# 4. INPUTS / OUTPUTS: Inputs: Internet connection (run once pre-event). Outputs: Cached weights in models_cache/.
# 5. DEPENDS ON / USED BY: paddleocr, sentence-transformers; consumed offline by backend/app/models/embedder.py and nli.py.
