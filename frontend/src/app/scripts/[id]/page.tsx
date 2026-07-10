/*
 1. FILE PURPOSE: Single-script evaluated-sheet view — the fully auto-graded answer sheet.
 2. RESPONSIBILITIES:
    - Show total marks, percentage (ScoreSummary) and the question-wise breakdown.
    - For each answer: student text, answer key, similarity, predicted mark, feedback, deduction reasons.
    - Flag low-confidence OCR answers for optional human verification before publishing.
 3. PLANNED CONTENTS: ScriptDetailPage({ params }) reading the route id via hooks/useResults.
 4. INPUTS / OUTPUTS: Inputs: script id (route param). Outputs: evaluated-sheet UI.
 5. DEPENDS ON / USED BY: hooks/useResults, results/ScoreSummary + AnswerList + AnswerCompare; App Router.
*/
