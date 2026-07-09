# User Roles & Access Controls
> Definitions, workspace profiles, and dashboard access boundaries for the three target user roles.

*Design / Planned — Not yet implemented*

---

## 1. User Roles Matrix

ExamShield defines three operational roles. Because the application runs locally, access control is managed via local login profiles or separate dashboard tabs:

```
                  ┌──────────────────────────────┐
                  │ Streamlit Dashboard Auth     │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
   [ Role 1: CoE ]        [ Role 2: Grader ]      [ Role 3: Auditor ]
   • View all tabs        • Calibration access    • Review MarkSafe
   • Resolve collusion    • Assistive rubrics     • Override sums
   • Finalize results     • No collusion access   • No collusion access
```

---

## 2. Roles Directory

### 1. Controller of Examinations (CoE)
*   **Definition:** The primary administrator legally accountable for final result accuracy and academic integrity.
*   **Dashboard Access:**
    *   Full access to all tabs.
    *   Exclusively authorized to view the CopyCatch collusion graph.
    *   Exclusively authorized to click the "Finalize Batch" button, which locks records in SQLite and exports grades to CSV.

### 2. Paper Grader / Evaluator
*   **Definition:** Subject matter experts responsible for grading scripts and entering marks.
*   **Dashboard Access:**
    *   Access to the visual calibration canvas tab to register answer layouts.
    *   Access to RubricLens highlights to assist with manual grading.
    *   No access to collusion graphs or student identity registers.

### 3. Exam-Cell Auditor
*   **Definition:** Administrative staff responsible for processing scripts and verifying score summation totals.
*   **Dashboard Access:**
    *   Access to Ingestion Logs to monitor batch uploads and page count errors.
    *   Access to the MarkSafe and ScriptID verification tabs to resolve duplicate IDs and score mismatch flags.
    *   No access to collusion graphs.

---

## 3. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Product FAQ Reference](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FAQ.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
