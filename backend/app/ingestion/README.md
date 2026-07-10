# Ingestion Module (Phase 2 input)

Turns uploaded answer scripts into clean page images for OCR.

- `pdf_loader.py` — rasterize PDF scripts to images (~300 DPI).
- `preprocess.py` — deskew, denoise, adaptive binarization.
