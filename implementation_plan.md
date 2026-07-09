# ExamShield Detailed Implementation Plan
> Granular task breakdown, target code locations, verification checks, and current status for each developmental milestone.

*Design / Planned — Not yet implemented*

---

## 1. Milestone M0: Core Ingestion Spine

### Tasks & File Allocations
- [ ] Create Python virtual environment and install primary dependencies (`requirements.txt`).
- [ ] Implement image load utility handles rasterizing PDF files using `pypdfium2`.
  *   *File:* `app/ingestion/loader.py`
- [ ] Code image preprocessing pipeline using OpenCV for binarization, deskewing, and noise reduction.
  *   *File:* `app/ingestion/preprocess.py`
- [ ] Write Streamlit coordinate calibration canvas dashboard.
  *   *File:* `app/calibration/canvas.py`
- [ ] Establish JSON template storage model to load coordinate boundaries for marks tables, roll numbers, and answer text boxes.
  *   *File:* `app/storage/templates.py`

### M0 Verification Checks
*   Verify image preprocessing successfully aligns skewed input pages.
*   Verify Canvas UI outputs correct rectangle coordinate bounds `(x, y, w, h)` to a local `.json` file.

---

## 2. Milestone M1: MarkSafe Verification Engine

### Tasks & File Allocations
- [ ] Initialize local CPU instance of PaddleOCR digit recognition pipeline.
  *   *File:* `app/ocr/digit_ocr.py`
- [ ] Implement target OCR crop extractor using calibrated coordinate rectangles.
  *   *File:* `app/ocr/crop_extractor.py`
- [ ] Write MarkSafe arithmetic engine checking parsed values (e.g., decimals, integers, `a+b` sub-marks) against the written total box.
  *   *File:* `app/engines/marksafe.py`
- [ ] Design regex parse rules identifying strikeouts, empty boxes, or overwritten digits, routing them to the manual audit flag.
  *   *File:* `app/engines/helpers.py`

### M1 Verification Checks
*   Verify digit extraction scores high accuracy on clear mock grading boxes.
*   Confirm summation anomalies trigger mismatch flags and prevent false automatic correction.

---

## 3. Milestone M2: CopyCatch Collusion Engine

### Tasks & File Allocations
- [ ] Build prose-oriented OCR pipeline extracting multi-paragraph handwritten answers with confidence thresholds.
  *   *File:* `app/ocr/prose_ocr.py`
- [ ] Integrate local sentence transformer `all-MiniLM-L6-v2` to vectorize prose OCR outputs.
  *   *File:* `app/engines/embeddings.py`
- [ ] Write pairwise similarity engine using cosine similarity math.
  *   *File:* `app/engines/copycatch.py`
- [ ] Write class-wide anomaly z-score filter. It automatically discounts identical answers caused by matching classroom slides or syllabus formulas.
  *   *File:* `app/engines/anomaly.py`
- [ ] Implement graph network mapper using NetworkX and export it as an interactive HTML document via PyVis.
  *   *File:* `app/engines/graph.py`

### M2 Verification Checks
*   Confirm pairwise comparisons run within seconds for a batch of 35 files.
*   Verify the NetworkX/PyVis HTML rendering accurately plots student pairs exceeding the similarity threshold.

---

## 4. Milestone M3: Administrative Helpers

### Tasks & File Allocations
- [ ] Implement ScriptID roster validator cross-referencing OCR-parsed roll numbers against the class CSV register.
  *   *File:* `app/engines/scriptid.py`
- [ ] Write ReEval Guard queue classifier. It filters scripts with final marks within borderline proximity of pass boundaries (e.g., scoring 39 when pass limit is 40).
  *   *File:* `app/engines/reeval_guard.py`

### M3 Verification Checks
*   Verify ScriptID correctly flags roll numbers missing from the CSV register or duplicated across pages.
*   Verify ReEval Guard flags and groups scripts meeting the border threshold configuration.

---

## 5. Milestone M4: Unified Streamlit Dashboard

### Tasks & File Allocations
- [ ] Set up FastAPI routes delivering parsed SQLite data.
  *   *File:* `app/api.py`
- [ ] Build the Streamlit dashboard tabs structure.
  *   *File:* `app/dashboard/main.py`
- [ ] Design side-by-side verification crop viewer within the Streamlit UI.
  *   *File:* `app/dashboard/views.py`

### M4 Verification Checks
*   Ensure the local dashboard loads and runs on a standard web browser at `localhost:8501`.
*   Confirm visual crops display correct images corresponding to highlighted discrepancies.

---

## 6. Milestone M5: Stretch Features

### Tasks & File Allocations
- [ ] Implement BlankCheck: pixel-density scans checking for attempted pages.
  *   *File:* `app/engines/blankcheck.py`
- [ ] Set up RubricLens: loads local NLI deberta cross-encoder and outputs green/red markup overlays on candidate text.
  *   *File:* `app/engines/rubriclens.py`

### M5 Verification Checks
*   Verify BlankCheck correctly marks entirely blank answer sheets.
*   Verify RubricLens generates color-coded highlights matching rubric directives.

---

## 7. Milestone M6: Validation & Hardening

### Tasks & File Allocations
- [ ] Perform integration runs on the 35 volunteer scripts.
  *   *File:* `app/test_runner.py`
- [ ] Resolve memory leaks in local OCR initialization and SQLite transaction writes.
- [ ] Clean temporary files and write scripts for demo execution backups.

### M6 Verification Checks
*   Ensure zero crash loops occur during consecutive batch processing.
*   Confirm final SQLite records match input volunteer metrics exactly.

---

## 8. Related Documents

*   [Overall Build Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/plan.md)
*   [Database Design Document](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [API Schema Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)
