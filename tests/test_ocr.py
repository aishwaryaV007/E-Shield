# 1. FILE PURPOSE: Test suite for OCR modules in backend/app/ocr/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/ocr/digit_ocr.py — digit extraction from calibrated zones.
#    - Test backend/app/ocr/prose_ocr.py — prose extraction with confidence filtering.
#    - Test backend/app/ocr/ambiguity.py — low-confidence/strikeout fallback to AMBIGUOUS flag.
# 3. PLANNED CONTENTS: One test function per OCR module; uses image crops as fixtures.
# 4. INPUTS / OUTPUTS: Inputs: Image crop fixtures. Outputs: Extracted text strings + pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/ocr/* (resolved via pyproject.toml pythonpath).
