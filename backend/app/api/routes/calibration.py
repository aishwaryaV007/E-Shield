# 1. FILE PURPOSE: API routes for zone-calibration templates.
# 2. RESPONSIBILITIES:
#    - GET /templates — list saved zone templates.
#    - POST /templates — save a new zone template (marks/total/roll-no/answer regions) as JSON.
# 3. PLANNED CONTENTS: FastAPI endpoints reading/writing via app/calibration/template_io.py.
# 4. INPUTS / OUTPUTS: Inputs: template JSON payloads. Outputs: stored template metadata.
# 5. DEPENDS ON / USED BY: fastapi, api/schemas.py, app/calibration/template_io.py.
