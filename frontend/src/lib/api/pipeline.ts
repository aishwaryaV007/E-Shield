/*
 1. FILE PURPOSE: API calls to run the evaluation pipeline and poll status.
 2. RESPONSIBILITIES:
    - runPipeline(batchId); getStatus(batchId).
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: batch id. Outputs: run ack + status payloads.
 5. DEPENDS ON / USED BY: lib/api/client, types; used by usePipeline.
*/
