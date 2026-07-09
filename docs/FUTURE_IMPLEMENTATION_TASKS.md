# Future Implementation Backlog
> Developer guide, task queue, and upcoming optimizations.

*Design / Planned — Not yet implemented*

---

## 1. Developer Onboarding Guidelines

This document tracks upcoming feature implementations, optimizations, and bug fixes for ExamShield. 

When working on a new backlog task, please follow these guidelines:
1.  **Isolate in Branches:** Create a descriptive branch (e.g., `backlog/export-pdf-report`).
2.  **Maintain Offline Compatibility:** Ensure new features do not import cloud dependencies or require GPU resources.
3.  **Preserve Fallback Rules:** Ensure that any OCR parser adjustments preserve the `AMBIGUOUS` flag fallback pattern. Grader grades must never be auto-corrected or overwritten without explicit human authorization.

---

## 2. Active Backlog Queue

### 1. Ingestion Subsystem Optimization
- [ ] **Adaptive Binarization Tweak:** Improve binarization parameters to handle scans from phone cameras under varied lighting.
- [ ] **Multi-format Importer:** Support raw image files (HEIC, JPEG, PNG) directly alongside PDFs in the ingestion folder.

### 2. OCR Subsystem Enhancements
- [ ] **TrOCR Handwritten Model Integration:** Add an optional pipeline fallback to use the TrOCR handwritten model for low-confidence prose fields.
- [ ] **Interactive Bounding Box Refinement:** Allow users to adjust bounding box alignments directly in the calibration tab if a scan is misaligned.

### 3. Core Engine Tweaks
- [ ] **Seating Proximity Weighted Similarity:** Enhance the CopyCatch algorithm by adjusting similarity scores based on physical seating coordinates in the exam room.
- [ ] **Custom Grading Rubric Importer:** Build a parser in RubricLens to import rubrics directly from Excel sheets or PDF documents.

### 4. User Interface Improvements
- [ ] **Export Final Grades Report:** Support exporting finalized, audited scores directly to university grading systems via standardized XLS/CSV file formats.
- [ ] **Visual Audit History Logs:** Build a dashboard view showing changes made by auditors to resolve mismatch flags.

---

## 3. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Product Roadmap](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ROADMAP.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
