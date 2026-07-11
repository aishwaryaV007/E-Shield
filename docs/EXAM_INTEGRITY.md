# Grading Integrity & Fairness
> How ExamShield keeps automated grading fair, consistent, transparent, and compliant.

---

## 1. Integrity Framework

ExamShield auto-grades answer sheets. Its integrity guarantees are about **fair, consistent, and
explainable marks** — not policing students.

```
┌────────────────────────────────────────────────────────────┐
│ Student answer + answer key + rubric                       │
└──────────────────────┬─────────────────────────────────────┘
         ┌─────────────┼──────────────┬────────────────┐
         ▼             ▼              ▼                ▼
   [ Consistency ][ Transparency ][ Compliance ]  [ Verification ]
   same trained   feedback +      trained model,   low-confidence
   model for all  deduction       never an LLM      answers flagged
```

---

## 2. Integrity Layers

### 1. Consistency
- Every answer is scored by the **same trained mark-predictor**, so equivalent answers get
  equivalent marks regardless of when or by whom they were scanned.
- Measured by agreement with teacher marks: **accuracy within ±1 mark** on a held-out split.

### 2. Transparency
- Each mark ships with **feedback** and explicit **deduction reasons** (which rubric points were
  missing/wrong), so a student or moderator can see *why*.

### 3. Compliance (Track 02)
- The mark is always the **trained model's prediction** — prompting an LLM to grade is prohibited
  and never done. An LLM may only phrase feedback text.
- No train/serve skew: the identical feature function runs at training and inference.

### 4. Verification before publication
- Answers the OCR cannot read confidently are flagged **low-confidence** for human verification —
  never silently guessed. The exam cell reviews these before releasing results.

---

## 3. Related Documents

*   [Data Privacy](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_PRIVACY.md)
*   [Scorer stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)
*   [Problem Statement](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/PROBLEM_STATEMENT.md)

## To-Do List

- [ ] Implement anomaly detection in grading
- [ ] Add audit logging for score changes
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
