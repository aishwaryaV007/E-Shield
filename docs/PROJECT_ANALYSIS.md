# Project Value & Technical Analysis
> Problem-space analysis, productivity impact, and technical design justifications for the
> AI answer-sheet evaluator (Track 02).

---

## 1. Problem Space Analysis

Manual grading scales poorly and grades inconsistently:

| Failure Mode | Legacy Manual Workflow | ExamShield Auto-Evaluator |
| :--- | :--- | :--- |
| **Marking consistency** | Different evaluators award different marks for equivalent answers; fatigue drifts standards across a batch. | Every answer graded by the **same trained model** learned from real teacher marking — one consistent standard. |
| **Speed** | A batch takes an office days to evaluate. | Question-wise marks + feedback for a batch in minutes. |
| **Transparency** | A bare number with no explanation → revaluation disputes. | Each mark ships with feedback + explicit deduction reasons. |
| **Institutional memory** | Rubric knowledge lives in evaluators' heads. | The trained model captures marking behaviour and reuses it every exam. |

---

## 2. Productivity Impact

- **Consistency:** targets high agreement with teacher marks (e.g. ≥90% within ±1 mark on
  held-out data) — a measurable Track-02 metric.
- **Speed:** days → minutes per batch.
- **Transparency:** feedback + deduction reasons on every answer reduce revaluation demand.
- **Reusability:** train once on history, grade every subsequent exam the same way.

---

## 3. Technical Design Justifications

- **Trained XGBoost regressor vs LLM prompting:** Track 02 prohibits LLM-generated predictions.
  A regressor on engineered features (similarity, concept coverage, …) is explainable, CPU-fast,
  and reports real metrics (RMSE, MAE, R², ±1-accuracy) against teacher marks. This is the core
  innovation: *learning marking behaviour*, not scripting rules.
- **Semantic similarity (all-MiniLM-L6-v2) vs keyword matching:** correctly credits
  differently-worded correct answers; runs locally in seconds, keeps student data private.
- **NLI cross-encoder for concept coverage:** resolves negation ("is not correct" → contradiction)
  that keyword search misses.
- **Shared feature function (train == inference):** `training/features.py` produces the identical
  vector at training and scoring time, so there is no train/serve skew.

---

## 4. Honest Limitations

- Phase-1 training needs a **labeled** historical corpus (answers + teacher marks). Fallback:
  unsupervised similarity-to-key scoring, upgraded to the trained model when labels exist.
- The exam cell publishes results; low-confidence OCR answers are flagged for human verification.

---

## 5. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Local Performance & Scalability Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)

## To-Do List

- [x] Complete initial feasibility analysis
- [x] Review system requirements
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
