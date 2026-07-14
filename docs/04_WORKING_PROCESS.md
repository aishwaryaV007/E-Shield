# 4. Working Process (End-to-End)

> How ExamShield goes from a scanned handwritten paper to a fully evaluated sheet, in two phases.
> **The mark is always produced by the trained XGBoost model — never an LLM.**

---

## Phase 1 — Training (one-time, offline)
```
Historical corrected scripts + teacher marks
+ question papers + answer keys + rubrics
        → Feature engineering (similarity, concept coverage, keyword recall, missing/extra points)
        → Train XGBoost mark-predictor
        → Evaluate (RMSE / MAE / R² / ±1-mark accuracy)
        → Save trained mark-predictor model
```

## Phase 2 — Evaluation (per new script)
```
Scanned handwritten answer PDF
        → Handwriting OCR (TrOCR)
        → Segment into questions + match to answer key
        → Semantic similarity + concept coverage
        → Trained model predicts marks   ⟵ (uses the saved model from Phase 1)
        → Feedback + mark-deduction reasons
        → Flag low-confidence answers for human review
        → Fully evaluated sheet: question-wise marks, total, percentage
```

> Low-confidence (unreadable) answers are **flagged for human verification — never guessed.**

---

## How a teacher uses it
1. Start the backend (`:8000`) and open the web dashboard (`:3000`) or the Expo mobile app.
2. Optionally upload a shared **answer key** and **question paper**.
3. Add students, upload each student's answer-script **PDF**, click **Grade** (or **Grade all**).
4. Review the evaluated sheet: MCQ + descriptive subtotals, total, percentage, per-question marks,
   extracted answer vs. correct answer, OCR confidence.
5. **Edit** any mis-read answer and **Re-grade** instantly (no OCR re-run). Export results as CSV.

---

## Data behind it
- 50 real Data-Science student answer PDFs + a teacher manual-marks CSV (MCQ letters + short-answer marks).
- **Mohler ASAG** dataset (2,442 graded answers) — the real training set for Model B.
- Prose-format test exams (question paper + answer key + synthetic handwritten PDF) for multiple subjects.

---
*See also: [01_ALREADY_IMPLEMENTED](01_ALREADY_IMPLEMENTED.md)*
