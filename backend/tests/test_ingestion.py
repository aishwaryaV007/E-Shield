# 1. FILE PURPOSE: Test suite for the ingestion pipeline in backend/app/ingestion/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/ingestion/pdf_loader.py — PDF to image rasterization.
#    - Test backend/app/ingestion/preprocess.py — deskew, denoise, binarize.
#    - Test backend/app/ingestion/blankcheck.py — page count and ink-presence detection.
# 3. PLANNED CONTENTS: One test function per ingestion module; uses sample image fixtures.
# 4. INPUTS / OUTPUTS: Inputs: Sample PDFs and images from data/raw. Outputs: pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/ingestion/* (resolved via pyproject.toml pythonpath).
