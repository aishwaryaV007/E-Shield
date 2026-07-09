/*
 1. FILE PURPOSE: API calls to fetch results — flags, script detail, collusion graph.
 2. RESPONSIBILITIES:
    - getFlags(batchId); getScript(id); getCollusionGraph(batchId).
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: batch/script ids. Outputs: FlagOut[], ScriptOut, graph JSON.
 5. DEPENDS ON / USED BY: lib/api/client, types; used by useFlags + review/scripts pages.
*/
