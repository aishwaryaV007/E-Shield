# 1. FILE PURPOSE: Verifies arithmetic. Digit-OCRs the marks grid, sums per-question marks, compares to the written total, flags mismatches and strikeouts as 'Ambiguous — Human Review'. Never auto-corrects.
# 2. RESPONSIBILITIES:
#    - Extract digits from calibrated marks zone.
#    - Calculate sums and cross-check totals.
#    - Flag mismatches and ambiguities.
# 3. PLANNED CONTENTS: MarkSafeEngine class. Takes OCR grids. Outputs OK/MISMATCH/AMBIGUOUS verdicts.
# 4. INPUTS / OUTPUTS: Inputs: extracted marks from OCR, calibrated zones. Outputs: verification flag object.
# 5. DEPENDS ON / USED BY: PaddleOCR (digits), OpenCV ink-presence.
