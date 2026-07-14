# 5. Feature Enhancements

> Candidate improvements to raise accuracy, usability, and reach. Complements the
> production-hardening list in [what should be implemented](what%20should%20be%20implemented.md).

---

## Accuracy & reading
- **Handwriting accuracy** — fine-tune OCR on domain handwriting; better deskew/binarize for noisy scans.
- **Layout robustness** — support multi-column, diagram-heavy, and mixed MCQ + descriptive sheets.
- **Multi-language answers** — extend OCR + similarity to regional languages.

## Grading intelligence
- **Rubric-aware scoring** — let teachers define per-question rubrics that feed the feature set.
- **Model retraining loop** — feed teacher corrections back to continuously improve Model B.

## Usability
- **Confidence UX** — inline highlighting of low-confidence words for faster teacher correction.
- **Batch/queue mode** — grade an entire class folder in the background with progress tracking.
- **Role-based access** — admin / teacher / operator roles with audit logs.

## Insight & deployment
- **Analytics dashboard** — cohort averages, pass rates, per-question difficulty, examiner-consistency.
- **One-click deployment** — Docker image + desktop installer for non-technical staff.

---

## Honest limitations (context for enhancements)
- **MCQ OCR** fails on double-sided scans (bleed-through) → MCQ answers come from the digital record or a dropdown, not real OCR yet.
- **OCR accuracy** ~90% characters on real scans; ~98% on clean/synthetic PDFs.
- **Throughput** — single-process, CPU/MPS-bound (~4–5 scripts/min); no parallelism yet.

---
*See also: [what should be implemented](what%20should%20be%20implemented.md)*
