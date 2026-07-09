# Exam Processing Lifecycle
> Step-by-step workflow tracking physical answer booklet transitions, pipeline events, and state changes.

*Design / Planned — Not yet implemented*

---

## 1. Step-by-Step Lifecycle Workflow

The processing lifecycle coordinates physical exam booklets and digital database records through six sequential stages:

```
[ Step 1: Scan Booklets ] ──► [ Step 2: Binarize & Deskew ] ──► [ Step 3: Calibrate Zones ]
                                                                        │
                                                                        ▼
[ Step 6: Export Grades ] ◄── [ Step 5: Human Resolution ] ◄── [ Step 4: Run OCR Engines ]
```

---

## 2. Lifecycle Stages

### Step 1: Scanning & Ingestion
*   **Physical Action:** The student booklet is collected and scanned by exam-cell staff.
*   **System Action:** The system rasterizes the scanned PDF into page images at **300 DPI**, saves files to local storage, and initializes a batch run in SQLite.

### Step 2: Pre-processing & Alignment
*   **Physical Action:** None.
*   **System Action:** OpenCV deskews text layout lines, filters paper grain noise, and binarizes the images using adaptive Gaussian thresholding. BlankCheck counts pages to flag missing inserts.

### Step 3: Zone Calibration
*   **Physical Action:** The administrator selects or creates a bounding-box template for the booklet format.
*   **System Action:** The system crops the images into separate digit grids, roll number boxes, and answer prose zones.

### Step 4: OCR & Engine Analysis
*   **Physical Action:** None.
*   **System Action:**
    *   **Tier-1 OCR** reads the roll number and marks table digits, saving scores to SQLite.
    *   **Tier-2 OCR** extracts answer text, vectorizes it, and calculates collusion graph connections.
    *   **Engine checks** run and raise pending audit flags for mismatches or duplicate IDs.

### Step 5: Manual Flag Resolution
*   **Physical Action:** Graders and auditors review flagged scripts in the dashboard.
*   **System Action:** Graders update values next to visual crops. User confirmations update flag statuses to `RESOLVED` and write finalized scores to SQLite.

### Step 6: Grade Export & Archiving
*   **Physical Action:** The CoE finalizes results.
*   **System Action:** The system updates the batch status to `completed`, generates finalized grade lists, exports results to a CSV file, and archives the batch.

---

## 3. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [In-Depth Architecture Spec](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ARCHITECTURE.md)
*   [Product Features List](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FEATURES.md)
