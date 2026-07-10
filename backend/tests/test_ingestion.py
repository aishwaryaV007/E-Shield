# 1. FILE PURPOSE: Test suite for the ingestion + segmentation stages in backend/app/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/ingestion/pdf_loader.py — PDF to image rasterization.
#    - Test backend/app/ingestion/preprocess.py — deskew, denoise, binarize.
#    - Test backend/app/segmentation/question_segmenter.py — split a script into per-question blocks.
#    - Test backend/app/segmentation/answer_matcher.py — align answers with the correct question/key.
# 3. PLANNED CONTENTS: One test function per module; uses sample image + answer-key fixtures.
# 4. INPUTS / OUTPUTS: Inputs: Sample PDFs/images from data/raw. Outputs: pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/ingestion/* + app/segmentation/* (via pyproject.toml pythonpath).
