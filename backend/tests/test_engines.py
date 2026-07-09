# 1. FILE PURPOSE: Test suite for the 5 verification engines in backend/app/engines/.
# 2. RESPONSIBILITIES:
#    - Test backend/app/engines/marksafe.py — sum-vs-total arithmetic verification.
#    - Test backend/app/engines/copycatch.py — pairwise similarity and graph output.
#    - Test backend/app/engines/scriptid.py — roll-number vs register matching.
#    - Test backend/app/engines/reeval_guard.py — borderline threshold flagging.
#    - Test backend/app/engines/rubriclens.py — NLI entailment/contradiction output.
# 3. PLANNED CONTENTS: One test function per engine; uses pytest fixtures and mock OCR data.
# 4. INPUTS / OUTPUTS: Inputs: Mock script data and OCR results. Outputs: pytest pass/fail.
# 5. DEPENDS ON / USED BY: pytest, backend/app/engines/* (resolved via pyproject.toml pythonpath).
