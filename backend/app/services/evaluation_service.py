# 1. FILE PURPOSE: Business logic mediating between API routes and the two pipelines (training + evaluation).
# 2. RESPONSIBILITIES:
#    - Create a batch and register its answer key / rubric.
#    - Kick off Phase-1 training (delegates to app/training/*) and expose metrics.
#    - Kick off Phase-2 evaluation for a batch (delegates to app/pipeline/orchestrator.evaluate_pipeline).
#    - Fetch evaluated sheets (question-wise marks, totals, feedback) for the frontend.
# 3. PLANNED CONTENTS: EvaluationService class.
# 4. INPUTS / OUTPUTS: Inputs: API requests. Outputs: training status/metrics + evaluated-sheet domain models.
# 5. DEPENDS ON / USED BY: app/training/*, app/pipeline/, app/storage/; used by api/routes/* via deps.get_evaluation_service().
