# Segmentation Module (Phase 2)

Turns a raw scanned script into gradable units. Replaces the old zone-calibration
approach — instead of drawing fixed rectangles per institution, we detect questions
and answers from layout + OCR text.

- `question_segmenter.py` — split the script into per-question answer blocks.
- `answer_matcher.py` — align each answer with its question, answer key, rubric, and max marks.
