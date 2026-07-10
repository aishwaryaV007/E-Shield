# Evaluation Module (Phase 2)

The automated grading brain. Takes segmented (student answer, answer key, rubric) units
and produces a fully evaluated answer sheet. Replaces the old audit "engines"
(MarkSafe/CopyCatch/ScriptID/ReEval/RubricLens) — this system **assigns marks**.

Flow: `similarity` + `concept_coverage` → features → `scorer` (trained model) →
`feedback` → `report`.

- `similarity.py` — semantic similarity, student answer vs answer key.
- `concept_coverage.py` — which rubric points are covered / missing / contradicted.
- `scorer.py` — apply the trained mark-predictor → predicted marks (percentage-based).
- `feedback.py` — per-answer feedback + mark-deduction reasons.
- `report.py` — question-wise marks, total, percentage → the evaluated sheet.

**Compliance:** every mark is the output of the trained model in `scorer.py`; an LLM may
only phrase feedback text, never decide a mark (Track 02 rule).
