# ExamShield API Contracts
> REST API specification for the FastAPI backend, covering routes, payloads, responses, and error definitions.

*Design / Planned — Not yet implemented*

---

## 1. REST Endpoints Matrix

The FastAPI backend coordinator operates locally at `http://localhost:8000`. The Streamlit dashboard uses these endpoints to control batch ingestion, template calibration, results querying, and database overrides.

```
┌────────────────────────────────────────────────────────┐
│ Streamlit UI Dashboard                                 │
└──────┬───────────────────▲───────────────────┬─────────┘
       │ POST /upload      │ GET /results      │ POST /override
       ▼                   │                   ▼
┌──────────────────────────┴─────────────────────────────┐
│ FastAPI API Server (localhost:8000)                    │
└────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints

### 1. Ingestion: Upload Answer Script Batch
*   **Endpoint:** `/api/v1/batch/upload`
*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`
*   **Request Payload:**
    *   `files`: List of scanned PDF or image assets.
    *   `register_csv`: Roster CSV containing student names and enrollment IDs.
*   **Success Response (202 Accepted):**
    ```json
    {
      "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
      "status": "QUEUED",
      "script_count": 35,
      "message": "Batch uploaded and binarization pipeline started."
    }
    ```

### 2. Calibration: Save Bounding-Box Layout Template
*   **Endpoint:** `/api/v1/templates/create`
*   **Method:** `POST`
*   **Content-Type:** `application/json`
*   **Request Payload:**
    ```json
    {
      "template_name": "SNIST_CSE_Final_2026",
      "page_width": 2480,
      "page_height": 3508,
      "zones": {
        "roll_number": {"page": 1, "rect": [372, 175, 1240, 280]},
        "marks_table": {"page": 1, "rect": [1984, 350, 372, 2455]},
        "total_score_box": {"page": 1, "rect": [1984, 2981, 372, 350]},
        "answers": [
          {"question_id": "Q1", "page": 2, "rect": [248, 350, 1984, 1227]},
          {"question_id": "Q2", "page": 2, "rect": [248, 1754, 1984, 1403]}
        ]
      }
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
      "template_id": "t77b8c9e-1a1a-2b2b-3c3c-d9a695d7367e",
      "status": "SAVED",
      "message": "Calibration layout registered successfully."
    }
    ```

### 3. Verification: Fetch Batch Audit Results
*   **Endpoint:** `/api/v1/batch/{batch_id}/results`
*   **Method:** `GET`
*   **Success Response (200 OK):**
    ```json
    {
      "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
      "summary": {
        "total_scripts": 35,
        "processed_scripts": 35,
        "total_flags_raised": 4,
        "resolved_flags": 0
      },
      "flags": [
        {
          "flag_id": "f55c8c9e-9b9b-8a8a-7b7b-d9a695d7367e",
          "script_id": "s22a8c9e-3b3b-4c4c-5d5d-d9a695d7367e",
          "roll_number": "26SN101024",
          "engine": "MarkSafe",
          "flag_type": "SUM_MISMATCH",
          "ocr_calculated_sum": 34,
          "written_total_registered": 24,
          "crop_urls": {
            "marks_column": "/data/crops/s22a8c9e/marks_col.png",
            "total_box": "/data/crops/s22a8c9e/total_box.png"
          },
          "status": "PENDING"
        }
      ]
    }
    ```

### 4. Collusion: Get CopyCatch Similarity Network Graph
*   **Endpoint:** `/api/v1/batch/{batch_id}/collusion`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `threshold` (float, default: `0.78`): The minimum cosine similarity score required to link two script nodes.
*   **Success Response (200 OK):**
    ```json
    {
      "batch_id": "b18f7c9e-2d4d-4e92-a1f9-d9a695d7367e",
      "threshold_used": 0.78,
      "nodes": [
        {"id": "s1", "label": "Student 26SN101012", "group": 1},
        {"id": "s2", "label": "Student 26SN101029", "group": 1},
        {"id": "s3", "label": "Student 26SN101035", "group": 2}
      ],
      "edges": [
        {"from": "s1", "to": "s2", "value": 0.89, "title": "Similarity: 89% on Question 2"}
      ]
    }
    ```

### 5. Override: Grader Manual Marks Correction
*   **Endpoint:** `/api/v1/marks/override`
*   **Method:** `POST`
*   **Content-Type:** `application/json`
*   **Request Payload:**
    ```json
    {
      "flag_id": "f55c8c9e-9b9b-8a8a-7b7b-d9a695d7367e",
      "script_id": "s22a8c9e-3b3b-4c4c-5d5d-d9a695d7367e",
      "question_number": "TOTAL",
      "resolved_value": 34,
      "auditor_notes": "Corrected totaling mismatch. Evaluator arithmetic error confirmed."
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
      "flag_id": "f55c8c9e-9b9b-8a8a-7b7b-d9a695d7367e",
      "status": "RESOLVED",
      "updated_total": 34
    }
    ```

---

## 3. Standard Error Responses

ExamShield endpoints return standard HTTP error structures when processing fails:

*   **404 Not Found (Missing Batch or File):**
    ```json
    {
      "error_code": "ERR_BATCH_NOT_FOUND",
      "message": "The requested batch UUID does not exist in local storage."
    }
    ```
*   **422 Unprocessable Entity (Invalid Template Coordinates):**
    ```json
    {
      "error_code": "ERR_INVALID_CALIBRATION_COORDS",
      "message": "Coordinates must fall within the document's width and height bounds."
    }
    ```
*   **500 Internal Server Error (OCR Processing Timeout):**
    ```json
    {
      "error_code": "ERR_OCR_INFERENCE_FAILED",
      "message": "Local PaddleOCR process timed out during execution."
    }
    ```

---

## 4. Related Documents

*   [Overall Architecture Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ARCHITECTURE.md)
*   [Data Flow and State Transitions](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_FLOW.md)
*   [API Development Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/PIPELINE_PLAN.md)
