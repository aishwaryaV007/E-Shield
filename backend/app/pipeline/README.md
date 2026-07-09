# Pipeline Module

This module contains the orchestrator that chains the evaluation stages together.

## Stage Order & Data Flow
1. **Ingestion**: Raw scripts (PDF/images) are loaded, page counted, deskewed, and binarized.
2. **Calibration**: Zones are applied to extract relevant areas.
3. **OCR**: Digits and prose are extracted from zones.
4. **Feature Engines**: MarkSafe, CopyCatch, ScriptID, ReEval Guard, and RubricLens analyze the OCR data.
5. **Storage**: Outputs and ranked flags are persisted to SQLite/JSON.
6. **API**: Front-end retrieves the aggregated anomalies.
