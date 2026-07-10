# 1. FILE PURPOSE: Handwriting OCR — extracts the student's handwritten answer text from each segmented answer region of a scanned script.
# 2. RESPONSIBILITIES:
#    - Run a handwriting-capable OCR model (TrOCR handwritten / PaddleOCR) on answer-region crops.
#    - Return recognised text plus per-line/per-token confidence scores.
#    - Never call an LLM to "read" the page; recognition is a local CV/OCR model only.
# 3. PLANNED CONTENTS: HandwritingOCR class; recognize(image) -> {text, confidence, lines}.
# 4. INPUTS / OUTPUTS: Inputs: preprocessed answer-region images. Outputs: extracted text + confidence.
# 5. DEPENDS ON / USED BY: TrOCR/PaddleOCR, torch; used by pipeline (Phase 2) before segmentation/matching.
