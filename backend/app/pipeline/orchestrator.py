# 1. FILE PURPOSE: End-to-end batch run orchestrator.
# 2. RESPONSIBILITIES:
#    - Ingest (pdf_loader -> preprocess -> blankcheck).
#    - OCR (digit + prose -> ambiguity).
#    - Run the 5 engines (MarkSafe, CopyCatch, ScriptID, ReEval Guard, RubricLens).
#    - Persist flags to storage.
#    - Principle: rank & flag, never accuse, never finalize; human decides.
# 3. PLANNED CONTENTS: run_pipeline() function taking batch ID.
# 4. INPUTS / OUTPUTS: Inputs: Raw batch images. Outputs: Ranked verification flags.
# 5. DEPENDS ON / USED BY: Ingestion, OCR, Engines, Storage.
