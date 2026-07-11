# Pipeline Development Plan
> Development steps, tasks, and configurations for the two-phase auto-grader (training + evaluation).

> Note: this replaces the earlier "five verification engines" plan. ExamShield now **assigns marks**
> via a trained model; the old audit engines (MarkSafe/CopyCatch/ScriptID/ReEval/RubricLens) are gone.

---

## 1. Development Focus

```
        ┌──────────────────────── PHASE 1: TRAINING ────────────────────────┐
        │ dataset_builder → features → trainer(XGBoost) → evaluate(metrics)  │
        │                              ↓                                     │
        │                     mark_predictor.pkl                            │
        └───────────────────────────────┬───────────────────────────────────┘
                                         │
        ┌──────────────────────── PHASE 2: EVALUATION ──────────────────────┐
        │ ingest → OCR → segment(question+key) → similarity+coverage →       │
        │ scorer(trained model → marks) → feedback → report(evaluated sheet) │
        └────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technical Task Breakdown

### Task 1 — Training dataset (`app/training/dataset_builder.py`)
- Read the historical corrected corpus; pair each answer with its key + teacher-awarded mark.
- Emit a tabular dataset (one row per answer) + train/val/test split.

### Task 2 — Feature engineering (`app/training/features.py`)
- Compute semantic similarity (MiniLM cosine), key-concept coverage, keyword recall,
  missing/extra points, length ratio, negation cues.
- Expose `FEATURE_NAMES`; the **same** function is used at inference (no train/serve skew).

### Task 3 — Train the mark-predictor (`app/training/trainer.py`)
- Fit an **XGBoost / RandomForest regressor** mapping features → mark.
- Hyperparameter tuning + feature importance (bonus scoring). Save to `models_cache/`.

### Task 4 — Evaluate (`app/training/evaluate.py`)
- Held-out RMSE, MAE, R², and accuracy within ±1 mark vs teacher marks; write a metrics report.

### Task 5 — Similarity + coverage (`app/evaluation/similarity.py`, `concept_coverage.py`)
- Embed answer vs key → similarity + aligned points; classify each rubric point
  covered/partial/missing/contradicted (optional NLI for negation).

### Task 6 — Scorer (`app/evaluation/scorer.py`)
- Build the feature vector, run the trained model, scale to `max_marks`, apply percentage bands,
  clamp to `[0, max]`. **The mark is the model's prediction — never an LLM's.**

### Task 7 — Feedback + report (`app/evaluation/feedback.py`, `report.py`)
- Feedback + deduction reasons from the coverage breakdown; assemble question-wise marks, total,
  percentage; flag low-confidence answers; persist.

---

## 3. Related Documents

*   [Training stage design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/TRAINING.md)
*   [Scorer stage design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)
*   [Evaluation module README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/evaluation/README.md)

## To-Do List

- [x] Build Ingestion & OCR Engines
- [x] Build Evaluation & Scoring Engine
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
