# Product FAQ Reference
> Common questions about the AI answer-sheet evaluator.

---

## 1. General

### Q: Does ExamShield grade answer sheets automatically?
A: **Yes.** ExamShield learns marking behaviour from previously corrected scripts and then assigns
question-wise marks, a total, a percentage, and feedback for new scripts. The exam cell reviews
low-confidence answers and publishes results.

### Q: Does it use ChatGPT / an LLM to grade?
A: **No.** Track 02 prohibits LLM-generated predictions. Marks come from a **trained regressor**
(XGBoost) fit on historical teacher marks. An LLM may only phrase feedback text — never decide a mark.

### Q: Why run locally rather than in the cloud?
A: Student scripts are sensitive. Everything runs on the host machine — no uploads, no third-party
APIs — so data stays private and the tool works offline.

---

## 2. Model & Accuracy

### Q: How is "accuracy" measured?
A: On a held-out split of the historical data we report **RMSE, MAE, R², and accuracy within ±1
mark** vs the teachers' marks. ±1-mark accuracy is the headline number.

### Q: What if we don't have historical teacher-marked data?
A: Phase 2 can run on an **unsupervised similarity-to-key baseline** (map similarity % → marks).
The trained model is the upgrade once labeled data exists.

### Q: How are differently-worded correct answers handled?
A: Scoring uses **semantic similarity** (sentence embeddings), not keyword matching, so a correct
answer phrased differently still scores well. Concept coverage checks rubric points, and negation
("is not exothermic") is detected so contradictions aren't counted as coverage.

---

## 3. Reliability

### Q: What happens with bad handwriting the OCR can't read?
A: The answer is marked **low-confidence** and flagged on the evaluated sheet for human
verification before publishing — it is never silently guessed.

### Q: What hardware is needed?
A: Runs on a standard CPU (4-core / 8 GB). MiniLM (~80 MB) and the XGBoost model are lightweight;
no GPU required.

---

## 4. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [User Roles](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/USER_ROLES.md)
*   [Scalability](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)

## To-Do List

- [ ] Review and update questions based on implementation progress
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
- [ ] Schedule a final review with project stakeholders.
