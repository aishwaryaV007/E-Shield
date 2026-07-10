# Ingestion & Segmentation Plan (Phase 2 input)
> Development steps for turning a scanned script into gradable (question, answer) units.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

```
[ Raw scans uploaded ]
        │  (Task 1: PDF → PNG rasterization)
[ Rasterized page images ]
        │  (Task 2: OpenCV deskew / denoise / binarize)
[ Clean binarized pages ]
        │  (Task 3: segment questions + match answer key)
[ Grading units: (student_answer, answer_key, rubric, max_marks) ]
```

---

## 2. Technical Task Breakdown

### Task 1: Document rasterization (`app/ingestion/pdf_loader.py`)
1. Read PDFs offline with `pypdfium2`; rasterize pages to PNG at **~300 DPI**.
2. Save to `data/raw/{batch_id}/{script_id}/page_{n}.png`.

### Task 2: Image preprocessing (`app/ingestion/preprocess.py`)
1. **Denoise:** bilateral filter (preserve handwriting edges).
2. **Deskew:** estimate skew (Hough / minAreaRect), rotate via affine transform.
3. **Binarize:** Gaussian adaptive thresholding for clean OCR input.

### Task 3: Question segmentation (`app/segmentation/question_segmenter.py` + `answer_matcher.py`)
1. Detect question numbers / answer boundaries from layout + OCR text.
2. Group multi-page answers for the same question.
3. Match each student answer to its question in the answer key; attach the model answer text,
   rubric points, and `max_marks` → produce the grading units the scorer consumes.

> This replaces the old zone-calibration approach — no per-institution rectangle drawing; questions
> and answers are detected from the page + OCR text.

---

## 3. Related Documents

*   [Ingestion module](file:///Users/gaurav/Desktop/MyProjects/E-Shield/backend/app/ingestion/README.md)
*   [OCR Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/OCR_PLAN.md)
*   [Scalability](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)

## To-Do List

- [x] Build PDF Rasterization pipeline
- [x] Build Image Preprocessing & Segmentation pipelines
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
