# MarkSafe Verification Engine
> Architectural specifications for physical digit OCR, score summation checking, regex parsing rules, and strikeout safety fallbacks.

*Design / Planned — Not yet implemented*

---

## 1. Engine Purpose & Core Logic

**MarkSafe** acts as the trust validation layer for ExamShield. Its primary goal is to identify mathematical and entry discrepancies on graded answer sheets before final scores are posted.

### Governing Principle
> **"Never guess ambiguous marks; when in doubt, flag for review."**
> If a digit is unclear, overwritten, or crossed out, the engine flags it as `AMBIGUOUS`. The system does not attempt to automatically correct grades.

```
                   ┌──────────────────────────────────┐
                   │ Calibrated Marks Box Crops (PNG) │
                   └────────────────┬─────────────────┘
                                    │
                                    ▼ (Tier-1 Digit OCR)
                   ┌──────────────────────────────────┐
                   │ Cleaned Digit Strings (0-9/.+)   │
                   └────────────────┬─────────────────┘
                                    │
                                    ▼ (Regex Rule Matching)
              ┌─────────────────────┴─────────────────────┐
              │                                           │
       Valid Format?                               No / Mismatch
              │                                           │
              ▼                                           ▼
   [ Sum individual fields ]                   [ Raise PENDING Flag ]
              │                                           │
      Matches Written Total?                              │
       ┌──────┴──────┐                                    │
    Yes│             │No                                  │
       ▼             ▼                                    ▼
   [ Approve ]   [ Flag: SUM_MISMATCH ]          [ Flag: AMBIGUOUS_MARK ]
```

---

## 2. Token Matching & Regular Expressions

The engine parses digit outputs using target regular expression formats:

*   **Standard Integer Rule:** `^\d+$` (e.g., `5`, `10`).
*   **Fractional Value Rule:** `^\d+\.\d+$` or `^\d+/10$` (e.g., `4.5`, `9/10`).
*   **Evaluable Sub-questions Rule:** `^\d+(\+\d+)+$` (e.g., `3+4` for sub-questions `a` and `b`).

```python
# Planned implementation pattern
import re

def parse_marks_token(token: str) -> float | None:
    # Remove whitespace
    clean_token = token.strip().replace(" ", "")
    
    # 1. Standard Decimal/Integer Match
    if re.match(r"^\d+(\.\d+)?$", clean_token):
        return float(clean_token)
        
    # 2. Fractions Match (extract numerator)
    fraction_match = re.match(r"^(\d+(\.\d+)?)/\d+$", clean_token)
    if fraction_match:
        return float(fraction_match.group(1))
        
    # 3. Addition Sub-questions Match
    addition_match = re.match(r"^(\d+(\.\d+)?)(?:\+(\d+(\.\d+)?))+$", clean_token)
    if addition_match:
        parts = re.split(r"\+", clean_token)
        return sum(float(part) for part in parts)
        
    # 4. Unknown or crossed-out token
    return None
```

---

## 3. Strikeout & Ambiguity Handling

Messy grader adjustments (e.g., crossing out a `5` and writing `8` next to it) result in overlapping strokes that lower OCR confidence scores:

```
[ Grader writes: ~~5~~ 8 ]  ──►  [ OCR Reads: "58" or "B" (Conf: 0.42) ]  ──►  [ Trigger Flag ]
```

1.  **Low Confidence Trigger:** If the raw PaddleOCR token prediction confidence score falls below **`0.85`**, the system skips automatic parsing and flags the zone as `AMBIGUOUS_MARK`.
2.  **Sum Contradiction Trigger:** If the parsed page marks sum does not equal the written total, the script is flagged as `SUM_MISMATCH`.
3.  **Ink Presence Conflict:** If pixel-density checks identify handwriting in an answer box but the corresponding marks grid field is empty, the system raises a `PAGE_MISSING_GRADE` warning.

All flags present the auditor with coordinates-based crops of the marks column and overall total box in the Streamlit UI, allowing for fast manual resolution.

---

## 4. Related Documents

*   [OCR Module Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/ocr/README.md)
*   [ReEval Guard Borderline Sorting](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/REEVAL_GUARD.md)
*   [Engines Implementation Plans](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ENGINES_PLAN.md)
