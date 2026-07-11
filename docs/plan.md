# ExamShield High-Level Build Plan
> Sequential milestones (M0–M6) from design to a working local auto-grader.

*Design / Planned — Not yet implemented*

---

## 1. Milestone Roadmap

```
 M0: Storage & schema ───────────────────────────┐
                                                 ▼
 M1: Phase-1 training (features → XGBoost → metrics)
                                                 │
                                                 ▼
 M2: Ingestion + OCR + segmentation ──► M3: Evaluation (similarity → scorer → feedback → report)
                                                 │
                                                 ▼
 M6: Demo & hardening ◄── M5: Stretch ◄── M4: Dashboard (training metrics + evaluated sheets)
```

---

## 2. Milestones

### M0 — Storage & schema (H0–H2)
- SQLite schema (models, answer_keys, questions, batches, scripts, pages, evaluations) + DB init.

### M1 — Phase-1 training (H2–H7)  ← proves the core idea
- `dataset_builder` (historical answers + teacher marks) → `features` (similarity, coverage, …) →
  `trainer` (XGBoost, tuned) → `evaluate` (RMSE / MAE / R² / ±1-mark accuracy). Save model artifact.
- Fallback: unsupervised similarity-to-key baseline if labels are unavailable.

### M2 — Ingestion + OCR + segmentation (H7–H14)
- PDF→image, deskew/binarize; handwriting OCR + confidence; split questions + match answer key.

### M3 — Evaluation (H14–H18)  ← end-to-end grading
- `similarity` + `concept_coverage` → `scorer` (trained model → marks, % bands) → `feedback` →
  `report` (question-wise marks, total, %).

### M4 — Dashboard (H18–H21)
- Training metrics view; evaluated-sheet view (marks + feedback + deduction reasons).

### M5 — Stretch (H19–H21, if stable)
- Concept-coverage NLI (negation-aware); feature-importance charts; CSV export.

### M6 — Validation & hardening (H21–H24)
- Run on the demo corpus + batch; verify predicted marks vs teacher marks; fallback demo video; freeze.

---

## 3. Related Documents

*   [Implementation Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/implementation_plan.md)
*   [Training stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/TRAINING.md)
*   [Scorer stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)

## To-Do List

- [x] Complete initial planning phase
- [x] Complete execution phase
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
