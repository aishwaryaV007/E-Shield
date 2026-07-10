import re
import numpy as np

class AnswerBlock:
    """
    Represents a cropped horizontal slice of a page image containing a student's answer
    to a specific question.
    """
    def __init__(self, question_no: str, page_index: int, bbox: list[int], image_crop: np.ndarray):
        self.question_no = question_no
        self.page_index = page_index
        self.bbox = bbox  # [x_min, y_min, x_max, y_max]
        self.image_crop = image_crop

class QuestionSegmenter:
    """
    Segments page images into question-wise AnswerBlocks by identifying question headers
    from OCR token text and coordinates, then slicing the page horizontally.
    """
    def __init__(self):
        # Matches patterns like Q21, Q.22, Question 23, Q 24, etc.
        self.header_pattern = re.compile(r'^(?:q(?:uestion)?[\s\.]*)(\d+)$', re.IGNORECASE)

    def segment(self, pages: list[np.ndarray], ocr_results: list[dict]) -> list[AnswerBlock]:
        """
        Segments the list of page images based on layout OCR tokens.
        
        Args:
            pages: List of preprocessed page images (numpy arrays).
            ocr_results: List of dicts matching:
                [
                    {
                        "page_index": 0,
                        "tokens": [
                            {"text": "Q21", "bbox": [100, 500, 150, 530]},
                            ...
                        ]
                    },
                    ...
                ]
                
        Returns:
            A list of AnswerBlock instances.
        """
        answer_blocks = []
        current_question_no = None
        
        # Build map from page_index to tokens for quick lookup
        page_tokens_map = {item["page_index"]: item["tokens"] for item in ocr_results}
        
        for page_idx, page in enumerate(pages):
            H, W = page.shape[:2]
            tokens = page_tokens_map.get(page_idx, [])
            
            # Find all tokens matching question headers
            detected_headers = []
            for token in tokens:
                text = token["text"].strip()
                match = self.header_pattern.match(text)
                if match:
                    q_num = match.group(1)
                    detected_headers.append({
                        "question_no": f"Q{q_num}",
                        "bbox": token["bbox"]  # [x_min, y_min, x_max, y_max]
                    })
                    
            # Sort headers vertically by their y_min coordinate
            detected_headers.sort(key=lambda h: h["bbox"][1])
            
            if not detected_headers:
                # No new question headers on this page: it's a continuation of the active question
                if current_question_no is not None:
                    # Crop the entire page
                    crop = page.copy()
                    block = AnswerBlock(
                        question_no=current_question_no,
                        page_index=page_idx,
                        bbox=[0, 0, W, H],
                        image_crop=crop
                    )
                    answer_blocks.append(block)
                continue
                
            # If there's a segment at the top of the page before the first header,
            # it belongs to the previous question
            first_header_y = detected_headers[0]["bbox"][1]
            if first_header_y > 50 and current_question_no is not None:
                # Slices from top of page to the first header
                crop = page[0:first_header_y, :].copy()
                block = AnswerBlock(
                    question_no=current_question_no,
                    page_index=page_idx,
                    bbox=[0, 0, W, first_header_y],
                    image_crop=crop
                )
                answer_blocks.append(block)
                
            # Now slice page between detected headers
            for i, header in enumerate(detected_headers):
                q_no = header["question_no"]
                current_question_no = q_no  # Update active question
                
                y_start = header["bbox"][1]
                
                # Determine y_end (starts of next header or page bottom)
                if i + 1 < len(detected_headers):
                    y_end = detected_headers[i + 1]["bbox"][1]
                else:
                    y_end = H
                    
                # Slice image
                crop = page[y_start:y_end, :].copy()
                block = AnswerBlock(
                    question_no=q_no,
                    page_index=page_idx,
                    bbox=[0, y_start, W, y_end],
                    image_crop=crop
                )
                answer_blocks.append(block)
                
        return answer_blocks
