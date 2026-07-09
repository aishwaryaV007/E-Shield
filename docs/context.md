# ExamShield Context & Scope
> Comprehensive overview of the problem, product goals, project boundaries, glossary, and current development status.

*Design / Planned — Not yet implemented*

---

## 1. Problem Statement

Universities and secondary education boards evaluate lakhs of physical, handwritten answer scripts each semester. This operation is managed by the **Controller of Examinations (CoE)** and executed by human evaluators working under high workload pressure. 

Currently, the process faces three critical, expensive points of failure:
1. **Collusion & Copying:** Students sitting near each other can easily copy answers. An evaluator grading hundreds of scripts sequentially cannot remember if script #200 copied answers from script #12. Pairwise comparison of $N=300$ scripts requires $\frac{N(N-1)}{2} = 44,850$ checks, which is humanly impossible. Plagiarism goes virtually undetected.
2. **Totaling and Transcription Errors:** Fatigue leads to graders miscalculating marks, missing ungraded pages, or transcribing physical marks lists incorrectly to the digital register. This results in costly disputes, withdrawn results, and revaluation backlogs.
3. **Identity & Roster Mismatches:** Miswritten, misread, or duplicate roll numbers result in grading errors where a student receives another student's marks. Lost paper sheets and border grade disputes (e.g., scoring 39 when 40 is a pass) cause administrative friction.

Existing mitigation steps are entirely retroactive: moderation committees, second evaluations, and student-funded revaluations, which occur *after* grade cards are published.

---

## 2. Product Goals

*   **Catch Mismatches Pre-Publication:** Identify student copying networks and grading inaccuracies *before* grades are finalized and released.
*   **100% Copying Coverage:** Perform automated semantic comparison on all answer scripts in a batch, transforming an unvetted batch into an audited cohort.
*   **Zero-Guess Sum Verification:** Flag every mismatch between calculated page sums and written overall totals without automatic guessing.
*   **Evaluate Autonomy preservation:** Provide evaluators and exam-cell staff with side-by-side visual crops of questionable answer regions rather than automated machine grading.
*   **Local & Secure Execution:** Protect student identity and grade records by avoiding cloud network uploads. The tool must operate offline on standard university computers.

---

## 3. Scope & Boundaries

### In Scope
*   Batch scanning/loading of handwritten paper answer scripts (PDFs/Images).
*   One-time calibration interface to create coordinates-based template profiles for varying answer sheet layouts.
*   Dual-tier local OCR: strict digit extraction for marks columns/totals, and fuzzy prose OCR for handwritten answers.
*   The five core inspection engines:
    1.  **MarkSafe:** Total validation and empty-box warning.
    2.  **CopyCatch:** Semantic pairwise distance ranking and NetworkX collusion graphs.
    3.  **ScriptID:** Roster crosscheck to verify enrollment matching.
    4.  **ReEval Guard:** High-priority queues for borderline grades (e.g., marks near pass/fail boundaries).
    5.  **RubricLens:** Assistive color-coded rubric matching for human review.
*   A unified Streamlit dashboard for audit logs, side-by-side handwriting comparison, and manual flag resolution.

### Out of Scope (Non-Goals)
*   **Automatic Grading:** The system will never assign scores or override grader marks. It strictly highlights regions and flags discrepancies for human decision-making.
*   **Automated Accusations:** CopyCatch does not convict a student of cheating. It marks two papers as possessing "anomalous similarity." The actual cheat review requires human inspection.
*   **Cloud Processing/SaaS API Integration:** Uploading answer sheets to public LLMs (e.g., GPT-4, Claude) is strictly prohibited due to privacy rules and venue internet constraints.
*   **Live Online Proctoring:** No webcam feeds, browser lockdowns, desktop tracking, or student-side digital portals are included in the MVP scope.

---

## 4. Project Glossary

| Term | Definition |
| :--- | :--- |
| **Answer Script** | The physical, handwritten paper booklet containing a student's responses to an exam. |
| **Controller of Examinations (CoE)** | The administrative officer responsible for organizing exams, managing evaluators, and publishing final grades. |
| **Zone Calibration** | Defining bounding box coordinates (marks column, roll number, text bodies) on a template answer sheet page. |
| **Digit OCR** | Strict digit recognition applied to mark-entry columns, optimizing accuracy over text variation. |
| **Prose OCR** | Multi-sentence handwritten text extraction, capturing semantic concepts to calculate cosine similarity. |
| **Collusion Network** | An interactive node graph linking students whose papers exceed the class-baseline similarity threshold. |
| **Borderline Script** | A paper whose total score is just 1 or 2 points below a passing score or grade-boundary cutoff. |
| **NLI (Natural Language Inference)** | A NLP task checking if a premise (student answer) logically entails, contradicts, or is neutral to a hypothesis (rubric). |

---

## 5. Current Development Status

*   **Workspace Status:** Initial planning, architecture, and technology assessment complete.
*   **Codebase:** `0%` implementation. Design blueprints and module boundaries are set.
*   **Datasets:** Simulated 35-script corpus and classroom register CSV are prepared for integration testing.

---

## 6. Related Documents

*   [Root README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Build Milestones Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/plan.md)
*   [System Architecture Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ARCHITECTURE.md)
