# ExamShield Testing Specification
> Test architecture for the training + evaluation pipelines.

*Design / Planned — Not yet implemented*

---

## 1. Test Architecture

`pytest` on the backend; type-check on the frontend.

```
┌────────────────────────────────────────────────────────────┐
│ PyTest Test Runner                                         │
└──────────────────────┬─────────────────────────────────────┘
         ┌─────────────┼──────────────┬────────────────┐
         ▼             ▼              ▼                ▼
   [ Unit ]      [ Training ]    [ Evaluation ]   [ End-to-end ]
   preprocess    features +      similarity +     script → sheet
   OCR conf.     trainer +       scorer +         on demo corpus
                 metrics         feedback
```

---

## 2. Test Suites

### Unit (`backend/tests/`)
- `test_ingestion.py` — PDF→image, deskew/binarize, question segmentation + answer matching.
- `test_ocr.py` — handwriting OCR + low-confidence flagging.
- `test_storage.py` — SQLite schema + evaluation persistence; JSON round-trips.

### Training & evaluation (`backend/tests/test_evaluation.py`)
- **Feature parity:** `features.py` returns the same vector at train and inference time.
- **Trainer/metrics:** model trains and reports RMSE / MAE / R² / ±1-mark accuracy on a held-out split.
- **Scorer:** the mark comes from the trained model and is clamped to `[0, max]`.
- **Feedback:** deduction reasons reference the missing rubric points.

### End-to-end (demo runner)
Run Phase 1 on the demo corpus, then Phase 2 on the demo batch; assert:
```python
def verify_demo(batch_id, model_metrics):
    assert model_metrics["accuracy_within_1_mark"] >= 0.85   # model tracks teacher marks
    sheets = get_results(batch_id)
    assert all(0 <= a["predicted_mark"] <= a["max_marks"] for s in sheets for a in s["answers"])
    assert all(s["total_marks"] == sum(a["predicted_mark"] for a in s["answers"]) for s in sheets)
    print("Demo verified: model trained + scripts fully evaluated.")
```

---

## 3. Related Documents

*   [Implementation Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/implementation_plan.md)
*   [Storage module](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/storage/README.md)
*   [Scorer stage](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/stages/SCORER.md)

## To-Do List

- [x] Write ingestion and storage unit tests
- [ ] Write end-to-end integration tests
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
