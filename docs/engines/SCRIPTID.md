# ScriptID Verification Engine
> Architectural specifications for roll-number digit OCR, roster verification, and student identity mismatch flags.

*Design / Planned — Not yet implemented*

---

## 1. Engine Purpose & Core Logic

The **ScriptID** engine validates student identity details. It ensures that every scanned paper matches an enrolled student in the class register and flags administrative errors before grades are posted.

```
                   ┌──────────────────────────────────┐
                   │ Calibrated Roll Number Box Crop  │
                   └────────────────┬─────────────────┘
                                    │
                                    ▼ (Tier-1 Digit OCR)
                   ┌──────────────────────────────────┐
                   │ Parsed Roll Number String        │
                   └────────────────┬─────────────────┘
                                    │
                       ┌────────────┴────────────┐
                       │   Roster lookup match?  │
                       └─────┬──────────────┬────┘
                             │              │
                    Matches  │              │ Mismatch / Duplicate
                             ▼              ▼
                     [ Roster Match ]   [ Raise Flag: DUPLICATE_ID / UNREGISTERED ]
                             │              │
                             └──────┬───────┘
                                    │
                                    ▼
                         [ Save state to SQLite ]
```

---

## 2. Roster Matching Logic (`scriptid.py`)

The engine compares OCR-parsed roll numbers against the official register database using pandas lookups:

```python
# Planned implementation pattern
import pandas as pd

class ScriptIDEngine:
    def __init__(self, register_path: str):
        # Load official student register
        self.register_df = pd.read_csv(register_path)
        self.enrolled_ids = set(self.register_df["student_id"].astype(str).tolist())
        self.scanned_ids = {}

    def verify_script_identity(self, script_id: str, extracted_roll: str) -> dict:
        result = {
            "script_id": script_id,
            "roll_number": extracted_roll,
            "flag_raised": None,
            "details": ""
        }
        
        # 1. Check for blank or unreadable roll numbers
        if not extracted_roll or extracted_roll.strip() == "":
            result["flag_raised"] = "MISSING_ID"
            result["details"] = "Roll number box OCR failed to detect text."
            return result
            
        # 2. Check registration roster
        if extracted_roll not in self.enrolled_ids:
            result["flag_raised"] = "UNREGISTERED_ID"
            result["details"] = f"ID '{extracted_roll}' not found in official class register."
            return result
            
        # 3. Check for duplicates (multiple booklets uploaded under same ID)
        if extracted_roll in self.scanned_ids:
            result["flag_raised"] = "DUPLICATE_ID"
            result["details"] = (
                f"Duplicate submissions: script '{script_id}' and "
                f"script '{self.scanned_ids[extracted_roll]}' share ID '{extracted_roll}'."
            )
            return result
            
        # Add to processed list if valid
        self.scanned_ids[extracted_roll] = script_id
        return result
```

---

## 3. Flag Scenarios

ScriptID raises three primary administrative flags:

| Flag Type | Trigger Conditions | Resolution Strategy |
| :--- | :--- | :--- |
| **UNREGISTERED_ID** | The OCR-extracted roll number does not match any entry in the class register CSV. | The dashboard displays the student's handwritten ID box crop, allowing the auditor to correct OCR errors (e.g., misreading `0` as `D`). |
| **DUPLICATE_ID** | Two separate answer booklets are parsed with the same roll number. | The auditor reviews both booklets side-by-side to resolve duplication errors. |
| **ABSENTEE_WITH_SCRIPT** | The register logs a student as absent, but a booklet is scanned under their ID. | The system prompts the administrator to verify physical attendance sheets. |

---

## 4. Related Documents

*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Database Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Engines Implementation Plans](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ENGINES_PLAN.md)
