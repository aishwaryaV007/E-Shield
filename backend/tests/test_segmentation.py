import pytest
import numpy as np
from app.segmentation.question_segmenter import QuestionSegmenter, AnswerBlock
from app.segmentation.answer_matcher import AnswerMatcher

def test_question_segmenter_basic():
    segmenter = QuestionSegmenter()
    
    # Mock preprocessed page (1000 height, 800 width)
    mock_page = np.ones((1000, 800), dtype=np.uint8) * 255
    
    # Mock OCR results
    ocr_results = [
        {
            "page_index": 0,
            "tokens": [
                {"text": "Q21", "bbox": [50, 100, 100, 120]},
                {"text": "Q22", "bbox": [50, 600, 100, 620]}
            ]
        }
    ]
    
    blocks = segmenter.segment([mock_page], ocr_results)
    assert len(blocks) == 2
    
    # First block should be Q21 starting at 100, ending at 600 (y_min of Q22)
    assert blocks[0].question_no == "Q21"
    assert blocks[0].bbox == [0, 100, 800, 600]
    assert blocks[0].image_crop.shape == (500, 800)  # height: 600-100 = 500
    
    # Second block should be Q22 starting at 600, ending at page bottom 1000
    assert blocks[1].question_no == "Q22"
    assert blocks[1].bbox == [0, 600, 800, 1000]
    assert blocks[1].image_crop.shape == (400, 800)  # height: 1000-600 = 400

def test_question_segmenter_continuation():
    segmenter = QuestionSegmenter()
    
    # Mock two preprocessed pages (1000 height, 800 width)
    mock_page_1 = np.ones((1000, 800), dtype=np.uint8) * 255
    mock_page_2 = np.ones((1000, 800), dtype=np.uint8) * 255
    
    # Q21 starts on page 1, page 2 has no headers (continuation)
    ocr_results = [
        {
            "page_index": 0,
            "tokens": [
                {"text": "Q21", "bbox": [50, 400, 100, 420]}
            ]
        },
        {
            "page_index": 1,
            "tokens": []  # No headers
        }
    ]
    
    blocks = segmenter.segment([mock_page_1, mock_page_2], ocr_results)
    # We should have two crops for Q21: one on page 1, one on page 2
    assert len(blocks) == 2
    
    assert blocks[0].question_no == "Q21"
    assert blocks[0].page_index == 0
    assert blocks[0].bbox == [0, 400, 800, 1000]
    
    assert blocks[1].question_no == "Q21"
    assert blocks[1].page_index == 1
    assert blocks[1].bbox == [0, 0, 800, 1000]

def test_answer_matcher():
    matcher = AnswerMatcher()
    
    # Mock crops
    crop_1 = np.zeros((100, 100))
    crop_2 = np.ones((200, 100))
    
    # Two answer blocks, both matching Q21 (e.g. from page 1 and page 2)
    blocks = [
        AnswerBlock(question_no="Q21", page_index=0, bbox=[0, 0, 100, 100], image_crop=crop_1),
        AnswerBlock(question_no="q21", page_index=1, bbox=[0, 0, 100, 200], image_crop=crop_2)
    ]
    
    # Question description list
    questions = [
        {
            "id": 101,
            "question_no": "21",
            "key_text": "Ground truth description",
            "rubric_json": "[]",
            "max_marks": 2.0
        }
    ]
    
    grading_units = matcher.match(blocks, questions)
    assert len(grading_units) == 1
    
    unit = grading_units[0]
    assert unit["question_id"] == 101
    assert unit["question_no"] == "21"
    assert len(unit["image_crops"]) == 2
    assert unit["page_indices"] == [0, 1]
    assert unit["max_marks"] == 2.0
