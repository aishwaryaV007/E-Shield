# Stage: Scoring — Automated Mark Assignment (Phase 2)

> Applies the trained mark-predictor to each answer's features and assigns percentage-based marks.
> **This is the only place a mark is decided, and it is decided by the trained model — never an LLM.**

*Design / Planned — Not yet implemented*

---

## 1. Objective

Convert the similarity + concept-coverage signals into a mark per question, scaled to that
question's maximum marks.

## 2. Steps (`backend/app/evaluation/scorer.py`)

1. Build the feature vector for the answer via `training/features.py` (same features as training).
2. Load the trained model (`models/mark_model.py`) and predict a mark.
3. Scale to the question's `max_marks`, apply percentage-based bands, and clamp to `[0, max]`.

## 3. Percentage-based bands (illustrative, 8-mark question)

| Match | Marks |
|-------|-------|
| 90–100% | 8 |
| 80–89% | 6–7 |
| 70–79% | 5–6 |
| 60–69% | 4–5 |
| 50–59% | 3–4 |
| < 50% | scaled down by quality/completeness |

## 4. Output

Per question: `{ predicted_mark, max_marks, percent_match, features, similarity }` → consumed by
the feedback + report stages.

## 5. Compliance

The mark is the trained model's prediction. An LLM is never asked to grade. Low-confidence OCR
answers are flagged (`low_confidence`) for optional human verification before publishing.
