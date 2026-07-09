# 1. FILE PURPOSE: Pydantic request/response models — the API contract shared with the frontend.
# 2. RESPONSIBILITIES:
#    - Define models for batches, scripts, flags, templates, and pipeline status.
#    - Keep field names/types in sync with frontend/src/types/index.ts.
# 3. PLANNED CONTENTS: BaseModel classes: BatchCreate, ScriptOut, FlagOut, TemplateIn/Out, PipelineStatus, CollusionGraph.
# 4. INPUTS / OUTPUTS: Inputs: request bodies. Outputs: serialised JSON responses.
# 5. DEPENDS ON / USED BY: pydantic; used by all api/routes/*; mirrored by frontend types/index.ts.
