# 1. FILE PURPOSE: (Phase 1 + Phase 2) Feature engineering — turns a (student_answer, answer_key) pair into the numeric features the mark-predictor learns from and scores on.
# 2. RESPONSIBILITIES:
#    - Compute semantic similarity (embedding cosine) between answer and key.
#    - Compute key-concept coverage, keyword recall, missing/extra-point counts, length ratio, negation cues.
#    - Return the SAME feature vector at train time and inference time (single source of truth).
# 3. PLANNED CONTENTS: extract_features(student_answer, answer_key, rubric) -> dict/np.ndarray; FEATURE_NAMES.
# 4. INPUTS / OUTPUTS: Inputs: answer text, key text, rubric points. Outputs: fixed-length feature vector.
# 5. DEPENDS ON / USED BY: models/embedder.py, numpy, scikit-learn; used by trainer.py AND evaluation/scorer.py.
