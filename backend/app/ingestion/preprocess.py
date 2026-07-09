# 1. FILE PURPOSE: Applies the vision pipeline spine: OpenCV deskew (Hough/minAreaRect), denoise, and adaptive-threshold binarization to prepare images for OCR.
# 2. RESPONSIBILITIES:
#    - Correct image skew.
#    - Reduce noise.
#    - Apply adaptive binarization for clear OCR.
# 3. PLANNED CONTENTS: Preprocess function suite. Takes raw image, returns cleaned image.
# 4. INPUTS / OUTPUTS: Inputs: raw raster images. Outputs: deskewed, binarized images.
# 5. DEPENDS ON / USED BY: OpenCV (opencv-python).
