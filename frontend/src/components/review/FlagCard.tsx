/*
 1. FILE PURPOSE: Card presenting a single ranked flag from an engine.
 2. RESPONSIBILITIES:
    - Show engine, severity, reason, and an evidence thumbnail.
    - Offer human-review actions (keep open / mark reviewed) — never auto-resolves.
 3. PLANNED CONTENTS: FlagCard({ flag }) component.
 4. INPUTS / OUTPUTS: Inputs: a FlagOut object. Outputs: card JSX + action callbacks.
 5. DEPENDS ON / USED BY: ui/Card, ui/Badge, review/EvidenceCrop; used by FlagList.
*/
