/*
 1. FILE PURPOSE: API calls for Phase-1 training.
 2. RESPONSIBILITIES:
    - startTraining(config); getTrainingStatus(); getTrainingMetrics().
 3. PLANNED CONTENTS: async functions using the shared axios client.
 4. INPUTS / OUTPUTS: Inputs: corpus/config. Outputs: TrainStatus + TrainMetrics payloads.
 5. DEPENDS ON / USED BY: lib/api/client, types; used by hooks/useTraining + training page.
*/
