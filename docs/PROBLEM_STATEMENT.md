# ExamShield — Problem Statement & Solution

**Hackathon:** HACK-THE-MATRIX 2026 (TECHNIDHI) — SNIST, 9–11 July | 24 Hours
**Track:** 02 — Predictive Analytics (ML / DL)
**Team Repo:** E-Shield

---

## 1. Problem Statement

Every semester, universities manually evaluate lakhs of handwritten answer scripts. Manual
evaluation is **slow, inconsistent, and subjective**:

1. **Inconsistent marking.** Different evaluators (and the same evaluator when tired) award
   different marks for equivalent answers. Students pay revaluation fees to correct this.
2. **Scale.** An evaluator grading hundreds of scripts cannot apply the rubric uniformly from
   sheet #1 to sheet #300.
3. **No learning from the past.** Every year the same rubric knowledge lives only in evaluators'
   heads; there is no system that captures *how teachers actually grade* and reuses it.

### Phase-1 Validation Checkpoint (per hackathon rules)

| Checkpoint | Our Answer |
|------------|-----------|
| **TARGET_USER** | **Controllers of Examinations, exam-cell staff, and evaluators** — they own the batch of physical scripts and are accountable for result accuracy and consistency. |
| **PROBLEM_STATE** | Yes — measurably. Marking a large batch consistently is impossible by hand; ExamShield grades every answer against the same learned standard in minutes, with a measurable agreement (±1 mark) against teacher marks. |
| **AI_NECESSITY** | Yes. Reading handwriting needs OCR; judging differently-worded answers needs **semantic similarity**, not keyword matching; and reproducing teacher marking behaviour needs a **model trained on historical evaluations** — not hand-written rules. |

---

## 2. Proposed Solution

**ExamShield** — an AI system that **learns how teachers grade** from previously corrected answer
sheets, then **automatically evaluates** new scanned scripts: question-wise marks, total,
percentage, and per-answer feedback with mark-deduction reasons.

### Two phases

**Phase 1 — Model Training.** Train on historical evaluations: previously corrected scripts with
teacher-awarded marks, question papers, model answer keys, marking rubrics, and teacher feedback →
a **mark-predictor** model that captures how teachers allocate marks and deduct for gaps.

**Phase 2 — Automated Evaluation.** For each new scanned script:
OCR the handwriting → detect each question and answer → measure **semantic similarity** to the
answer key → apply the trained model → assign **percentage-based marks** → generate feedback and
deduction reasons → produce a fully evaluated answer sheet.

### Governing principle
> **The mark is produced by the trained model — never by prompting an LLM.** An LLM may only phrase
> feedback text. Answers the OCR cannot read confidently are flagged for human verification,
> never guessed.

### Percentage-based marking (illustrative, 8-mark question)

| Match | Marks | | Match | Marks |
|-------|-------|-|-------|-------|
| 90–100% | 8 | | 60–69% | 4–5 |
| 80–89% | 6–7 | | 50–59% | 3–4 |
| 70–79% | 5–6 | | < 50% | scaled by quality |

### Pipeline

```
Phase 1:  Historical corrected scripts + keys + rubrics + teacher marks
          → dataset_builder → features → trainer → evaluate (RMSE/MAE/R²/±1-acc) → mark-predictor

Phase 2:  Scanned scripts → preprocess → handwriting OCR → segment (question + key)
          → semantic similarity + concept coverage → trained model → marks
          → feedback + deduction reasons → evaluated sheet (question-wise marks, total, %)
```

---

## 3. Track 02 Compliance — Predictive Analytics (all requirements met)

| Track Requirement | How ExamShield satisfies it |
|-------------------|------------------------------|
| **Dataset** — structured data (CSV/SQL/time-series/sensor) | Structured training table: one row per (student answer, answer key, engineered features, **teacher-awarded mark** label), built from the historical corrected corpus. |
| **Training Engine** — custom model training (Random Forest, XGBoost, Neural Nets, LSTM) | A trained **XGBoost / RandomForest regressor** (the mark-predictor) fit on the historical data — not hand-written rules. |
| **Evaluation** — measurable performance (RMSE, R², Accuracy, F1) | On a held-out split we report **RMSE, MAE, R², and accuracy within ±1 mark** vs teacher marks. |
| **Output** — meaningful predictions | Predicted question-wise marks, totals, and percentages for new scripts. |
| **Bonus** — feature engineering + hyperparameter tuning | Engineered features (semantic similarity, concept coverage, keyword recall, length ratio, negation cues) + tuned regressor hyperparameters. |
| **Strictly Prohibited** — prompting GPT/LLMs to generate predictions | **Fully compliant:** the mark is always the trained model's output. No LLM is used to predict or assign marks (an LLM may only phrase feedback text). |

---

## 4. Quantified Impact

- **Consistency:** every answer graded against the *same* learned standard, targeting high
  agreement (≥90% within ±1 mark) with teacher marks on held-out data.
- **Speed:** a batch that takes an office days is graded in minutes.
- **Transparency:** every mark comes with feedback and explicit deduction reasons.
- **Reusability:** the trained model captures marking behaviour once and reuses it every exam.

---

## 5. Scope Honesty

- The final decision to publish stays with the exam cell; low-confidence OCR answers are flagged
  for human verification before results are released.
- Phase-1 training needs a labeled historical corpus (answers + teacher marks). If unavailable in
  time, Phase 2 runs on an **unsupervised similarity-to-key baseline**, with the trained model as
  the upgrade — disclosed honestly.
- No LLM decides a mark, anywhere.

---

## 6. Demo Plan

1. Show the **Training** dashboard: a model trained on the historical corpus, with RMSE/±1-accuracy
   vs teacher marks and feature importance.
2. Upload a fresh scanned script + answer key; run **Phase 2** live.
3. Open the **evaluated sheet**: question-wise marks, total, percentage, and per-answer feedback
   with deduction reasons.
4. Compare a few predicted marks against a teacher's marks to show agreement.
5. Honesty beat: an unreadable answer flagged *"low confidence — verify"*, never guessed.
