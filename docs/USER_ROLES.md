# User Roles & Access Controls
> Roles and dashboard access boundaries for the AI answer-sheet evaluator.

*Design / Planned — Not yet implemented*

---

## 1. Roles Matrix

The app runs locally; access is managed via local profiles / dashboard sections.

```
                  ┌──────────────────────────────┐
                  │ ExamShield Dashboard         │
                  └──────────────┬───────────────┘
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   [ Role 1: CoE ]        [ Role 2: Evaluator ]   [ Role 3: ML Admin ]
   • View all             • Review evaluated      • Train / retrain
   • Verify low-conf.       sheets + feedback       the mark-predictor
   • Publish results      • Confirm/adjust flags   • View metrics
```

---

## 2. Roles

### 1. Controller of Examinations (CoE)
- Accountable for result accuracy. Full access; verifies flagged low-confidence answers and
  **publishes** results (locks + exports the batch).

### 2. Paper Evaluator
- Reviews auto-graded sheets, feedback, and deduction reasons; confirms or adjusts flagged
  low-confidence answers before publication.

### 3. ML Admin
- Runs **Phase-1 training** on the historical corpus, monitors metrics (RMSE / MAE / R² /
  ±1-mark accuracy) and feature importance, and manages the trained-model registry.

> No role can override a mark by prompting an LLM; the mark always comes from the trained model.
> Human review is limited to verifying flagged low-confidence answers.

---

## 3. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [FAQ](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FAQ.md)
*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)

## To-Do List

- [ ] Define RBAC (Role-Based Access Control) models
- [ ] Implement Role-checking middleware
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
