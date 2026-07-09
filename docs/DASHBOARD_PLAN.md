# Dashboard Interface Development Plan
> Development steps, layout configurations, evidence crop interfaces, and manual override routers.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

The **Dashboard Interface** provides a visual portal for exam-cell staff, displaying pipeline logs, node cluster graphs, and evidence crops to simplify audit reviews.

```
┌────────────────────────────────────────────────────────┐
│ Streamlit UI Entrypoint (dashboard/main.py)            │
└───────────────────────┬────────────────────────────────┘
                        │
         ┌──────────────┼──────────────┬────────────────┐
         ▼              ▼              ▼                ▼
   [ Tab 1: Ingest ] [ Tab 2: Sums ][ Tab 3: Graph ][ Tab 4: Border ]
   • Loader logs     • MarkSafe list• PyVis network  • ReEval queue
   • Blank checks    • Crop views   • Side-by-side   • Roster check
```

---

## 2. Technical Task Breakdown

### Task 1: Main Streamlit Tab Routing (`app/dashboard/main.py`)
*   **Objectives:** Build the primary navigation structure and batch selectors for the local dashboard.
*   **Implementation Steps:**
    1.  Create a sidebar for batch selection (reading active batches from SQLite).
    2.  Implement tab layouts: Ingestion Logs, MarkSafe Auditor, CopyCatch Network, ScriptID, and ReEval Guard.
    3.  Configure page styling: set clean fonts, a dark visual theme, and responsive element containers.

### Task 2: CopyCatch PyVis Network Viewer (`app/dashboard/views.py`)
*   **Objectives:** Render the interactive collusion graph and enable page comparison views.
*   **Implementation Steps:**
    1.  Use PyVis to construct an interactive HTML network graph.
    2.  Embed the PyVis HTML layout within Streamlit components.
    3.  Configure node click events: selecting a connection edge retrieves text crops from the two related booklets and displays them side-by-side for comparison.

### Task 3: Grader Correction Entry Form (`app/dashboard/views.py`)
*   **Objectives:** Let administrators override OCR totals or resolve audit discrepancies.
*   **Implementation Steps:**
    1.  Build an input form next to highlighted flag zones.
    2.  Set up confirmation buttons to send corrections to the FastAPI endpoint (`/api/v1/marks/override`).
    3.  Implement validation logic to ensure user overrides update flag status values to `RESOLVED` in the SQLite database.

---

## 3. Related Documents

*   [Dashboard Subsystem Module specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/dashboard/README.md)
*   [API Specifications Guide](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
