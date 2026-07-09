# Application Logging & Monitoring
> Run logs directory structure, execution tracking, exception levels, and dashboard monitoring charts.

*Design / Planned — Not yet implemented*

---

## 1. Application Runtime Monitoring

ExamShield records all ingestion and engine execution events locally using Python’s standard `logging` library. This allows administrators to track pipeline status, identify processing bottlenecks, and debug OCR errors.

```
┌────────────────────────────────────────────────────────┐
│ Ingestion & Processing Pipeline                        │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼ (Output structured messages)
┌────────────────────────────────────────────────────────┐
│ Local Log Files (/data/logs/run_logs.log)              │
├────────────────────────────────────────────────────────┤
│ • INFO: Ingestion steps completed                      │
│ • WARN: Sum verification mismatch flags raised         │
│ • ERROR: File read or OCR processing failures          │
└────────────────────────────────────────────────────────┘
```

---

## 2. Structured Log Formats

Log entries are saved in JSON format in the local file `/data/logs/run_logs.log`. This makes it easy to parse log events and display them in the dashboard:

```json
{
  "timestamp": "2026-07-09T20:45:12.894Z",
  "level": "INFO",
  "module": "app.ingestion.loader",
  "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
  "message": "Scanned scripts rasterization complete. Count: 35 booklets."
}
{
  "timestamp": "2026-07-09T20:46:04.112Z",
  "level": "WARNING",
  "module": "app.engines.marksafe",
  "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
  "script_id": "s22a8c9e",
  "flag_type": "SUM_MISMATCH",
  "message": "Arithmetic discrepancy detected: OCR sum 34, written total 24. Audit flag raised."
}
{
  "timestamp": "2026-07-09T20:47:01.340Z",
  "level": "ERROR",
  "module": "app.ocr.digit_ocr",
  "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
  "script_id": "s35f8d9a",
  "error_code": "ERR_OCR_INFERENCE_TIMEOUT",
  "message": "Local PaddleOCR digit recognition process timed out on page 2."
}
```

---

## 3. Dashboard Monitoring Views

The dashboard's Ingestion tab displays real-time processing statistics for active batches:
*   **Pipeline Progress Bar:** Shows the percentage of scripts processed in the current batch.
*   **Average Processing Speed:** Displays the average processing time per script (in seconds).
*   **OCR Confidence Metrics:** Shows average confidence scores for digit and prose extractions, helping administrators identify potential layout template alignment issues.
*   **Active Flag Counts:** Displays a breakdown of pending audit flags by type (`SUM_MISMATCH`, `DUPLICATE_ID`, `UNREGISTERED_ID`).

---

## 4. Related Documents

*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Disaster Recovery Procedures](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DISASTER_RECOVERY.md)
