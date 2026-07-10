/*
 1. FILE PURPOSE: Card presenting one auto-graded answer within an evaluated sheet.
 2. RESPONSIBILITIES:
    - Show question no, predicted mark / max, percentage match, and semantic similarity.
    - Show feedback + mark-deduction reasons; badge low-confidence OCR answers for verification.
 3. PLANNED CONTENTS: AnswerCard({ answer }) component.
 4. INPUTS / OUTPUTS: Inputs: an AnswerResult object. Outputs: card JSX.
 5. DEPENDS ON / USED BY: ui/Card, ui/Badge, results/AnswerCompare; used by AnswerList.
*/
