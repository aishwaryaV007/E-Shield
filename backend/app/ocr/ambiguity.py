# 1. FILE PURPOSE: Ambiguity fallback — decides when OCR output is too uncertain to trust.
# 2. RESPONSIBILITIES:
#    - Evaluate OCR confidence and detect strikeouts/overwrites.
#    - Return an 'Ambiguous — Human Review' sentinel instead of a guessed value.
# 3. PLANNED CONTENTS: is_ambiguous(ocr_result) -> bool; wrap_value_or_ambiguous(...).
# 4. INPUTS / OUTPUTS: Inputs: OCR token + confidence. Outputs: parsed value or AMBIGUOUS sentinel.
# 5. DEPENDS ON / USED BY: Used by ocr/digit_ocr.py and engines (marksafe, scriptid). Enforces 'never guess'.
