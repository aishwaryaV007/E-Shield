# Product Roadmap
> Release timeline for the AI answer-sheet evaluator (Track 02).

---

## 1. Release Timeline

```
[ v1.0 Core Auto-Grader ] ──► [ v2.0 Better Model & Feedback ] ──► [ v3.0 Institutional Scale ]
```

---

## 2. Release Phases

### Phase 1: Core Auto-Grader (v1.0)
- **Objectives:** Train on historical marks and auto-grade new scripts end-to-end.
- **Key features:**
  - **Phase-1 training:** dataset builder + engineered features + XGBoost mark-predictor + metrics
    (RMSE / MAE / R² / ±1-mark accuracy).
  - **Phase-2 evaluation:** handwriting OCR → question segmentation → semantic similarity →
    trained-model scoring → feedback → evaluated sheet.
  - Dashboard: Training metrics + evaluated sheets.

### Phase 2: Better Model & Feedback (v2.0)
- **Objectives:** Improve accuracy and explanation quality.
- **Key features:**
  - Per-subject / per-question models; hyperparameter tuning + feature-importance dashboards.
  - Concept-coverage NLI for negation-aware feedback.
  - Confidence-calibrated flagging; batch CSV export of results.
  - Active learning: teachers correct a few predictions → the model retrains and improves.

### Phase 3: Institutional Scale (v3.0)
- **Objectives:** Multi-subject, multi-exam deployment.
- **Key features:**
  - Model registry across subjects/semesters; drift monitoring vs teacher marks over time.
  - Reviewer workflow for low-confidence answers before publication.
  - Optional integration with the exam-cell result system.

---

## 3. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Future Implementation Tasks](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FUTURE_IMPLEMENTATION_TASKS.md)
*   [Features](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FEATURES.md)

## To-Do List

- [x] Define initial milestones
- [ ] Update roadmap based on current progress
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
