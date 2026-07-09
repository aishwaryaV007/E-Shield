# ExamShield Scalability Specification
> Local CPU performance optimizations, memory profiles, processing run times, and $O(N^2)$ scaling limits.

*Design / Planned — Not yet implemented*

---

## 1. Local Resource Scale Model

ExamShield runs entirely on the host machine. Scale optimizations focus on managing CPU execution and memory usage on standard laptops rather than scaling across multi-node cloud clusters.

```
┌────────────────────────────────────────────────────────┐
│ Scanned Input Batch (N answer scripts)                 │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ CPU Ingestion Spine (OpenCV thread pool execution)     │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ Local OCR Pipeline (Sequential CPU Inference)          │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ Pairwise Similarity Math (O(N^2) NumPy Tensor Calc)    │
└────────────────────────────────────────────────────────┘
```

---

## 2. Execution Run Times & Resource Targets

The system is optimized for a target batch size of **$N=300$ scripts** (averaging 5 pages per booklet) running on a standard 4-core CPU with 8 GB of RAM:

| Pipeline Stage | Algorithmic Complexity | Bottleneck Factor | Est. Time ($N=35$) | Est. Time ($N=300$) | Optimization Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ingestion** | $O(N \cdot P)$ | Disk I/O & PDF Rasterization. | ~15 seconds | ~2.5 minutes | OpenCV multithreading; low-overhead binarization. |
| **Digit OCR** | $O(N)$ | Neural Network CPU Inference. | ~45 seconds | ~6.5 minutes | Crop and scan only calibrated zones; ignore background text. |
| **Prose OCR** | $O(N \cdot P_{text})$ | Neural Network CPU Inference. | ~90 seconds | ~13 minutes | Scale down input resolution and filter out blank answer fields. |
| **CopyCatch Math** | $O(N^2)$ | Tensor dot products. | < 0.1 seconds | ~1.5 seconds | Vectorize matrix calculations using NumPy; bypass Python loops. |

---

## 3. Algorithmic Optimization & Bottleneck Remediation

### 1. Managing $O(N^2)$ Pairwise Comparisons
For a batch of $N=300$ scripts, the engine performs $\frac{300 \times 299}{2} = 44,850$ similarity checks. 
*   **Bypassing Python Loops:** Running these checks in standard Python loops causes noticeable UI lag. Instead, ExamShield stacks all MiniLM text embedding vectors into a single NumPy array of shape `(300, 384)` and calculates the cosine similarity matrix in one step using optimized tensor operations:
    ```python
    # Planned implementation pattern
    import numpy as np

    def calculate_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
        # Normalize vectors to unit length
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = embeddings / norms
        # Compute dot product matrix in one step
        return np.dot(normalized, normalized.T)
    ```

### 2. Reducing OCR Compute Loads
Running OCR scans across whole pages is slow. The calibration engine limits OCR processing to specific coordinate bounding boxes (e.g., marks boxes, roll number grids, and answer blocks), reducing the scanned surface area by up to **80%**.

### 3. Memory Profile & Footprint Management
*   **Image Discarding:** High-resolution page matrices are discarded from memory immediately after pre-processing and coordinate cropping.
*   **Model Lifecycles:** OCR and embedding pipelines share model weights in memory instead of spinning up independent instances, keeping the overall RAM footprint under **600 MB**.

---

## 4. Related Documents

*   [System Design Subsystems](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [CopyCatch Algorithmic Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [Database Optimization Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
