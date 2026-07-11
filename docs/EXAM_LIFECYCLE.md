# Exam Processing Lifecycle
> How a script moves from scan to evaluated sheet, plus the one-time training lifecycle.

*Design / Planned — Not yet implemented*

---

## 1. Training lifecycle (once per exam/subject, reused after)

```
[ Collect historical corrected scripts + teacher marks ] ──► [ Build labeled dataset ]
        │                                                             │
        ▼                                                             ▼
[ Trained mark-predictor + metrics ] ◄── [ Train + evaluate ] ◄── [ Engineer features ]
```

## 2. Per-batch evaluation lifecycle

```
[ Step 1: Scan scripts + attach answer key ] ──► [ Step 2: Preprocess (deskew/binarize) ]
                                                          │
                                                          ▼
[ Step 6: Publish results ] ◄── [ Step 5: Verify low-confidence ] ◄── [ Step 4: Score + feedback ]
                                                          ▲
                                                          │
                                          [ Step 3: OCR + segment (question+key) ]
```

---

## 3. Stages

### Step 1 — Scan & attach key
Scripts scanned to PDF/images; the question paper + answer key + rubric registered for the batch;
a batch row created in SQLite.

### Step 2 — Preprocess
OpenCV deskew/denoise/binarize; pages saved locally.

### Step 3 — OCR & segmentation
Handwriting OCR (+confidence) reads answers; the script is split into questions and each answer is
matched to its answer key + rubric + max marks.

### Step 4 — Scoring & feedback
Semantic similarity + concept coverage → feature vector → **trained model** predicts a mark
(percentage bands); feedback + deduction reasons generated. *(Mark from the model, not an LLM.)*

### Step 5 — Verification
Low-confidence OCR answers are flagged for human verification before publishing.

### Step 6 — Publish & archive
Evaluated sheets (question-wise marks, total, percentage, feedback) exported; batch marked
`evaluated`; results released by the exam cell.

---

## 4. Related Documents

*   [README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Architecture](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ARCHITECTURE.md)
*   [Data Flow](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATA_FLOW.md)

## To-Do List

- [x] Implement exam creation workflow
- [x] Implement end-to-end exam grading workflow
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
