/*
 1. FILE PURPOSE: Results page (Phase 2) — lists the auto-graded scripts in a batch with totals and percentages.
 2. RESPONSIBILITIES:
    - Fetch evaluated scripts for the selected batch.
    - Show each script's total marks, percentage, and any low-confidence answers to verify.
    - Link into the per-script evaluated sheet.
 3. PLANNED CONTENTS: ResultsPage() using hooks/useResults; renders a table of ScriptEvaluation rows.
 4. INPUTS / OUTPUTS: Inputs: batch id. Outputs: evaluated-scripts overview UI.
 5. DEPENDS ON / USED BY: hooks/useResults, components/results/*, ui/*.
*/
