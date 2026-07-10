# 1. FILE PURPOSE: Orchestrates the two pipelines — Phase 1 (train the mark-predictor) and Phase 2 (auto-grade a batch).
# 2. RESPONSIBILITIES:
#    - train_pipeline(): dataset_builder -> features -> trainer -> evaluate; persist model + metrics.
#    - evaluate_pipeline(batch_id): ingest (pdf_loader -> preprocess) -> handwriting OCR ->
#      segment (question_segmenter -> answer_matcher) -> score (similarity + trained model) ->
#      feedback -> report; persist the evaluated sheets.
#    - Principle: the mark comes from the trained model, never an LLM; unreadable answers are flagged.
# 3. PLANNED CONTENTS: train_pipeline(corpus) and evaluate_pipeline(batch_id) functions.
# 4. INPUTS / OUTPUTS: Inputs: historical corpus (Phase 1) / scanned batch + answer key (Phase 2).
#    Outputs: trained model + metrics (Phase 1) / evaluated answer sheets (Phase 2).
# 5. DEPENDS ON / USED BY: training/*, ingestion/*, ocr/*, segmentation/*, evaluation/*, storage/.
