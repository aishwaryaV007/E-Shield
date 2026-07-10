# 1. FILE PURPOSE: Computes semantic similarity between a student's answer and the official answer key (meaning, not keyword overlap).
# 2. RESPONSIBILITIES:
#    - Embed student answer and answer key with the local sentence-embedding model.
#    - Return cosine similarity plus sentence-level alignment (which key points are covered).
#    - Provide the primary signal for percentage-based marking.
# 3. PLANNED CONTENTS: answer_similarity(student, key) -> float; aligned_points(student, key) -> list.
# 4. INPUTS / OUTPUTS: Inputs: student + key text. Outputs: similarity score + covered-point map.
# 5. DEPENDS ON / USED BY: models/embedder.py, numpy; used by training/features.py and evaluation/scorer.py.
