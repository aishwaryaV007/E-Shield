# Frontend Dashboard

Next.js dashboard for the ExamShield AI answer-sheet evaluator (Track 02).

*Design / Planned — Not yet implemented*

---

## Pages

1. **Overview** (`app/page.tsx`) — batches, whether a model is trained, scripts evaluated, average score.
2. **Training** (`app/training/page.tsx`) — **Phase 1**: upload the historical corrected corpus, train the
   mark-predictor, and view metrics (RMSE / MAE / R² / ±1-mark accuracy) + feature importance.
3. **Ingestion** (`app/ingestion/page.tsx`) — **Phase 2 input**: upload scanned scripts + the question paper /
   answer key / rubric, then start the auto-grading run.
4. **Results** (`app/results/page.tsx`) — list of auto-graded scripts with totals and percentages.
5. **Evaluated sheet** (`app/scripts/[id]/page.tsx`) — the fully graded answer sheet: question-wise marks,
   feedback, deduction reasons, and a student-answer-vs-key comparison per question.

## Key components

- `components/results/ScoreSummary.tsx` — total marks, percentage, low-confidence flags.
- `components/results/AnswerList.tsx` + `AnswerCard.tsx` — question-wise auto-graded answers.
- `components/results/AnswerCompare.tsx` — student answer vs answer key, covered/missing key-points.

## Data flow

`lib/api/*` (axios) → `hooks/*` (TanStack Query) → pages/components. Charts via `recharts`.

**Note:** the frontend only *displays* marks; every mark is computed by the trained model on the
backend (`app/evaluation/scorer.py`) — never by an LLM.
