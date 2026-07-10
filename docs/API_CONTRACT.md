# ExamShield API Contracts
> REST API for the FastAPI backend — training, evaluation, and results.

*Design / Planned — Not yet implemented*

Backend runs locally at `http://localhost:8000`. The Next.js dashboard uses these endpoints.

---

## 1. Training (Phase 1)

### `POST /api/v1/train`
Build the dataset from the historical corpus and train the mark-predictor (async).
```json
// request
{ "corpus_dir": "data/corpus", "model_name": "midterm-cse-2026" }
// 202 Accepted
{ "training_id": "t-1", "status": "TRAINING" }
```

### `GET /api/v1/train/metrics`
```json
{
  "model_name": "midterm-cse-2026",
  "rmse": 0.71, "mae": 0.52, "r2": 0.88,
  "accuracy_within_1_mark": 0.93,
  "feature_importance": { "similarity": 0.41, "concept_coverage": 0.33, "keyword_recall": 0.14, "length_ratio": 0.12 }
}
```

---

## 2. Ingestion (Phase 2 input)

### `POST /api/v1/batch/upload` — `multipart/form-data`
`files` (scanned PDFs/images) + `answer_key` (question paper + model answers + rubric).
```json
// 202 Accepted
{ "batch_id": "b-18f7", "status": "QUEUED", "script_count": 35 }
```

---

## 3. Evaluation (Phase 2)

### `POST /api/v1/evaluate`
```json
// request
{ "batch_id": "b-18f7", "answer_key_id": "k-22", "model_id": "m-1" }
// 202 Accepted
{ "batch_id": "b-18f7", "status": "EVALUATING" }
```

### `GET /api/v1/evaluate/status?batch_id=b-18f7`
```json
{ "batch_id": "b-18f7", "status": "EVALUATED", "scripts_done": 35, "scripts_total": 35 }
```

---

## 4. Results

### `GET /api/v1/results/{batch_id}` — list evaluated scripts
```json
{
  "batch_id": "b-18f7",
  "scripts": [
    { "script_id": "s-22a", "roll_no": "26SN101024", "total_marks": 68, "max_total": 80, "percentage": 85.0, "low_confidence_count": 0 }
  ]
}
```

### `GET /api/v1/results/{script_id}/answers` — the evaluated sheet
```json
{
  "script_id": "s-22a",
  "total_marks": 68, "max_total": 80, "percentage": 85.0,
  "answers": [
    {
      "question_no": "Q2",
      "answer_text": "The process is exothermic because heat is released...",
      "similarity": 0.86,
      "predicted_mark": 6.5, "max_marks": 8, "percent_match": 0.82,
      "feedback": "Covers the exothermic definition and heat release; misses activation energy.",
      "deduction_reasons": ["missing: activation energy"],
      "low_confidence": false
    }
  ]
}
```

> **No override-the-mark endpoint by design in the MVP** — the mark is the trained model's output.
> Low-confidence answers are flagged (`low_confidence: true`) for a human to verify before publishing.

---

## 5. Standard Errors

```json
{ "error_code": "ERR_MODEL_NOT_TRAINED", "message": "No trained mark-predictor found. Run Phase 1 or use the similarity baseline." }
{ "error_code": "ERR_BATCH_NOT_FOUND",   "message": "The requested batch does not exist." }
{ "error_code": "ERR_OCR_FAILED",        "message": "Handwriting OCR failed on one or more pages." }
```

---

## 6. Related Documents

*   [Architecture](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ARCHITECTURE.md)
*   [Data Flow](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_FLOW.md)
*   [Database Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
