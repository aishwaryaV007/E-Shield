# OCR Subsystem Development Plan (Phase 2)
> Development steps for reading handwritten answers with confidence.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

The **OCR subsystem** converts clean answer-region images into text the evaluation pipeline can
score. Recognition uses a **local handwriting OCR model** — never an LLM "reading" the image.

```
[ Preprocessed answer-region image ]
        │  (handwriting OCR: TrOCR handwritten / PaddleOCR)
[ Recognised text + per-line/token confidence ]
        │  (confidence aggregation)
[ Answer text (+ LOW_CONFIDENCE flag if unreadable) ]
```

---

## 2. Technical Task Breakdown

### Task 1: Handwriting OCR (`app/ocr/handwriting_ocr.py`)
1. Initialise a local handwriting-capable OCR model (TrOCR handwritten, or PaddleOCR).
2. Recognise the student's answer text for each answer region.
3. Return recognised text plus per-line/token confidence scores.

### Task 2: Confidence handling (`app/ocr/confidence.py`)
1. Aggregate token confidences into an answer-level confidence score.
2. If below threshold, mark the answer `LOW_CONFIDENCE` — surfaced on the evaluated sheet for
   human verification, **never silently trusted or guessed**.
3. The mark is still produced by the trained model from whatever text was read; low confidence
   just flags it for a human check before publishing.

---

## 3. Notes

- Digit-only OCR of a marks grid is no longer needed — ExamShield *produces* the marks; it does not
  re-read a teacher's marks column.
- Keep OCR local for privacy (student scripts never leave the machine) and offline reliability.

---

## 4. Related Documents

*   [OCR module](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/ocr/README.md)
*   [Ingestion & Segmentation Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/PIPELINE_PLAN.md)
*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
