# ExamShield Dashboard Module
> Specifications for the local Streamlit web application dashboard and visual evidence views.

*Design / Planned — Not yet implemented*

---

## 1. Dashboard User Interface Structure

The dashboard operates as a multi-tab desktop view served locally via Streamlit, pulling analysis metrics from the backend SQLite DB and FastAPI service.

```
┌────────────────────────────────────────────────────────────────────────┐
│ ExamShield Dashboard                       [Batch Selector: MidtermA ] │
├─────────────┬─────────────────┬────────────────┬──────────────┬────────┤
│ Ingestion   │ MarkSafe Sums   │ CopyCatch Net  │ Script Roster│ ReEval │
├─────────────┴─────────────────┴────────────────┴──────────────┴────────┤
│                                                                        │
│  Ranked Flagged Anomalies:                                             │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Flag ID: F-102 | Type: MarkSafe Mismatch | Status: PENDING       │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │ OCR Read Sum: 34  | written Total Box: 24 | Diff: -10            │  │
│  │                                                                  │  │
│  │  Page 1 Crops:                                                   │  │
│  │  ┌─────────────────────────┐      ┌───────────────────────────┐  │  │
│  │  │ Marks Column Crop:      │      │ Total Score Box Crop:     │  │  │
│  │  │ [ 10 | 12 | 12 ]        │      │ [ 24 ]                    │  │  │
│  │  │                         │      │                           │  │  │
│  │  └─────────────────────────┘      └───────────────────────────┘  │  │
│  │                                                                  │  │
│  │  Grader Override Entry: [ 34 ]        [ Resolve Mismatch ]       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Primary Dashboard Views
1.  **Ingestion Overview:** Logs batch loading speed, blank check results, and document template calibrations.
2.  **MarkSafe sum Auditor:** Displays list items sorted by mismatch margins, showing raw crops alongside human input fields.
3.  **CopyCatch Network:** Embeds interactive HTML widgets rendering PyVis collusion clusters. Clicking a student node opens side-by-side prose comparison crops.
4.  **Script Roster Auditor (ScriptID):** Alerts users to unregistered IDs, missing sheets, and double-graded roll numbers.
5.  **ReEval Guard List:** Displays borderline pass/fail folders for prioritized regrading.

---

## 2. Dashboard Technical Orchestration (`main.py`)

Streamlit manages component routing while loading visual crops via Pillow (`PIL`):

```python
# Planned implementation pattern
import streamlit as st
import requests
from PIL import Image
import io

def render_marksafe_audit(batch_id: str):
    st.subheader("MarkSafe Sum Discrepancy Queue")
    
    # Retrieve anomalies from FastAPI
    response = requests.get(f"http://localhost:8000/api/v1/batch/{batch_id}/anomalies")
    anomalies = response.json().get("anomalies", [])
    
    for anomaly in anomalies:
        col1, col2 = st.columns(2)
        
        with col1:
            st.warning(f"Student Roll Number: {anomaly['roll_number']}")
            st.metric("OCR Calculated Sum", anomaly["ocr_sum"])
            st.metric("Grader Written Total", anomaly["written_total"])
            
        with col2:
            st.image(anomaly["marks_column_crop_url"], caption="Calibrated Marks Entry Crop")
            st.image(anomaly["total_box_crop_url"], caption="Written Total Box Crop")
            
        resolved_value = st.number_input(
            "Resolve Correct Marks Value:", 
            value=int(anomaly["ocr_sum"]), 
            key=anomaly["flag_id"]
        )
        
        if st.button("Confirm Corrected Value", key=f"btn_{anomaly['flag_id']}"):
            requests.post("http://localhost:8000/api/v1/marks/override", json={
                "flag_id": anomaly["flag_id"],
                "resolved_value": resolved_value
            })
            st.success("Flag resolved successfully!")
```

---

## 3. Related Documents

*   [API Schema Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)
*   [CopyCatch Interactive Visualizations](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [User Interface Layout Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DASHBOARD_PLAN.md)
