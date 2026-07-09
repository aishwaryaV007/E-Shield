/*
 1. FILE PURPOSE: Landing page — batch overview and entry into the workflow.
 2. RESPONSIBILITIES:
    - List batches and their status; link to ingestion/calibration/review.
    - Show high-level stats (scripts processed, open flags).
 3. PLANNED CONTENTS: Home() page component fetching batch summary via hooks.
 4. INPUTS / OUTPUTS: Inputs: backend batch list. Outputs: overview UI.
 5. DEPENDS ON / USED BY: hooks (useFlags/usePipeline), components/review, ui/*.
*/
