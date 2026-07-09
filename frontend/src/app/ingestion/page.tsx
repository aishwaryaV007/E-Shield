/*
 1. FILE PURPOSE: Ingestion page — upload scanned scripts and view BlankCheck results.
 2. RESPONSIBILITIES:
    - Upload PDFs/images for a batch and trigger ingest.
    - Display page-count + ink-presence (BlankCheck) outcomes.
 3. PLANNED CONTENTS: IngestionPage() component using lib/api/ingestion + usePipeline.
 4. INPUTS / OUTPUTS: Inputs: file uploads. Outputs: ingest/blankcheck status UI.
 5. DEPENDS ON / USED BY: lib/api/ingestion.ts, hooks/usePipeline.ts, ui/*.
*/
