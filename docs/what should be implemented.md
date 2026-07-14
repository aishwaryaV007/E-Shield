# 2. What Should Be Implemented

> Production-hardening and reach items. None are demo blockers — the system already grades
> exams end-to-end. See [what is already implemented](what%20is%20already%20implemented.md).

---

## Performance & scale
- **Throughput / parallelism** — currently single-process (~4–5 scripts/min). Add batching or a worker queue.
- **Prediction caching** — skip re-OCR/re-scoring for identical scripts.

## Accuracy
- **Real MCQ OCR** — MCQ answers currently fall back to the digital record because scan bleed-through defeats OCR; improve preprocessing for double-sided scans.
- **More exam formats** — tune segmentation for varied layouts; assign marks to synthetic booklets so they become trainable.
- **Better Model B accuracy** — larger/cleaner training data; the current R² is modest.

## Operations & security
- **Monitoring & alerting** — metrics dashboards on top of the existing logging.
- **Backups / disaster recovery** runbook.
- **RBAC** — admin / teacher / operator roles with audit logs.
- **Role-based dashboards**.

## Deployment
- **Cloud/on-prem packaging** (Docker image).
- **Installer** for non-technical staff.

## Analytics
- Class/cohort trends, question-difficulty analysis, examiner-consistency reports.

---
*See also: [feature enhancements](feature%20enhancements.md)*
