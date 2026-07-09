# 1. FILE PURPOSE: Manages the one-time template JSON mapping calibrated zones (marks column, total box, roll-no box, answer regions) per institution format.
# 2. RESPONSIBILITIES:
#    - Load zone definitions.
#    - Save new templates from the Streamlit UI.
#    - Provide bounding boxes to the pipeline.
# 3. PLANNED CONTENTS: TemplateIO utility. Reads/writes template JSON schemas.
# 4. INPUTS / OUTPUTS: Inputs: JSON payloads from calibration UI. Outputs: parsed zone coordinates.
# 5. DEPENDS ON / USED BY: JSON, SQLite.
