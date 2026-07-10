/*
 1. FILE PURPOSE: API calls for ingestion (upload scripts + answer key).
 2. RESPONSIBILITIES:
    - uploadScripts(batchId, files); uploadAnswerKey(batchId, keyFile).
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: files/ids. Outputs: typed ingest responses.
 5. DEPENDS ON / USED BY: lib/api/client, types; used by hooks/useEvaluation / ingestion page.
*/
