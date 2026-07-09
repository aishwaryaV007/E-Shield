/*
 1. FILE PURPOSE: Hooks to run the pipeline and poll its status.
 2. RESPONSIBILITIES:
    - Mutation to POST /run; query to GET /status; ingest/blankcheck triggers.
 3. PLANNED CONTENTS: useRunPipeline(); usePipelineStatus(batchId).
 4. INPUTS / OUTPUTS: Inputs: batch id. Outputs: run mutation + status query.
 5. DEPENDS ON / USED BY: @tanstack/react-query, lib/api/pipeline; used by ingestion/review pages.
*/
