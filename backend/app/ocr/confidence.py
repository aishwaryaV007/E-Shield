# 1. FILE PURPOSE: OCR confidence handling — flags low-confidence handwriting recognition so the grader can be told "verify this answer".
# 2. RESPONSIBILITIES:
#    - Aggregate per-token confidence into an answer-level confidence score.
#    - Mark answers below threshold as LOW_CONFIDENCE (surfaced in the report, never silently trusted).
#    - Keep the auto-grader honest: an unreadable answer is flagged, not guessed.
# 3. PLANNED CONTENTS: answer_confidence(ocr_result) -> float; needs_human_check(score) -> bool.
# 4. INPUTS / OUTPUTS: Inputs: OCR tokens + confidences. Outputs: confidence score + LOW_CONFIDENCE flag.
# 5. DEPENDS ON / USED BY: numpy; used by ocr/handwriting_ocr.py and evaluation/report.py.
