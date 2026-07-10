# 1. FILE PURPOSE: Test suite for OCR modules in backend/app/ocr/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/ocr/handwriting_ocr.py — handwritten answer-text recognition.
#    - Test backend/app/ocr/confidence.py — low-confidence answers flagged for human check.
# 3. PLANNED CONTENTS: One test function per OCR module; uses answer-region image fixtures.
# 4. INPUTS / OUTPUTS: Inputs: Image crop fixtures. Outputs: Extracted text + pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/ocr/* (resolved via pyproject.toml pythonpath).
