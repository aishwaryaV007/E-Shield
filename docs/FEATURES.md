# Product Features Specifications
> Detailed user-facing feature list, execution triggers, data inputs, and audit outputs.

*Design / Planned — Not yet implemented*

---

## 1. Feature Architecture

ExamShield provides six primary evaluation and auditing features. These features are powered by a unified image processing and local OCR pipeline, and are accessed via the Streamlit dashboard:

```
┌────────────────────────────────────────────────────────┐
│ ExamShield Core Dashboard                              │
├─────────────┬─────────────┬─────────────┬──────────────┤
│ MarkSafe    │ CopyCatch   │ ScriptID    │ ReEval Guard │
│ Sum checks  │ Collusion   │ Identity    │ Borderline   │
│             │ network     │ check       │ queue        │
└─────────────┴─────────────┴─────────────┴──────────────┘
```

---

## 2. Core Features Directory

### 1. MarkSafe (Sum Auditing)
*   **What it does:** Verifies page-wise question marks and validates the sum against the written total.
*   **Who uses it:** Graders and Exam-Cell Auditors.
*   **Data Inputs:** Digit crops from the marks table and overall total boxes.
*   **Outputs & Flags:** `SUM_MISMATCH` flag (when page sum does not equal written total), `AMBIGUOUS_MARK` flag (when OCR confidence is low).

### 2. CopyCatch (Collusion Detection)
*   **What it does:** Compares student answer prose to map similarity networks.
*   **Who uses it:** Controllers of Examinations (CoE).
*   **Data Inputs:** Answer prose text extracted via Tier-2 OCR.
*   **Outputs & Flags:** `SIMILARITY_CLUSTER` (raised when student similarity z-scores exceed the class-wide baseline), interactive HTML community graphs.

### 3. ScriptID (Identity Check)
*   **What it does:** Verifies handwritten student roll numbers against the roster database.
*   **Who uses it:** Exam-Cell Staff.
*   **Data Inputs:** Hand-written roll number crop, student roster CSV.
*   **Outputs & Flags:** `UNREGISTERED_ID`, `DUPLICATE_ID`, `ABSENTEE_WITH_SCRIPT` alerts.

### 4. ReEval Guard (Borderline Queue)
*   **What it does:** Automatically routes borderline scores (e.g., scoring 39 when 40 is a pass) to a priority audit queue.
*   **Who uses it:** Exam-Cell Auditors.
*   **Data Inputs:** Graded totals from MarkSafe, grade boundary configurations.
*   **Outputs & Flags:** `BORDERLINE_PASS_FAIL` priority review markers.

### 5. BlankCheck (Page Triage)
*   **What it does:** Performs a fast pixel-density scan to check for blank pages.
*   **Who uses it:** Ingestion Operators.
*   **Data Inputs:** High-contrast binary page image matrices.
*   **Outputs & Flags:** Page count audits, `PAGE_BLANK` log lists.

### 6. RubricLens (Grading Assistant)
*   **What it does:** Uses local NLI models to highlight answer text segments that align with or contradict rubric guidelines.
*   **Who uses it:** Graders.
*   **Data Inputs:** Answer prose text, grading rubric text files.
*   **Outputs & Flags:** Color-coded text overlays (green for entailment, red for contradiction).

---

## 3. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Product Roadmap](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ROADMAP.md)
*   [CopyCatch Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
