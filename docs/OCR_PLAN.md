# OCR Subsystem Development Plan
> Development steps, tasks, local PaddleOCR engine setups, and confidence score parser targets.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

The **OCR Subsystem** digitizes image regions cropped from the ingestion pipeline. It maps pixel coordinates to structured data, separating digits from handwritten prose text.

```
                  ┌──────────────────────────────┐
                  │ Crop Bounding Box Image      │
                  └──────────────┬───────────────┘
                                 │
                  ┌──────────────▼───────────────┐
                  │ Initialize local PaddleOCR   │
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
        [ Task 1: Digit OCR ]           [ Task 2: Prose OCR ]
        • whitelist: 0-9/.+             • full lexicon model
        • limit: marks grid/ID          • limit: answer boxes
                 │                               │
                 ▼                               ▼
        [ Save digits/confidence ]      [ Token confidence filtering ]
```

---

## 2. Technical Task Breakdown

### Task 1: Digit-Specific OCR (`app/ocr/digit_ocr.py`)
*   **Objectives:** Extract numbers from marks columns, overall total boxes, and roll number fields.
*   **Implementation Steps:**
    1.  Initialize local PaddleOCR with numeric-only configurations.
    2.  Implement regex filters to clean extracted text and remove non-digit characters (e.g., converting `O` to `0` or `I` to `1` when reading IDs).
    3.  Set the confidence cutoff to **`0.85`**. If the extraction confidence falls below this value, write `NULL` to SQLite and flag the zone as `AMBIGUOUS_MARK`.

### Task 2: Prose-Specific OCR (`app/ocr/prose_ocr.py`)
*   **Objectives:** Extract text paragraphs from handwritten answer areas for semantic similarity matching.
*   **Implementation Steps:**
    1.  Initialize PaddleOCR with English prose recognition weights.
    2.  Filter extracted text: keep words with confidence scores above **`0.65`** to reduce noise.
    3.  Strip punctuation and common stop words (e.g., *"and"*, *"the"*, *"is"*) to optimize vector embeddings downstream.

### Task 3: Visual Crop Manager (`app/ocr/crop_extractor.py`)
*   **Objectives:** Crop target regions from page image matrices using normalized coordinate values.
*   **Implementation Steps:**
    1.  Load the preprocessed page image.
    2.  Convert relative ratios from JSON templates into actual pixel coordinates:
        $$\text{Pixel}_x = \text{Ratio}_x \times W_{\text{image}}$$
    3.  Save the cropped image to disk as a JPEG, which the dashboard uses to display visual evidence alongside audit flags.

---

## 3. Related Documents

*   [OCR Subsystem Module specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/ocr/README.md)
*   [Ingestion Pipeline Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/PIPELINE_PLAN.md)
*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
