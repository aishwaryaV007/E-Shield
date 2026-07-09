# ReEval Guard Engine
> Architectural specifications for borderline score sorting, grade boundary rules, and priority audit queues.

*Design / Planned — Not yet implemented*

---

## 1. Engine Purpose & Core Logic

**ReEval Guard** implements a preemptive review queue for borderline grades. 

In traditional exam systems, students who score just below a passing threshold or grade boundary (e.g., scoring 39 when 40 is a pass) frequently file paid revaluation disputes. ReEval Guard automates this review by identifying and queueing these scripts *before* results are finalized.

```
                    ┌───────────────────────────────┐
                    │  MarkSafe Graded Total (Sum)  │
                    └───────────────┬───────────────┘
                                    │
                                    ▼ (Evaluate Boundaries)
                    ┌───────────────────────────────┐
                    │ Compare to Config thresholds  │
                    └───────────────┬───────────────┘
                                    │
                       ┌────────────┴────────────┐
                       │  Within review range?   │
                       └─────┬──────────────┬────┘
                             │              │
                    Yes      │              │ No
                             ▼              ▼
                     [ Flag: BORDERLINE ]   [ Log normal total ]
                             │              │
                             └──────┬───────┘
                                    │
                                    ▼
                         [ Save state to SQLite ]
```

---

## 2. Borderline Detection & Sorting (`reeval_guard.py`)

The engine checks final script totals against a JSON configuration file containing passing limits and grade cutoffs:

```python
# Planned implementation pattern
class ReEvalGuardEngine:
    def __init__(self, config: dict):
        # Load grade boundary structures
        self.pass_mark = config.get("pass_mark", 40.0)
        self.grade_boundaries = config.get("grade_boundaries", [50.0, 60.0, 70.0, 80.0])
        # Define priority lookup margin (e.g., 2 marks below cutoff)
        self.review_margin = config.get("review_margin", 2.0)
        
    def evaluate_script(self, script_id: str, total_marks: float) -> dict:
        result = {
            "script_id": script_id,
            "total_marks": total_marks,
            "is_borderline": False,
            "flag_type": None,
            "target_cutoff": None
        }
        
        # 1. Check pass/fail boundary
        pass_diff = self.pass_mark - total_marks
        if 0 < pass_diff <= self.review_margin:
            result["is_borderline"] = True
            result["flag_type"] = "BORDERLINE_PASS_FAIL"
            result["target_cutoff"] = self.pass_mark
            return result
            
        # 2. Check grade-boundary cutoffs (A, B, C, etc.)
        for boundary in self.grade_boundaries:
            grade_diff = boundary - total_marks
            if 0 < grade_diff <= self.review_margin:
                result["is_borderline"] = True
                result["flag_type"] = "BORDERLINE_GRADE_CUTOFF"
                result["target_cutoff"] = boundary
                return result
                
        return result
```

---

## 3. Review Queue Prioritization

Scripts flagged as `BORDERLINE` are routed to a dedicated review tab in the dashboard. The dashboard sorts these scripts by proximity to the cutoff margin:

| Roll Number | Extracted Score | Target Boundary | Gap | Review Status |
| :--- | :--- | :--- | :--- | :--- |
| **26SN101014** | 39.0 | 40.0 (Pass Cutoff) | -1.0 | **PENDING AUDIT** |
| **26SN101035** | 38.5 | 40.0 (Pass Cutoff) | -1.5 | **PENDING AUDIT** |
| **26SN101009** | 58.5 | 60.0 (Grade B Cutoff) | -1.5 | **PENDING AUDIT** |

### Audit Action Steps
1.  The auditor selects a borderline student file.
2.  The interface loads page thumbnails and highlights question crops that are blank or graded low.
3.  The auditor can verify if any attempted answers were missed during grading, resolving disputes pre-publication.

---

## 4. Related Documents

*   [MarkSafe Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/MARKSAFE.md)
*   [Database Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
