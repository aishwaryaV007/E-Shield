# 1. FILE PURPOSE: Loads and caches the NLI cross-encoder (nli-deberta-v3-xsmall) for RubricLens.
# 2. RESPONSIBILITIES:
#    - Lazy-load CrossEncoder('cross-encoder/nli-deberta-v3-xsmall') from local cache.
#    - Provide classify(pairs) -> entailment/neutral/contradiction scores.
# 3. PLANNED CONTENTS: get_nli() singleton; classify(pairs) -> labels/scores.
# 4. INPUTS / OUTPUTS: Inputs: (rubric point, student span) pairs. Outputs: NLI label + score.
# 5. DEPENDS ON / USED BY: sentence-transformers CrossEncoder, torch; used by engines/rubriclens.py.
