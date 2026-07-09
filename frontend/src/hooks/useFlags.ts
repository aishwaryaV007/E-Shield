/*
 1. FILE PURPOSE: TanStack Query hook to fetch ranked flags for a batch.
 2. RESPONSIBILITIES:
    - Query lib/api/results.getFlags; expose data/loading/error; cache + refetch.
 3. PLANNED CONTENTS: useFlags(batchId) -> UseQueryResult<FlagOut[]>.
 4. INPUTS / OUTPUTS: Inputs: batch id. Outputs: flags query state.
 5. DEPENDS ON / USED BY: @tanstack/react-query, lib/api/results; used by FlagList.
*/
