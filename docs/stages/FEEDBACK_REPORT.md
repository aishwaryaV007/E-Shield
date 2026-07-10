# Stage: Feedback & Report (Phase 2)

> Explains each mark and assembles the fully evaluated answer sheet — question-wise marks, total,
> percentage, per-answer feedback, and mark-deduction reasons.

*Design / Planned — Not yet implemented*

---

## 1. Objective

Make the auto-graded sheet self-explanatory, like one corrected by a human examiner.

## 2. Steps (`backend/app/evaluation/`)

### `feedback.py`
- Turn the concept-coverage breakdown into plain-language feedback: covered points (strengths),
  missing points (gaps), contradictions.
- State **why marks were deducted** (which rubric points were missing/wrong).
- An LLM may **only phrase** this feedback text — it never changes the mark.

### `report.py`
- Collect per-question marks (scorer) + feedback into one script report.
- Compute **total marks** and **overall percentage**.
- Mark low-confidence / unreadable answers for optional human verification before publishing.
- Persist the evaluation; the results API serves it to the dashboard.

## 3. Final output per script

Question-wise marks · total · percentage · per-answer feedback · deduction reasons ·
low-confidence flags — the fully evaluated answer sheet.
