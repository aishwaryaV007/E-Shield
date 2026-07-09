/*
 1. FILE PURPOSE: The main review dashboard page. Renders ranked flags and image-level evidence so the human can review and decide on anomalies detected by the engines.
 2. RESPONSIBILITIES:
    - Fetch ranked flags from backend.
    - Display CopyCatch graph and MarkSafe discrepancies.
    - Provide interface for human verdict.
 3. PLANNED CONTENTS: Next.js page component. Assembles FlagCard, EvidenceCrop, and CollusionGraph.
 4. INPUTS / OUTPUTS: Inputs: API data. Outputs: Human decision UI.
 5. DEPENDS ON / USED BY: React, TanStack Query, Tailwind.
*/
