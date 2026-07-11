# Product Features Specifications
> User-facing features of the AI answer-sheet evaluator (Track 02).

*Design / Planned — Not yet implemented*

---

## 1. Feature Architecture

```
┌────────────────────────────────────────────────────────────┐
│ ExamShield Dashboard                                       │
├───────────────┬───────────────┬────────────────────────────┤
│ Train Model   │ Auto-Evaluate │ Evaluated Sheets           │
│ (Phase 1)     │ (Phase 2)     │ (marks + feedback)         │
└───────────────┴───────────────┴────────────────────────────┘
```

---

## 2. Core Features

### 1. Model Training (Phase 1)
- **What it does:** Learns teacher marking behaviour from historical corrected scripts + marks.
- **Who uses it:** Exam-cell admins (once per exam/subject, reused after).
- **Inputs:** Historical answers + teacher marks, answer keys, rubrics.
- **Outputs:** A trained mark-predictor + metrics (RMSE / MAE / R² / ±1-mark accuracy) and feature importance.

### 2. Handwriting OCR + Segmentation
- **What it does:** Reads handwritten answers and splits each script into question-wise answers.
- **Inputs:** Scanned PDF/image scripts.
- **Outputs:** Per-question answer text (+ low-confidence flags), matched to the answer key.

### 3. Semantic Scoring (Auto-Evaluation)
- **What it does:** Measures semantic similarity to the answer key + concept coverage, then the
  **trained model** assigns percentage-based marks.
- **Inputs:** Grading units (answer, key, rubric, max marks).
- **Outputs:** Predicted mark per question. *(The mark comes from the model, never an LLM.)*

### 4. Feedback & Deduction Reasons
- **What it does:** Explains each mark — covered points, missing points, contradictions.
- **Outputs:** Per-answer feedback + explicit reasons marks were lost.

### 5. Evaluated Sheet
- **What it does:** Assembles question-wise marks, total, and percentage into one sheet.
- **Outputs:** A fully evaluated answer sheet resembling a human examiner's, with low-confidence
  answers flagged for verification.

### 6. Consistency Metrics
- **What it does:** Reports agreement with teacher marks (±1-mark accuracy) on held-out data —
  the Track-02 measurable-performance story.

---

## 3. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Roadmap](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ROADMAP.md)
*   [Scorer stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)

## To-Do List

- [x] Implement Core OCR and Storage features
- [x] Implement Frontend and Analytics features
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
