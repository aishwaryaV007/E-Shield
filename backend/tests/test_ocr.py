import pytest
import numpy as np
from app.ocr.handwriting_ocr import HandwritingOCR
from app.ocr.confidence import answer_confidence, needs_human_check

def test_ocr_initialization():
    ocr = HandwritingOCR()
    assert ocr is not None
    assert ocr.model is not None
    assert ocr.processor is not None

def test_ocr_inference_on_blank():
    ocr = HandwritingOCR()
    # Create a simple blank white image representing an empty region
    blank_img = np.ones((100, 300, 3), dtype=np.uint8) * 255
    
    result = ocr.recognize_text(blank_img)
    assert isinstance(result, dict)
    assert "text" in result
    assert "confidences" in result
    assert isinstance(result["text"], str)
    assert isinstance(result["confidences"], list)

def test_confidence_scoring():
    # An empty confidence list (e.g. blank answer) defaults to 1.0
    assert answer_confidence([]) == 1.0
    
    # Verify mean calculation
    conf_scores = [0.9, 0.8, 0.7]
    assert abs(answer_confidence(conf_scores) - 0.8) < 1e-5
    
    # Verify low confidence trigger
    assert needs_human_check(0.75, threshold=0.8) is True
    assert needs_human_check(0.85, threshold=0.8) is False
