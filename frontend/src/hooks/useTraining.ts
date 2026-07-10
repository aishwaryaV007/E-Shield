/*
 1. FILE PURPOSE: Hooks to run Phase-1 training and read its metrics.
 2. RESPONSIBILITIES:
    - Mutation to POST /train; query to GET /train/status and /train/metrics.
 3. PLANNED CONTENTS: useStartTraining(); useTrainingStatus(); useTrainingMetrics().
 4. INPUTS / OUTPUTS: Inputs: corpus/config. Outputs: training mutation + metrics query.
 5. DEPENDS ON / USED BY: @tanstack/react-query, lib/api/training; used by the training page.
*/
