# 1. FILE PURPOSE: Runs fuzzy PaddleOCR prose mode on answer regions, generating per-token confidence scores to drop low-confidence spans before CopyCatch embeddings.
# 2. RESPONSIBILITIES:
#    - Run prose OCR.
#    - Filter tokens below confidence threshold.
#    - Extract clean text for embeddings.
# 3. PLANNED CONTENTS: ProseOCR class. Takes answer region images, returns filtered text.
# 4. INPUTS / OUTPUTS: Inputs: answer region images. Outputs: high-confidence text blocks.
# 5. DEPENDS ON / USED BY: PaddleOCR.
