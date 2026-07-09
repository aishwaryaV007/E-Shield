/*
 1. FILE PURPOSE: API calls for ingestion + BlankCheck.
 2. RESPONSIBILITIES:
    - uploadScripts(batchId, files); runBlankCheck(scriptId).
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: files/ids. Outputs: typed ingest/blankcheck responses.
 5. DEPENDS ON / USED BY: lib/api/client, types; used by usePipeline / ingestion page.
*/
