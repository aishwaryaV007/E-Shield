# 1. FILE PURPOSE: Retrieval + NLI (deberta-xsmall) to highlight where student text aligns (green) or contradicts (red) the rubric. Never outputs a mark.
# 2. RESPONSIBILITIES:
#    - Retrieve candidate regions for rubric points.
#    - Run NLI cross-encoder for entailment/contradiction.
#    - Highlight text regions.
# 3. PLANNED CONTENTS: RubricLensEngine class. Takes rubric points and prose OCR. Returns highlight coordinates.
# 4. INPUTS / OUTPUTS: Inputs: rubric text, student answer OCR. Outputs: colored text coordinates.
# 5. DEPENDS ON / USED BY: cross-encoder/nli-deberta-v3-xsmall, sentence-transformers.
