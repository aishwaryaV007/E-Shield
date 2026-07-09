# Ingestion Pipeline Plan
> Development steps, tasks, image pre-processing configurations, and calibration dashboard roadmaps.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

The **Ingestion Pipeline** forms the backbone of ExamShield. It processes raw scanned documents and prepares them for OCR extraction and engine evaluation.

```
[ Raw Scans Uploaded ] 
         │ 
         ▼ (Task 1: PDF to PNG Rasterization)
[ Rasterized Page Images ] 
         │ 
         ▼ (Task 2: OpenCV Deskew & Denoise Filters)
[ Pre-processed Binarized Matrices ] 
         │ 
         ▼ (Task 3: Calibration GUI template mapping)
[ JSON Template coordinates mapping ] 
```

---

## 2. Technical Task Breakdown

### Task 1: Document Rasterization (`app/ingestion/loader.py`)
*   **Objectives:** Convert multi-page scanned booklets (PDF format) into separate image arrays.
*   **Implementation Steps:**
    1.  Use `pypdfium2` to read PDFs offline.
    2.  Rasterize pages to PNG format at a target resolution of **`300 DPI`**.
    3.  Save files to the local temp path `/data/temp/{batch_id}/{script_id}/`.

### Task 2: OpenCV Image Preprocessing (`app/ingestion/preprocess.py`)
*   **Objectives:** Clean, align, and binarize images to improve OCR accuracy.
*   **Implementation Steps:**
    1.  **Denoising:** Apply a bilateral filter (`cv2.bilateralFilter`) to smooth background paper grain while preserving handwriting edges.
    2.  **Deskewing:** Calculate the skew angle of the text using Hough Line Transform, rotating the image via affine transformation when necessary.
    3.  **Adaptive Binarization:** Convert pages to high-contrast binary formats (0 or 255) using Gaussian adaptive thresholding.

### Task 3: Streamlit Alignment GUI (`app/calibration/canvas.py`)
*   **Objectives:** Provide administrators with a visual canvas tool to define coordinates for various answer sheet layouts.
*   **Implementation Steps:**
    1.  Embed the `streamlit-drawable-canvas` widget.
    2.  Map bounding boxes for roll numbers, marks columns, overall totals, and answer fields on a reference page image.
    3.  Convert the pixel coordinates to relative ratios `(x/W, y/H, w/W, h/H)` and save them to a reusable layout template JSON file.

---

## 3. Related Documents

*   [Ingestion Module specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/ingestion/README.md)
*   [OCR Development Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/OCR_PLAN.md)
*   [Local Performance & Scalability Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
