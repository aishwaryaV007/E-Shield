/*
 1. FILE PURPOSE: Single-script evidence view.
 2. RESPONSIBILITIES:
    - Show a script's flags, marks breakdown, and side-by-side evidence crops.
    - Let the auditor review each flag; never auto-resolves.
 3. PLANNED CONTENTS: ScriptDetailPage({ params }) reading the route id.
 4. INPUTS / OUTPUTS: Inputs: script id (route param). Outputs: detailed evidence UI.
 5. DEPENDS ON / USED BY: lib/api/results.getScript, review/EvidenceCrop; App Router.
*/
