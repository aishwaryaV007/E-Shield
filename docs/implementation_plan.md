# ExamShield Detailed Implementation Plan
> Granular tasks, target files, and verification checks per milestone.

*Design / Planned — Not yet implemented*

---

## 1. M0 — Storage & Schema
- [ ] venv + install `requirements.txt` (includes `xgboost`, `joblib`, `sentence-transformers`).
- [ ] SQLite schema — *File:* `backend/app/storage/schema.sql` (models, answer_keys, questions, batches, scripts, pages, evaluations).
- [ ] DB init + CRUD helpers — *File:* `backend/app/storage/db.py`.
- **Verify:** DB creates on boot; tables exist.

## 2. M1 — Phase-1 Training  ← the core innovation
- [ ] Build labeled dataset from historical corpus — *File:* `backend/app/training/dataset_builder.py`.
- [ ] Feature engineering (similarity, concept coverage, keyword recall, length ratio, negation) — *File:* `backend/app/training/features.py`.
- [ ] Train + tune XGBoost mark-predictor, save artifact — *File:* `backend/app/training/trainer.py`.
- [ ] Evaluate: RMSE / MAE / R² / ±1-mark accuracy — *File:* `backend/app/training/evaluate.py`.
- **Verify:** metrics report written; predicted marks track teacher marks on a held-out split.

## 3. M2 — Ingestion + OCR + Segmentation
- [ ] PDF→image — *File:* `backend/app/ingestion/pdf_loader.py`.
- [ ] Deskew/denoise/binarize — *File:* `backend/app/ingestion/preprocess.py`.
- [ ] Handwriting OCR + confidence — *Files:* `backend/app/ocr/handwriting_ocr.py`, `confidence.py`.
- [ ] Question segmentation + answer-key matching — *Files:* `backend/app/segmentation/question_segmenter.py`, `answer_matcher.py`.
- **Verify:** a scanned script yields ordered (question, answer, key, max_marks) units; unreadable answers flagged.

## 4. M3 — Evaluation
- [ ] Semantic similarity + aligned points — *File:* `backend/app/evaluation/similarity.py`.
- [ ] Concept coverage (optional NLI) — *File:* `backend/app/evaluation/concept_coverage.py`.
- [ ] Scorer: features → trained model → marks (% bands, clamp) — *File:* `backend/app/evaluation/scorer.py`.
- [ ] Feedback + deduction reasons — *File:* `backend/app/evaluation/feedback.py`.
- [ ] Report: question-wise marks, total, % — *File:* `backend/app/evaluation/report.py`.
- **Verify:** the mark comes from the trained model; totals/percentages correct; feedback references missing points.

## 5. M4 — API + Dashboard
- [ ] Routes: training, evaluation, results, ingestion — *Files:* `backend/app/api/routes/*`.
- [ ] Frontend: Training metrics, Ingestion/upload, Results (evaluated sheets) — *Files:* `frontend/src/app/*`.
- **Verify:** train → metrics; upload → evaluate → evaluated sheet renders.

## 6. M5 — Stretch
- [ ] NLI negation-aware coverage; feature-importance chart; CSV export.

## 7. M6 — Validation & Hardening
- [ ] Run on demo corpus + batch; verify predicted vs teacher marks; fallback video; freeze.

---

## 8. Related Documents

*   [Build Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/plan.md)
*   [Database Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [API Contract](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)

## To-Do List

- [x] Execute database implementation plan
- [x] Draft evaluation engine implementation plan
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
