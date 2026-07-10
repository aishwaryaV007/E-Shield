# 1. FILE PURPOSE: Aggregates all API route modules into a single router.
# 2. RESPONSIBILITIES:
#    - Import the ingestion, training, evaluation, and results routers.
#    - Combine them into one APIRouter for main.py to include.
# 3. PLANNED CONTENTS: `api_router = APIRouter()` including each sub-router with prefixes/tags.
# 4. INPUTS / OUTPUTS: Inputs: sub-routers. Outputs: a combined api_router.
# 5. DEPENDS ON / USED BY: fastapi.APIRouter; routes/*; included by main.py.
