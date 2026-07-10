/*
 1. FILE PURPOSE: Shared TypeScript types mirroring backend/app/api/schemas.py (the API contract).
 2. RESPONSIBILITIES:
    - Define Batch, Script, AnswerKey, TrainStatus, TrainMetrics, AnswerResult, ScriptEvaluation types.
    - Keep in sync with the Pydantic schemas on the backend.
 3. PLANNED CONTENTS: exported interfaces/types (ScriptEvaluation = question-wise marks + total + % + feedback).
 4. INPUTS / OUTPUTS: Inputs: none. Outputs: types used across lib/api, hooks, components.
 5. DEPENDS ON / USED BY: Mirrors api/schemas.py; used throughout the frontend.
*/
