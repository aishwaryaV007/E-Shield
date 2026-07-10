# 1. FILE PURPOSE: Generates demo data for both phases — a small historical training corpus and a
#    fresh batch of scanned scripts to auto-grade (for testing + the live judging demo).
# 2. RESPONSIBILITIES:
#    - Phase 1: generate a historical corpus of answers with teacher-awarded marks -> data/corpus/.
#    - Phase 2: generate a question paper + answer key + rubric -> data/answer_keys/.
#    - Generate a batch of student answer scripts (varying quality) -> data/raw/ to grade against the key.
#    - Include a few deliberately hard cases (partial answers, a strikeout, an off-topic answer).
# 3. PLANNED CONTENTS: seed_corpus() and seed_batch() functions; helpers to render answer-sheet images.
# 4. INPUTS / OUTPUTS: Inputs: Config (corpus size, batch size). Outputs: data/corpus/, data/answer_keys/, data/raw/.
# 5. DEPENDS ON / USED BY: Pillow, NumPy, pandas; output consumed by the training + evaluation pipelines.
