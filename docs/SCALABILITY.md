# ExamShield Scalability Specification
> Local CPU performance for training + evaluation on standard laptops.

*Design / Planned — Not yet implemented*

---

## 1. Resource Model

Everything runs on the host machine. Phase 1 (training) is a one-time batch job; Phase 2
(evaluation) is what runs per exam batch.

```
[ Scanned batch (N scripts) ]
        │  (ingestion: OpenCV thread pool)
[ Clean pages ]
        │  (handwriting OCR — sequential CPU inference; the main cost)
[ Per-answer text ]
        │  (embedding similarity + trained-model prediction — fast on CPU)
[ Evaluated sheets ]
```

---

## 2. Run-time & Resource Targets (4-core CPU, 8 GB RAM)

### Phase 1 — Training (one-time)
| Stage | Complexity | Est. time (a few thousand answers) | Notes |
|-------|-----------|-------------------------------------|-------|
| Feature extraction | $O(A)$ over answers | ~seconds–minutes | Embeddings dominate; batch them. |
| XGBoost training + tuning | small | ~seconds | Tabular features → fast. |
| Evaluation (metrics) | $O(A)$ | ~seconds | RMSE/MAE/R²/±1-acc. |

### Phase 2 — Evaluation (per batch of N scripts)
| Stage | Complexity | Est. ($N=35$) | Est. ($N=300$) | Optimization |
|-------|-----------|---------------|----------------|--------------|
| Ingestion | $O(N \cdot P)$ | ~15 s | ~2.5 min | OpenCV multithreading. |
| Handwriting OCR | $O(N \cdot A)$ | ~2 min | ~15 min | The bottleneck; crop to answer regions, skip blanks. |
| Embedding similarity | $O(N \cdot A)$ | ~seconds | ~1 min | Batch-encode all answers once. |
| Trained-model scoring | $O(N \cdot A)$ | < 1 s | ~seconds | Vectorized feature matrix → one `predict`. |

*(A = answers per script.)* **Scoring is cheap; OCR dominates** — the opposite of a per-pair
collusion search, so there is no $O(N^2)$ term.

---

## 3. Optimizations

### 1. Batch the embeddings
Encode all answers in one MiniLM call — stack into a `(num_answers, 384)` array — instead of one
call per answer.
```python
import numpy as np
def score_batch(feature_matrix, model):     # (num_answers, num_features)
    return np.clip(model.predict(feature_matrix), 0, None)   # one vectorized prediction
```

### 2. Trim OCR surface
OCR only detected answer regions, skip blank areas — cuts scanned surface and time substantially.

### 3. Memory footprint
Discard high-res page matrices after OCR; share model weights (embedder + mark-predictor) as
single cached instances. Target RAM footprint under **~600 MB**.

---

## 4. Related Documents

*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Scorer stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)
*   [Database Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
