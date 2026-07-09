# 1. FILE PURPOSE: Digit-OCRs the roll-number box and validates it against the class register to catch duplicates/absentees/misreads.
# 2. RESPONSIBILITIES:
#    - Digit OCR on roll-number box.
#    - Cross-reference with pandas CSV register.
#    - Flag duplicates and absentees.
# 3. PLANNED CONTENTS: ScriptIDEngine class. Takes roll number box OCR. Returns presence/absence flags.
# 4. INPUTS / OUTPUTS: Inputs: roll number OCR text, register CSV. Outputs: identity verification flags.
# 5. DEPENDS ON / USED BY: PaddleOCR, pandas.
