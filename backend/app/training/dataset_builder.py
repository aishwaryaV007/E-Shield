# 1. FILE PURPOSE: (Phase 1) Builds the supervised training dataset from historical teacher-corrected answer scripts.
# 2. RESPONSIBILITIES:
#    - Read past scripts + question papers + answer keys + rubrics + teacher-awarded marks (the labels).
#    - Pair every historical student answer with its answer key and the mark the teacher gave it.
#    - Emit a tabular dataset: one row per (student_answer, answer_key, features..., teacher_mark).
# 3. PLANNED CONTENTS: build_dataset(corpus_dir) -> pandas.DataFrame; train/val/test split helper.
# 4. INPUTS / OUTPUTS: Inputs: historical corrected corpus. Outputs: labeled DataFrame for training/features.
# 5. DEPENDS ON / USED BY: pandas; used by training/trainer.py, feeds training/features.py.
