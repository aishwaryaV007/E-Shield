#!/usr/bin/env python3
import os
import sys

# 1. FILE PURPOSE: Pre-fetches the required ML model weights to the local models_cache/ directory
#    so the pipeline runs fully offline at the venue with no Wi-Fi dependency.
# 2. RESPONSIBILITIES:
#    - Download a handwriting OCR model (TrOCR handwritten) weights.
#    - Download sentence-transformers all-MiniLM-L6-v2.
#    - Download Teklia/RIMES-2011-line dataset.
#    - Verify each model loads successfully and report the cache path.

def download_models():
    print("Starting download of required ML models and datasets...")
    
    # Configure custom cache dir (resolve relative to script or use env var)
    default_cache = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models_cache"))
    cache_dir = os.environ.get("MODEL_DIR", default_cache)
    os.makedirs(cache_dir, exist_ok=True)
    print(f"Using cache directory: {cache_dir}")
    
    # 1. sentence-transformers/all-MiniLM-L6-v2
    try:
        print("\n1. Downloading sentence-transformers (all-MiniLM-L6-v2)...")
        from sentence_transformers import SentenceTransformer
        _ = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", cache_folder=cache_dir)
        print("✓ Sentence-transformer downloaded and cached successfully.")
    except Exception as e:
        print(f"✗ Failed to download sentence-transformers: {e}")
        
    # 2. TrOCR Handwritten
    try:
        print("\n2. Downloading TrOCR processor and model (microsoft/trocr-base-handwritten)...")
        from transformers import VisionEncoderDecoderModel, TrOCRProcessor
        _ = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten", cache_dir=cache_dir)
        _ = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten", cache_dir=cache_dir)
        print("✓ TrOCR model downloaded and cached successfully.")
    except Exception as e:
        print(f"✗ Failed to download TrOCR model: {e}")

    # 3. Teklia/RIMES-2011-line dataset
    try:
        print("\n3. Downloading dataset (Teklia/RIMES-2011-line)...")
        from datasets import load_dataset
        _ = load_dataset("Teklia/RIMES-2011-line", cache_dir=cache_dir)
        print("✓ Dataset Teklia/RIMES-2011-line downloaded and cached successfully.")
    except Exception as e:
        print(f"✗ Failed to download dataset: {e}")

if __name__ == "__main__":
    download_models()
