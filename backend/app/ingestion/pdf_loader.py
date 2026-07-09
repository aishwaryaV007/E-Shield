# 1. FILE PURPOSE: Rasterizes incoming PDF answer scripts to PNG format at ~300 DPI for downstream processing using pypdfium2.
# 2. RESPONSIBILITIES:
#    - Load PDF bytes.
#    - Render pages to high-res images.
#    - Handle multi-page scripts.
# 3. PLANNED CONTENTS: PDFLoader class. Takes raw bytes, yields list of numpy images.
# 4. INPUTS / OUTPUTS: Inputs: raw PDF files. Outputs: image arrays.
# 5. DEPENDS ON / USED BY: pypdfium2, NumPy.
