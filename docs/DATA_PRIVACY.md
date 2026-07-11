# Data Privacy & Offline Processing
> Local data storage, privacy controls, offline sandboxing constraints, and local library guidelines.

---

## 1. Privacy Strategy

ExamShield handles sensitive student academic data, including names, roll numbers, grading rubrics, and scanned answer sheets. To comply with educational data regulations, the system is designed to run **completely offline**.

```
┌────────────────────────────────────────────────────────┐
│ Client Desktop PC (Offline Exam Cell)                  │
├────────────────────────────────────────────────────────┤
│  [ Scanned PNGs ] ──► [ Local OCR ] ──► [ Local SQLite]│
│                                                        │
│  No internet connectivity allowed                      │
│  No external cloud uploads                             │
└────────────────────────────────────────────────────────┘
```

---

## 2. Privacy Guidelines

### 1. No Third-Party Cloud API Uploads
The application is prohibited from using external cloud APIs (e.g., OpenAI, Gemini, Google Cloud Vision, AWS Textract) to process scanned scripts.
*   **Reasoning:** Uploading student answers to external servers violates student data privacy regulations.
*   **Technical Implementation:** All image pre-processing, digit/prose OCR, and vector embedding calculations are performed by local libraries (OpenCV, PaddleOCR, Sentence Transformers) running on the host machine.

### 2. Local-Only Storage
All data is stored locally on the host machine:
*   Scanned images and bounding box crops are stored in a designated local folder (`/data/corpus/`).
*   Extraction results, grades, and audit flags are stored in a local SQLite database file (`db.sqlite3`).
*   No external databases (e.g., cloud Postgres databases) are configured.

### 3. Cleaning Temp Files
Temporary image crops generated during page binarization are deleted immediately after the pipeline finishes processing. Only the calibrated marks crops and roll number boxes are retained to display visual evidence in the dashboard.

---

## 3. Related Documents

*   [Technology Stack Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TECH_STACK.md)
*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)

## To-Do List

- [ ] Add data anonymization for students
- [ ] Implement data retention and deletion policies
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
