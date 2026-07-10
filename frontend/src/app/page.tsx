/*
 1. FILE PURPOSE: Landing page — batch overview and entry into the workflow.
 2. RESPONSIBILITIES:
    - List batches and their status; link to Training, Ingestion, and Results.
    - Show high-level stats (model trained?, scripts evaluated, average score).
 3. PLANNED CONTENTS: Home() page component fetching batch + model summary via hooks.
 4. INPUTS / OUTPUTS: Inputs: backend batch list. Outputs: overview UI.
 5. DEPENDS ON / USED BY: hooks (useResults/useTraining), components/results, ui/*.
*/
