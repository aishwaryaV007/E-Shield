# Exam Integrity Verification
> Core value proposition, collusion network maps, sum check layers, and validation rules.

*Design / Planned — Not yet implemented*

---

## 1. Exam Integrity Protection Framework

ExamShield is designed to protect **Exam Integrity** in offline written examinations. It provides exam-cell staff with a multi-layered verification framework to detect errors and discrepancies before grades are published.

```
┌────────────────────────────────────────────────────────┐
│ Scanned Paper Batch                                    │
└───────────────────────┬────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
   [ Integrity 1 ][ Integrity 2 ][ Integrity 3 ]
   MarkSafe       CopyCatch      ScriptID
   Verify sums    Find collusion Roster validate
   & strikeouts   networks       & duplicates
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ Verified & Audited Grade Cards                         │
└────────────────────────────────────────────────────────┘
```

---

## 2. Integrity Verification Layers

### 1. Arithmetic Grade Auditing (MarkSafe)
Prevents totaled-marks disputes and grading transcription errors.
*   **Verification Rule:** The sum of question scores on a script must equal the written total.
*   **Safety Trigger:** If the OCR-extracted sum does not match the written total, the script is flagged as `SUM_MISMATCH` and queued for manual verification.
*   **Strikeout Handling:** Ambiguous marks and crossed-out numbers are flagged as `AMBIGUOUS_MARK`, requiring human intervention to prevent false corrections.

### 2. Collusion & Copying Detection (CopyCatch)
Maps student copying networks across handwritten scripts.
*   **Verification Rule:** Answer prose similarities must not exceed class-wide baselines.
*   **Safety Trigger:** If two scripts share similarity scores that deviate from the class average, the system creates a node connection in the collusion graph. Graders can review both scripts side-by-side to confirm copying.

### 3. Student Identity Validation (ScriptID)
Prevents student identity mix-ups and registry errors.
*   **Verification Rule:** Every roll number must match an active student registered in the enrollment CSV database.
*   **Safety Trigger:** The system flags duplicates, absent students with scripts, or unregistered IDs, prompting the user to check the original booklets.

---

## 3. Related Documents

*   [Anti-Cheating Mechanisms Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ANTI_CHEATING.md)
*   [Data Privacy & Local Constraints](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_PRIVACY.md)
*   [MarkSafe Technical Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/MARKSAFE.md)
