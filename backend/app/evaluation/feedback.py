# 1. FILE PURPOSE: Generates per-answer feedback and mark-deduction reasons, so the evaluated sheet explains itself like a human examiner.
# 2. RESPONSIBILITIES:
#    - Turn the concept-coverage breakdown into plain-language feedback (covered points, missing points, contradictions).
#    - State WHY marks were deducted (which rubric points were missing/wrong).
#    - Optionally use an LLM only to phrase the feedback text — the MARK is never decided by an LLM.
# 3. PLANNED CONTENTS: build_feedback(unit, coverage, mark) -> {summary, strengths, gaps, deduction_reasons}.
# 4. INPUTS / OUTPUTS: Inputs: coverage + predicted mark. Outputs: structured feedback per answer.
# 5. DEPENDS ON / USED BY: evaluation/concept_coverage.py; used by evaluation/report.py.
