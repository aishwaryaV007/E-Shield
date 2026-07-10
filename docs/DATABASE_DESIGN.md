# ExamShield Database Design Spec
> SQLite schema, entity relationships, and indexing for the auto-grader.

*Design / Planned — Not yet implemented*

---

## 1. Database Paradigm

Local, serverless **SQLite** — portable, zero-install, fast on local storage. The authoritative
schema lives in [`backend/app/storage/schema.sql`](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/storage/schema.sql).

---

## 2. Entity-Relationship Schema

```mermaid
erDiagram
    MODELS ||--o{ BATCHES : grades-with
    ANSWER_KEYS ||--o{ QUESTIONS : defines
    ANSWER_KEYS ||--o{ BATCHES : graded-against
    BATCHES ||--o{ SCRIPTS : contains
    SCRIPTS ||--o{ PAGES : has
    SCRIPTS ||--o{ EVALUATIONS : produces
    QUESTIONS ||--o{ EVALUATIONS : scored-for

    MODELS {
        int id PK
        text name
        text artifact_path "models_cache/mark_predictor.pkl"
        text metrics_json "RMSE/MAE/R2/±1-acc"
    }
    ANSWER_KEYS { int id PK  text name }
    QUESTIONS {
        int id PK
        int answer_key_id FK
        text question_no
        text key_text "model answer"
        text rubric_json "key points"
        real max_marks
    }
    BATCHES {
        int id PK
        int answer_key_id FK
        int model_id FK
        text status "created/ingested/evaluated"
    }
    SCRIPTS {
        int id PK
        int batch_id FK
        text roll_no
        int page_count
        real total_marks
        real percentage
    }
    EVALUATIONS {
        int id PK
        int script_id FK
        int question_id FK
        text answer_text "OCR'd"
        real similarity
        real predicted_mark "trained model"
        real max_marks
        real percent_match
        text feedback
        text deduction_reasons
        int low_confidence "0/1"
    }
```

---

## 3. Key Tables

- **`models`** — registry of trained mark-predictors + their metrics (Phase 1 output).
- **`answer_keys` / `questions`** — the question paper, model answers, rubric points, and max marks.
- **`batches` / `scripts` / `pages`** — the uploaded scripts to grade.
- **`evaluations`** — the core auto-grader output: one row per (script, question) with the
  **predicted mark**, similarity, feedback, deduction reasons, and a low-confidence flag.

---

## 4. Indexes

```sql
CREATE INDEX IF NOT EXISTS idx_scripts_batch   ON scripts(batch_id);
CREATE INDEX IF NOT EXISTS idx_questions_key   ON questions(answer_key_id);
CREATE INDEX IF NOT EXISTS idx_evals_script    ON evaluations(script_id);
CREATE INDEX IF NOT EXISTS idx_evals_question  ON evaluations(question_id);
CREATE INDEX IF NOT EXISTS idx_pages_script    ON pages(script_id);
```

---

## 5. Related Documents

*   [DBMS Concepts](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DBMS_CONCEPTS.md)
*   [Storage module](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/storage/README.md)
*   [Data Flow](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_FLOW.md)
