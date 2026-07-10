import os
import pytest
import numpy as np
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.preprocess import deskew_image, denoise_image, binarize_image, preprocess_image

# Path to the actual student script
SAMPLE_PDF_PATH = "/Users/gaurav/Desktop/MyProjects/E-Shield/dataset/raw_scripts/Student_Pdf/Student_1.pdf"

def test_pdf_loader_rasterize():
    # Verify that loading the sample PDF works
    assert os.path.exists(SAMPLE_PDF_PATH), f"Sample PDF not found at {SAMPLE_PDF_PATH}"
    
    # Rasterize at 72 DPI (low resolution for fast testing)
    images = PDFLoader.rasterize_pdf(SAMPLE_PDF_PATH, dpi=72)
    assert len(images) > 0
    assert isinstance(images[0], np.ndarray)
    # Check that image is 3D (BGR)
    assert len(images[0].shape) == 3
    assert images[0].shape[2] == 3

def test_pdf_loader_file_not_found():
    with pytest.raises(FileNotFoundError):
        PDFLoader.rasterize_pdf("non_existent_file.pdf")

def test_preprocessing_steps():
    # Create a dummy image (e.g. light gray square)
    dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 200
    # Draw some "strokes" in the middle
    dummy_img[30:70, 30:70] = 50 
    
    # Test deskew
    deskewed = deskew_image(dummy_img)
    assert deskewed.shape == dummy_img.shape
    
    # Test denoise
    denoised = denoise_image(dummy_img)
    assert denoised.shape == dummy_img.shape
    
    # Test binarize
    binarized = binarize_image(dummy_img)
    assert len(binarized.shape) == 2  # Grayscale binary image
    assert binarized.shape == (100, 100)
    
    # Test full preprocessing pipeline
    preprocessed = preprocess_image(dummy_img)
    assert len(preprocessed.shape) == 2
    assert preprocessed.shape == (100, 100)
