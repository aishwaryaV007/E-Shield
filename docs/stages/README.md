# Pipeline Stage Designs

Detailed design per stage of the two-phase auto-grader. Replaces the old per-engine docs
(MarkSafe / CopyCatch / ScriptID / ReEval Guard / RubricLens), which belonged to the earlier
"never-grades audit tool" concept.

- [`TRAINING.md`](TRAINING.md) — **Phase 1**: learn marking behaviour → trained mark-predictor.
- [`SIMILARITY.md`](SIMILARITY.md) — **Phase 2**: semantic similarity + concept coverage.
- [`SCORER.md`](SCORER.md) — **Phase 2**: trained model assigns percentage-based marks.
- [`FEEDBACK_REPORT.md`](FEEDBACK_REPORT.md) — **Phase 2**: feedback, deductions, evaluated sheet.
