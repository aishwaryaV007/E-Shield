# Future Implementation Backlog
> Task queue and upcoming optimizations for the auto-grader.

*Design / Planned — Not yet implemented*

---

## 1. Developer Guidelines

1. **Isolate in branches** (e.g., `backlog/csv-export`).
2. **Stay offline & CPU-only** — no cloud deps, no GPU requirement.
3. **Never let an LLM decide a mark** — the trained model in `evaluation/scorer.py` owns the mark;
   preserve low-confidence flagging (never auto-trust unreadable answers).
4. **Keep feature parity** — any change to `training/features.py` applies to both train and inference.

---

## 2. Backlog Queue

### Model & features
- [ ] Per-question / per-subject models instead of one global regressor.
- [ ] Add features: answer structure, numeric-answer exact match, ordered-steps coverage.
- [ ] Hyperparameter search + published feature-importance report.
- [ ] Active learning: teachers correct a few predictions → periodic retrain.

### OCR & segmentation
- [ ] Swap-in TrOCR handwritten for hard scripts; phone-camera-friendly preprocessing.
- [ ] Robust question detection for varied answer-sheet layouts (no per-institution templates).

### Feedback & explainability
- [ ] NLI-based, negation-aware concept coverage for sharper deduction reasons.
- [ ] Confidence calibration so ±1-mark reliability is shown per answer.

### UI & ops
- [ ] CSV/XLS export of evaluated sheets to the exam-cell result system.
- [ ] Model-registry + drift monitoring (predicted vs teacher marks over time).
- [ ] Reviewer queue for low-confidence answers before publication.

---

## 3. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Roadmap](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ROADMAP.md)
*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
