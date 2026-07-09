# Product Roadmap
> Development timeline, target releases (v1.0 to v3.0), and future online extension plans.

*Design / Planned — Not yet implemented*

---

## 1. Release Timeline

The development roadmap is structured into three phases, expanding the core offline evaluation features before exploring online integrations:

```
[ Phase 1: Core Offline MVP (v1.0) ] ──► [ Phase 2: Administrative Addons (v2.0) ] ──► [ Phase 3: Future Online Extensions (v3.0) ]
```

---

## 2. Release Phases

### Phase 1: Core Offline MVP (v1.0)
*   **Objectives:** Deliver the baseline image processing pipeline, digit auditing capabilities, and handwriting similarity graphs.
*   **Key Features:**
    *   Binarization, deskewing, and coordinate alignment canvas templates.
    *   **MarkSafe:** Validates page score totals.
    *   **CopyCatch:** Identifies similarity clusters using local `all-MiniLM-L6-v2` embeddings.
    *   Streamlit review dashboard displaying ranked audit flags.

### Phase 2: Administrative Automation Addons (v2.0)
*   **Objectives:** Automate student roster validation and borderline grading audits.
*   **Key Features:**
    *   **ScriptID:** Matches roll numbers against student registers.
    *   **ReEval Guard:** Prioritizes borderline grades for review.
    *   **BlankCheck:** Automates page counting and page triage checks.
    *   **RubricLens:** Matches student answers against rubrics using DeBERTa models.
    *   Supports batch export of corrected grades to CSV.

### Phase 3: Future Online Extensions (v3.0)
*   **Objectives:** Connect ExamShield's offline engine with online testing portals.
*   **Key Features:**
    *   **Secure Web-Exam Portal:** Enables digital exam delivery on personal devices.
    *   **Integrated Secure Browser Client:** Implements browser lockdowns, disables keyboard shortcuts, and blocks copy-paste functions during exams.
    *   **Automated Online Proctoring Subsystem:** Uses webcam video streams and audio analysis to flag suspicious student behavior.
    *   **Unified Dashboard:** Displays collusion graphs for both offline handwritten scripts and online submissions.

---

## 3. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Future Implementation Tasks](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FUTURE_IMPLEMENTATION_TASKS.md)
*   [Product Features List](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FEATURES.md)
