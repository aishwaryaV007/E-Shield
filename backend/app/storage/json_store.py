# 1. FILE PURPOSE: Read/write JSON artefacts (calibration templates and result exports).
# 2. RESPONSIBILITIES:
#    - Save/load zone templates to data/templates/*.json.
#    - Persist pipeline results/flags to data/results/*.json.
# 3. PLANNED CONTENTS: save_json(path, obj); load_json(path); save_template(); load_template().
# 4. INPUTS / OUTPUTS: Inputs: dict payloads + file paths. Outputs: JSON files on disk / parsed dicts.
# 5. DEPENDS ON / USED BY: json, pathlib, config.DATA_DIR; used by calibration + pipeline.
