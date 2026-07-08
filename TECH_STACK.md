# ExamShield v2 — Tech Stack

**Track:** 03 — Computer Vision | **Format:** 24-hour hackathon

Guiding rule for every pick: **boring, offline, pip-installable in one shot.** Nothing that needs a GPU cluster, a paid API, or venue Wi-Fi to run. Download and test every model **before** the event.

---

## 🧱 Stack at a Glance

| Layer | Choice | Used by |
|-------|--------|---------|
| Language | **Python 3.11** | Everything |
| Image preprocessing | **OpenCV** (`opencv-python`) | Pipeline spine, BlankCheck |
| Digit OCR (robust) | **PaddleOCR** (fallback: Tesseract) | MarkSafe, ScriptID, ReEval Guard |
| Prose OCR (fuzzy) | **PaddleOCR** with confidence scores (option: TrOCR handwritten) | CopyCatch, RubricLens |
| Embeddings | **sentence-transformers** — `all-MiniLM-L6-v2` | CopyCatch |
| NLI cross-encoder | **cross-encoder/nli-deberta-v3-xsmall** | RubricLens (stretch) |
| Similarity / stats | **NumPy + scikit-learn** (cosine sim, z-score baseline) | CopyCatch |
| Collusion graph | **NetworkX** (compute) + **PyVis / vis.js** (interactive render) | CopyCatch |
| Backend API | **FastAPI + Uvicorn** | Dashboard ↔ pipeline |
| Dashboard UI | **Streamlit** (fastest) — Plan B: plain HTML + vis.js served by FastAPI | Review dashboard, demo |
| Zone calibration UI | **Streamlit** + `streamlit-drawable-canvas` (draw rectangles → template JSON) | One-time per sheet format |
| Data store | **SQLite + JSON files** — no server DB | Flags, templates, register |
| Register / seating input | **pandas** (CSV) | ScriptID, CopyCatch seating weights |
| Image evidence crops | **Pillow** | Every feature's Tier-2 evidence view |
| PDF input handling | **pypdfium2** (PDF pages → images) | Ingestion |

---

## 🔍 Per-Feature Breakdown

### Pipeline spine (H0–H3)
- **OpenCV:** deskew (Hough / minAreaRect), denoise, adaptive-threshold binarize
- **pypdfium2:** if scripts arrive as PDFs, rasterize to PNG at ~300 DPI
- **Template JSON:** calibrated zones (marks column, total box, roll-no box, answer regions) saved per institution format, drawn once via `streamlit-drawable-canvas`

### MarkSafe (H3–H7)
- **PaddleOCR digit recognition** on calibrated zones only (never full-page)
- Pure-Python safe parser: integers, decimals, evaluable `a+b`; anything else → `AMBIGUOUS — human review`
- **OpenCV ink-presence:** pixel-density threshold in answer region vs empty marks cell

### CopyCatch (H7–H14)
- **PaddleOCR prose mode** with per-token confidence → drop low-confidence spans
- **all-MiniLM-L6-v2** embeddings (fast on CPU, ~80 MB) → cosine similarity matrix (~600 pairs at 35 scripts — milliseconds)
- **NumPy z-score anomaly ranking** against class baseline (class-wide shared mistakes auto-discounted)
- **NetworkX** cluster detection → **PyVis** interactive graph in the dashboard
- **Pillow** side-by-side image crops for Tier-2 human confirmation

### ReEval Guard (H14–H15)
- Zero new dependencies — pure Python over MarkSafe's extracted totals + a boundaries config (pass marks, grade cutoffs)

### ScriptID (H15–H16)
- Same PaddleOCR digit pipeline on the roll-number zone
- **pandas** join against register CSV → duplicates, absentees-with-sheets, present-without-sheets

### BlankCheck (H19–H21, if time)
- Page count per script (file/page enumeration) + OpenCV ink-presence per answer region — no OCR at all

### RubricLens (H19–H21, stretch)
- MiniLM retrieval to locate candidate regions per rubric point
- **nli-deberta-v3-xsmall** entailment/contradiction per point — entailed = green highlight, contradiction = red, uncertain = no highlight, **never a mark**

---

## 📦 One-Shot Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install opencv-python paddleocr paddlepaddle \
    sentence-transformers scikit-learn numpy pandas \
    fastapi uvicorn streamlit streamlit-drawable-canvas \
    networkx pyvis pillow pypdfium2
```

**Pre-event model warm-up (run once with internet, models cache locally):**

```python
from paddleocr import PaddleOCR
from sentence_transformers import SentenceTransformer, CrossEncoder
PaddleOCR(use_angle_cls=True, lang="en")                      # OCR weights
SentenceTransformer("all-MiniLM-L6-v2")                       # embeddings
CrossEncoder("cross-encoder/nli-deberta-v3-xsmall")           # NLI (stretch)
```

---

## 🗂️ Suggested Repo Layout

```
E-Shield/
├── app/
│   ├── pipeline/          # ingest.py, preprocess.py, calibrate.py, ocr.py
│   ├── features/          # marksafe.py, copycatch.py, reeval_guard.py,
│   │                      # scriptid.py, blankcheck.py, rubriclens.py
│   ├── api.py             # FastAPI endpoints
│   └── dashboard.py       # Streamlit review dashboard
├── data/
│   ├── corpus/            # 30–40 volunteer scripts (pre-event)
│   ├── templates/         # calibrated zone JSONs
│   └── register.csv       # class register with planted errors
├── ExamShield_Workflow.md
└── TECH_STACK.md
```

---

## ⚖️ Deliberate Choices (judge-Q&A ready)

- **PaddleOCR over cloud OCR APIs** — offline, free, per-token confidence scores (needed for confidence-weighted matching), no venue-Wi-Fi risk.
- **MiniLM over an LLM** — CopyCatch needs *relative* similarity ranking, not comprehension; a 80 MB CPU model does 600 pairs instantly and is fully explainable to judges.
- **NLI cross-encoder over cosine similarity for RubricLens** — solves the negation problem ("is not exothermic" → contradiction, shown red).
- **Streamlit over React** — dashboard in hours, not days; the demo is the graph and the evidence crops, not the CSS.
- **SQLite/JSON over Postgres** — nothing to install at the venue, trivially portable between laptops.
- **No fine-tuning anywhere** — nothing is fitted on 30 samples, so nothing overfits; matches the "deterministic retrieval + NLI, no trained scorer" claim in the idea doc.
