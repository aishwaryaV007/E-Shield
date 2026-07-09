# 1. FILE PURPOSE: Detects student collusion. Runs prose OCR text through MiniLM sentence embeddings, computes the O(N^2) pairwise cosine-similarity matrix for the batch, z-score ranks pairs against the class baseline, and emits a NetworkX collusion graph as JSON. Never accuses — only flags for human review.
# 2. RESPONSIBILITIES:
#    - Prose OCR token filtering by confidence.
#    - Sentence embeddings via all-MiniLM-L6-v2.
#    - Z-score anomaly ranking.
#    - NetworkX graph generation.
# 3. PLANNED CONTENTS: CopyCatchEngine class. Takes in prose OCR. Computes similarities. Returns NetworkX JSON graph.
# 4. INPUTS / OUTPUTS: Inputs: prose OCR per script. Outputs: ranked suspicious pairs + graph JSON.
# 5. DEPENDS ON / USED BY: sentence-transformers, NumPy, scikit-learn, NetworkX, OCR pipeline.
