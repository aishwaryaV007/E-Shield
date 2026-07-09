# ExamShield High-Level Build Plan
> Sequential development milestones (M0–M6) mapping the transition of ExamShield from conceptual design to a verified local desktop application.

*Design / Planned — Not yet implemented*

---

## 1. Milestone Roadmap

The build timeline is structured sequentially, prioritizing the ingestion spine and core risk-detection engines (MarkSafe, CopyCatch) before developing administrative helper tools and UI dashboard wrappers.

```
 M0: Core Ingestion Spine ────────────────────────┐
                                                  ▼
 M1: MarkSafe (Trust) ──────────────────────────► M3: Admin Helpers (ScriptID & ReEval)
                                                  ▲
 M2: CopyCatch (Collusion) ───────────────────────┘
                                                  │
                                                  ▼
 M6: Live Demo & Hardening ◄── M5: Stretch ◄── M4: Streamlit Dashboard
```

---

## 2. Milestones Breakdown

### M0: Core Ingestion Spine (Target: H0–H3)
Build the foundational pipeline that reads raw scans and maps coordinates.
*   **Objectives:** Load batches of physical scripts, deskew/denoise images, and output template alignment coordinates.
*   **Deliverables:**
    *   Image processing pipeline using OpenCV (`deskew.py`, `binarize.py`).
    *   One-time calibration GUI using Streamlit Canvas to output template JSON configurations.
    *   PDF rasterization utility (`pypdfium2`).

### M1: MarkSafe Trust Layer (Target: H3–H7)
Implement the digit evaluation checker.
*   **Objectives:** Extract marks columns, sum them up, and cross-check against overall written totals.
*   **Deliverables:**
    *   Digit OCR bounding box processor via local PaddleOCR.
    *   Math summation validation engine handling fractions, strikeouts, and blanks.
    *   Ambiguity flagging trigger system for grader overrides.

### M2: CopyCatch Collusion Engine (Target: H7–H14)
Create the semantic plagiarism check and graph network.
*   **Objectives:** Extract handwritten prose, calculate cosine similarity networks, and surface anomaly rankings.
*   **Deliverables:**
    *   Prose OCR engine utilizing confidence-weighted token extraction.
    *   Embedding generation module utilizing local `all-MiniLM-L6-v2`.
    *   Z-score statistical normalizer to filter class-wide identical answers (e.g., standard formulas).
    *   Interactive collusion node graph generated via NetworkX and PyVis.

### M3: Administrative Automation Helpers (Target: H14–H16)
Implement identity validation and borderline reviews.
*   **Objectives:** Automate register matching and borderline grade checks.
*   **Deliverables:**
    *   **ScriptID:** Digit OCR parser for roll number boxes, cross-checked against pandas-loaded student registration register CSV files.
    *   **ReEval Guard:** Grade-range evaluation lookup flagging border scores (e.g., 39 marks when passing score is 40).

### M4: Unified Streamlit Review Dashboard (Target: H16–H19)
Wire all pipelines and engines into a single desktop interface.
*   **Objectives:** Combine ingestion logs, collusion networks, totaled discrepancies, and flag reviews in one dashboard.
*   **Deliverables:**
    *   FastAPI backend routing results from SQLite to Streamlit.
    *   Streamlit-based tabbed interface displaying: Ingestion, MarkSafe audit, CopyCatch Network, ScriptID alerts, and Borderline list.
    *   Evidence crop visualizer showing side-by-side original image comparisons.

### M5: Stretch Features Integration (Target: H19–H21)
Integrate secondary modules if time permits.
*   **Objectives:** Implement page triage check and rubric-matching.
*   **Deliverables:**
    *   **BlankCheck:** OpenCV-based page-count and ink-presence validation.
    *   **RubricLens:** Cross-encoder/NLI deberta model matching answers to evaluation rubrics (color-coded evidence highlights).

### M6: Validation, Hardening & Demo Prep (Target: H21–H24)
Harden application and verify on test corpus.
*   **Objectives:** Verify the application on the 35-sheet corpus and construct fallback materials.
*   **Deliverables:**
    *   Verification runs on volunteer scripts to flag planted errors.
    *   Fallback demonstration video showing end-to-end functionality.
    *   Development freeze and configuration clean-ups.

---

## 3. Related Documents

*   [Implementation Action Items](file:///Users/gaurav/Desktop/MyProjects/E-Shield/implementation_plan.md)
*   [Core Ingestion Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/ingestion/README.md)
*   [CopyCatch Design Doc](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [MarkSafe Design Doc](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/MARKSAFE.md)
