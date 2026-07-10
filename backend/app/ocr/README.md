# OCR Module (Phase 2 input)

Extracts handwritten answer text from scanned scripts so the evaluation pipeline can
score it. Recognition is done by a **local OCR model** (TrOCR handwritten / PaddleOCR) —
never by prompting an LLM to "read the image".

- `handwriting_ocr.py` — recognise handwritten answer text + confidence.
- `confidence.py` — answer-level confidence; flags unreadable answers for human check.
