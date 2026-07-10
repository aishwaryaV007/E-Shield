/*
 1. FILE PURPOSE: Hooks to run the Phase-2 evaluation pipeline and poll its status.
 2. RESPONSIBILITIES:
    - Mutation to POST /evaluate; query to GET /evaluate/status; ingest trigger.
 3. PLANNED CONTENTS: useRunEvaluation(); useEvaluationStatus(batchId).
 4. INPUTS / OUTPUTS: Inputs: batch id + answer-key id. Outputs: run mutation + status query.
 5. DEPENDS ON / USED BY: @tanstack/react-query, lib/api/evaluation + ingestion; used by ingestion/results pages.
*/
