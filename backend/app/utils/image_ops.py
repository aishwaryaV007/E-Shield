# 1. FILE PURPOSE: Shared image helpers, especially evidence-crop extraction.
# 2. RESPONSIBILITIES:
#    - Crop a calibrated zone (rectangle) from a page image.
#    - Produce side-by-side evidence crops for the review dashboard.
# 3. PLANNED CONTENTS: crop_zone(image, bbox); make_evidence_crop(...); to_png_bytes(...).
# 4. INPUTS / OUTPUTS: Inputs: images + zone bboxes. Outputs: cropped regions / PNG bytes.
# 5. DEPENDS ON / USED BY: OpenCV, Pillow; used by engines (Tier-2 evidence) and the results API.
