/*
 1. FILE PURPOSE: Side-by-side view of the student's OCR'd answer against the official answer key.
 2. RESPONSIBILITIES:
    - Render student answer text next to the model answer / rubric points.
    - Highlight covered key-points (green) and missing/contradicted ones (red) that drove the mark.
    - Optionally show the original answer-region image crop for verification.
 3. PLANNED CONTENTS: AnswerCompare React component. Takes student text, key text, coverage map.
 4. INPUTS / OUTPUTS: Inputs: answer + key + coverage. Outputs: comparison JSX.
 5. DEPENDS ON / USED BY: Next/Image, Tailwind; used by AnswerCard / scripts detail page.
*/
