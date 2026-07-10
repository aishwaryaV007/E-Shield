# 1. FILE PURPOSE: Read/write JSON artefacts (answer keys, evaluated-sheet exports, training metrics).
# 2. RESPONSIBILITIES:
#    - Save/load answer keys + rubrics to data/answer_keys/*.json.
#    - Persist evaluated sheets to data/results/*.json and training metrics to data/metrics/*.json.
# 3. PLANNED CONTENTS: save_json(path, obj); load_json(path); save_answer_key(); save_evaluation().
# 4. INPUTS / OUTPUTS: Inputs: dict payloads + file paths. Outputs: JSON files on disk / parsed dicts.
# 5. DEPENDS ON / USED BY: json, pathlib, config.DATA_DIR; used by ingestion, evaluation/report, training/evaluate.
