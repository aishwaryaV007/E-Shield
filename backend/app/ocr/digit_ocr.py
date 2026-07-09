# 1. FILE PURPOSE: Executes robust PaddleOCR digit recognition exclusively on calibrated zones (never full-page) for MarkSafe and ScriptID.
# 2. RESPONSIBILITIES:
#    - Run OCR configured for digits only.
#    - Extract confidence scores per digit.
#    - Ignore out-of-zone noise.
# 3. PLANNED CONTENTS: DigitOCR class. Takes image crops, returns numeric strings and confidences.
# 4. INPUTS / OUTPUTS: Inputs: image crops of marks/totals/roll-no. Outputs: text strings + confidence.
# 5. DEPENDS ON / USED BY: PaddleOCR.
