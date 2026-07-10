/*
 1. FILE PURPOSE: API calls for Phase-2 evaluation + fetching evaluated sheets.
 2. RESPONSIBILITIES:
    - runEvaluation(batchId, answerKeyId); getEvaluationStatus(batchId).
    - getResults(batchId); getScriptEvaluation(scriptId); getScriptAnswers(scriptId).
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: batch/script ids. Outputs: EvalStatus, ScriptEvaluation[], AnswerResult[].
 5. DEPENDS ON / USED BY: lib/api/client, types; used by hooks/useEvaluation + useResults.
*/
