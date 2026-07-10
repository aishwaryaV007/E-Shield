# dataset/ — ExamShield Training Data (Track 02: Predictive Analytics)

This folder holds the **structured dataset** used to train the mark-predictor in Phase 1.
Instead of hand-written marking rules, the model **learns from previously corrected answer
sheets** — so this is where the historical teacher-marked data lives.

> **Privacy:** real student scripts + teacher marks are **git-ignored** here (see `.gitignore`).
> Only the folder structure, this README, and a synthetic `sample/` are committed.

## Structure

```
dataset/
├── raw_scripts/     # historical corrected answer scripts (scanned PDF/images) — gitignored
├── answer_keys/     # question papers + model answer keys + rubrics (JSON/CSV)  — gitignored
├── training_csv/    # the built structured dataset used to train the model      — gitignored
└── sample/          # a small SYNTHETIC sample (committed) showing the schema
    └── training_sample.csv
```

## Training dataset schema (`training_csv/*.csv`)

One row per (student answer, question). The **label** is the teacher-awarded mark.

| Column | Type | Meaning |
|--------|------|---------|
| `script_id` | str | Which historical script the answer came from |
| `question_no` | str | Question number (e.g. Q2) |
| `student_answer` | text | OCR'd / transcribed student answer |
| `answer_key` | text | Official model answer for the question |
| `max_marks` | float | Maximum marks for the question |
| `similarity` | float | Semantic similarity (student answer vs key), 0–1 |
| `concept_coverage` | float | Fraction of rubric key-points covered, 0–1 |
| `keyword_recall` | float | Fraction of key terms present, 0–1 |
| `length_ratio` | float | len(answer) / len(key) |
| `negation_flag` | int | 1 if a contradiction/negation was detected, else 0 |
| `teacher_mark` | float | **LABEL** — the mark the teacher actually awarded |

The engineered feature columns are produced by `backend/app/training/features.py` — the **same**
function is reused at inference time (no train/serve skew). The trained model artifact is written
to `models_cache/mark_predictor.pkl`.

## How it is built

```bash
cd backend && source .venv/bin/activate
python ../scripts/seed_demo_data.py     # generates a demo corpus + answer key (for testing)
# then the Phase-1 training pipeline (dataset_builder → features → trainer → evaluate)
# reads dataset/raw_scripts + dataset/answer_keys and writes dataset/training_csv/*.csv
```

See [`docs/stages/TRAINING.md`](../docs/stages/TRAINING.md) for the full Phase-1 design.
