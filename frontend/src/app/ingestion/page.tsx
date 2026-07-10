/*
 1. FILE PURPOSE: Ingestion page (Phase 2 input) — upload scanned scripts + the answer key, then start evaluation.
 2. RESPONSIBILITIES:
    - Upload PDFs/images for a batch and the question paper + answer key + rubric.
    - Trigger the auto-grading run and show its progress.
 3. PLANNED CONTENTS: IngestionPage() component using lib/api/ingestion + hooks/useEvaluation.
 4. INPUTS / OUTPUTS: Inputs: file uploads. Outputs: ingest + evaluation-run status UI.
 5. DEPENDS ON / USED BY: lib/api/ingestion.ts, hooks/useEvaluation.ts, ui/*.
*/
