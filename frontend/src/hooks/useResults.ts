/*
 1. FILE PURPOSE: TanStack Query hooks to fetch evaluated sheets for a batch / single script.
 2. RESPONSIBILITIES:
    - Query lib/api/evaluation.getResults(batchId) and getScriptEvaluation(scriptId).
    - Expose data/loading/error; cache + refetch.
 3. PLANNED CONTENTS: useResults(batchId); useScriptEvaluation(scriptId).
 4. INPUTS / OUTPUTS: Inputs: batch/script id. Outputs: evaluated-sheet query state.
 5. DEPENDS ON / USED BY: @tanstack/react-query, lib/api/evaluation; used by results pages + AnswerList.
*/
