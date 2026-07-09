# Product FAQ Reference
> Answers to common questions regarding local processing, OCR limits, and manual auditing controls.

*Design / Planned — Not yet implemented*

---

## 1. General Questions

### Q: Why does ExamShield run locally rather than as a cloud service?
A: ExamShield processes sensitive student information (scanned answer scripts and roster grades). Running the application locally ensures student data privacy and allows it to operate without internet dependencies during examinations.

### Q: Does ExamShield grade answer sheets automatically?
A: No. ExamShield is an **assistive auditing tool**. It flags mathematical total errors, highlights rubric alignments, and maps collusion networks, but leaves all final grading and disciplinary decisions to human graders.

---

## 2. Technical & OCR Questions

### Q: How does the system handle bad handwriting or crossed-out scores?
A: The system uses a safe fallback model:
*   If digit recognition confidence falls below **`0.85`** (which is common for messy writing or crossed-out numbers), the system flags the field as `AMBIGUOUS_MARK` and write `NULL` to the database.
*   The dashboard presents the grader with the original image crop, allowing them to manually enter the correct score.

### Q: How does CopyCatch prevent false collusion flags on standard definitions?
A: The engine uses **Class-Baseline Anomaly Normalizing**. Instead of flagging raw similarity scores, it calculates similarity z-scores against the class average. Common definitions or standard formulas copied by the entire class will have a low z-score and will not be flagged.

---

## 3. Deployment & Scaling Questions

### Q: What hardware is required to run the pipeline?
A: The pipeline is optimized to run on standard university computers. A 4-core CPU with 8 GB of RAM can process a batch of 35 scripts (with 5 pages each) in under 3 minutes.

### Q: How does the SQLite database handle concurrent requests from the dashboard and processing thread?
A: The database is configured with **Write-Ahead Logging (WAL)**. This allows background ingestion threads to write data while users read metrics in the dashboard, preventing database locks.

---

## 4. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [User Roles and Access Control](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/USER_ROLES.md)
*   [Performance & Scalability Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
