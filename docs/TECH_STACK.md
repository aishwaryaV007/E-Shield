# ExamShield Tech Stack Reference
> Technical justifications, local model specifications, package dependencies, and offline initialization.

*Design / Planned — Not yet implemented*

---

## 1. Technical Frameworks

ExamShield is built using a local-only Python stack to ensure compatibility with standard university computers:

| Layer | Technology | Version | Purpose & Selection Justification |
| :--- | :--- | :--- | :--- |
| **Language** | **Python** | 3.11+ | Provides broad support for ML libraries and file processing utilities. |
| **CV Pipeline** | **OpenCV** | 4.8+ | Used for binarization, deskewing, and BlankCheck page triage. |
| **Local OCR** | **PaddleOCR** | 2.7+ | Offers reliable offline OCR performance, providing layout matching and token confidence scores. |
| **Embeddings** | **Sentence Transformers** | 2.2+ | Loads local embedding models to evaluate handwriting similarity without API calls. |
| **NLI Classifier** | **Hugging Face Hub** | 4.30+ | Classifies semantic rubric alignments. |
| **App Server** | **FastAPI** | 0.100+ | Lightweight REST coordinator connecting backend pipelines and UI components. |
| **UI Dashboard** | **Streamlit** | 1.25+ | Enables fast UI rendering and visual canvas interactions without web framework overhead. |
| **Database** | **SQLite** | 3.x (std) | Serverless relational database for local records. |

---

## 2. Local AI/ML Models Specs

To run offline on standard CPUs, ExamShield uses lightweight, pre-trained models:

1.  **Text OCR Model:** `PaddleOCR` (English weights). This model runs text detection and classification locally using CNN-based backends.
2.  **Sentence Embeddings (CopyCatch):** `all-MiniLM-L6-v2`.
    *   *Parameters:* 22 Million
    *   *Model Size:* ~80 MB (cached locally)
    *   *Dimension:* 384-dimensional vector space
    *   *Justification:* Optimizes CPU performance, executing 600 pairwise comparisons in milliseconds.
3.  **Rubric Cross-Encoder (RubricLens):** `cross-encoder/nli-deberta-v3-xsmall`.
    *   *Model Size:* ~100 MB
    *   *Performance:* Resolves semantic negation issues (e.g., matching "is not correct" as a contradiction rather than a similarity).

---

## 3. Dependency Environment Installation

Install all required packages within a Python virtual environment:

```bash
# Initialize and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install opencv-python paddleocr paddlepaddle \
    sentence-transformers scikit-learn numpy pandas \
    fastapi uvicorn streamlit streamlit-drawable-canvas \
    networkx pyvis pillow pypdfium2
```

### Pre-downloading Model Weights
To ensure offline compatibility, download and cache model weights before deploying in restricted exam-cell environments:

```python
# cache_models.py
from paddleocr import PaddleOCR
from sentence_transformers import SentenceTransformer, CrossEncoder

print("Caching PaddleOCR weights...")
PaddleOCR(use_angle_cls=True, lang="en")

print("Caching all-MiniLM-L6-v2 Embeddings...")
SentenceTransformer("all-MiniLM-L6-v2")

print("Caching DeBERTa Cross-Encoder...")
CrossEncoder("cross-encoder/nli-deberta-v3-xsmall")

print("All models successfully cached locally!")
```

---

## 4. Related Documents

*   [System Design Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Local Database Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DATABASE_DESIGN.md)
*   [Performance Scalability](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
