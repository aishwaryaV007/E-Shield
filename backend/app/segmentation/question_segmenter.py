# 1. FILE PURPOSE: Splits a scanned script into individual (question, answer) blocks so each answer can be graded separately.
# 2. RESPONSIBILITIES:
#    - Detect question numbers / answer boundaries on the page (layout + regex on OCR text).
#    - Group multi-page answers belonging to the same question.
#    - Emit an ordered list of answer blocks with page + bbox references.
# 3. PLANNED CONTENTS: QuestionSegmenter class; segment(pages, ocr) -> list[AnswerBlock].
# 4. INPUTS / OUTPUTS: Inputs: preprocessed pages + OCR text. Outputs: per-question answer blocks.
# 5. DEPENDS ON / USED BY: OpenCV, regex; used by pipeline (Phase 2) before answer_matcher.
