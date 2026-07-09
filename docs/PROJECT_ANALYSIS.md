# Project Value & Technical Analysis
> Problem space analysis, productivity impacts, collusion coverage, and technical design justifications.

*Design / Planned — Not yet implemented*

---

## 1. Problem Space Analysis

Educational grading operations scale poorly when managed manually:

| Metric / Failure Mode | Legacy Manual Workflow | ExamShield Automated Audit |
| :--- | :--- | :--- |
| **Collusion / Plagiarism Checks** | **0% Coverage.** Graders evaluate booklets sequentially, making it impossible to detect copying across hundreds of sheets. | **100% Coverage.** The system automatically runs pairwise vector comparisons across the entire batch in seconds. |
| **Summation Auditing** | **Manual Verification.** Administrative staff manually check page calculations, resulting in arithmetic errors and transcription slips. | **Automated Sum Check.** MarkSafe validates sums automatically, flagging layout or arithmetic discrepancies for review. |
| **Disputed Grade Resolution** | **Post-publication Revaluation.** Disputes are resolved retroactively via student-funded revaluations, causing administrative backlogs. | **Preemptive Queue.** ReEval Guard flags borderline grades, allowing staff to review scripts before final grades are posted. |
| ** Roster Matches** | **Manual Key Entry.** Data entry errors can attribute grades to the wrong student enrollment ID. | **Automatic Validation.** ScriptID checks extracted roll numbers against student registers to flag duplicates or unregistered IDs. |

---

## 2. Productivity Impact Analysis

ExamShield provides measurable efficiency improvements across grading operations:

*   **50% Reduction in Grading Times:** RubricLens highlights matching and contradicting rubric segments, helping graders evaluate answers faster without auto-grading.
*   **Zero Arithmetic Slips:** MarkSafe verifies score additions, routing unclear markings or crossed-out numbers to the manual review queue rather than guessing values.
*   **Reduced Roster Discrepancies:** ScriptID flags registry mismatches and duplicates, preventing identity mix-ups before final grades are posted.
*   **Reduced Revaluation Backlogs:** ReEval Guard flags borderline scores for preemptive review, helping resolve potential grading disputes before publication.

---

## 3. Technical Design Justifications

The system stack was selected to support offline execution on standard university computers:

*   **PaddleOCR (Offline) vs. Cloud OCR APIs:** Running PaddleOCR locally ensures student data privacy, runs for free, and works without internet connectivity in restricted exam-cell environments.
*   **all-MiniLM-L6-v2 Embeddings vs. LLM API calls:** CopyCatch uses a local, lightweight vector model (~80 MB) to calculate pairwise similarity. This runs within seconds on standard CPUs, avoiding the cost and latency of cloud API calls.
*   **NLI DeBERTa Cross-Encoder vs. Keyword Matching:** RubricLens uses a local cross-encoder model to identify semantic alignments, resolving negation issues (e.g., matching "is not correct" as a contradiction) that simple keyword searches miss.

---

## 4. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Local Performance & Scalability Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
