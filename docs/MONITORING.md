# Application Logging & Monitoring
> Run logs, execution tracking, and dashboard monitoring for training + evaluation.

*Design / Planned — Not yet implemented*

---

## 1. Runtime Monitoring

ExamShield logs training and evaluation events locally via Python's `logging`, so admins can track
pipeline status, spot bottlenecks (usually OCR), and debug failures.

```
[ Training / Evaluation pipeline ]
        │ (structured JSON messages)
[ Local log file: data/logs/run_logs.log ]
  • INFO:  stage completed
  • WARN:  answer flagged low-confidence OCR
  • ERROR: OCR / file / model-load failures
```

---

## 2. Structured Log Format

```json
{
  "timestamp": "2026-07-09T20:45:12.894Z",
  "level": "INFO",
  "module": "app.training.trainer",
  "message": "Mark-predictor trained. RMSE=0.71, ±1-mark accuracy=0.93."
}
{
  "timestamp": "2026-07-09T20:46:04.112Z",
  "level": "WARNING",
  "module": "app.ocr.confidence",
  "batch_id": "b-18f7",
  "script_id": "s-22a",
  "question_no": "Q4",
  "message": "Answer OCR confidence 0.41 < threshold — flagged low_confidence for human verification."
}
{
  "timestamp": "2026-07-09T20:47:01.340Z",
  "level": "ERROR",
  "module": "app.evaluation.scorer",
  "error_code": "ERR_MODEL_NOT_TRAINED",
  "message": "No trained mark-predictor found; falling back to similarity baseline."
}
```

---

## 3. Dashboard Monitoring Views

- **Training metrics:** RMSE / MAE / R² / ±1-mark accuracy + feature importance for the current model.
- **Evaluation progress:** scripts done / total for the active batch; average time per script.
- **OCR confidence:** average answer-level confidence; count of low-confidence answers to verify.
- **Score distribution:** histogram of predicted marks / percentages across the batch.

---

## 4. Related Documents

*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Storage module](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/storage/README.md)
*   [Disaster Recovery](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DISASTER_RECOVERY.md)
