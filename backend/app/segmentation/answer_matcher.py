import re

class AnswerMatcher:
    """
    Groups segmented AnswerBlocks by question number (aggregating multi-page crops)
    and matches them to official answer keys/rubrics to produce unified GradingUnits.
    """
    def __init__(self):
        pass

    def _normalize_q_no(self, q_str: str) -> str:
        """
        Normalizes a question number string to digit format (e.g. 'Q21' -> '21', '21' -> '21').
        """
        if not q_str:
            return ""
        match = re.search(r'\d+', q_str)
        return match.group(0) if match else q_str.strip().lower()

    def match(self, answer_blocks: list, questions: list[dict]) -> list[dict]:
        """
        Groups multi-page AnswerBlocks by question and aligns them with database questions.
        
        Args:
            answer_blocks: List of AnswerBlock instances.
            questions: List of dictionaries matching the questions DB table schema:
                [
                    {
                        "id": 1,
                        "question_no": "Q21",
                        "key_text": "Sample answer key text...",
                        "rubric_json": "[...]",
                        "max_marks": 2.0
                    },
                    ...
                ]
                
        Returns:
            A list of dicts (GradingUnits) structured as:
                [
                    {
                        "question_id": 1,
                        "question_no": "Q21",
                        "image_crops": [crop1, crop2, ...],
                        "page_indices": [0, 1, ...],
                        "key_text": "...",
                        "rubric_json": "...",
                        "max_marks": 2.0
                    },
                    ...
                ]
        """
        # 1. Group blocks by normalized question number
        grouped_blocks = {}
        for block in answer_blocks:
            norm_q = self._normalize_q_no(block.question_no)
            if norm_q not in grouped_blocks:
                grouped_blocks[norm_q] = []
            grouped_blocks[norm_q].append(block)
            
        # 2. Build index of questions by normalized question_no
        questions_map = {self._normalize_q_no(q["question_no"]): q for q in questions}
        
        grading_units = []
        
        # 3. Align grouped blocks to questions
        for norm_q, blocks in grouped_blocks.items():
            # Sort blocks by page index and then y-coordinate to maintain order
            blocks.sort(key=lambda b: (b.page_index, b.bbox[1]))
            
            question_data = questions_map.get(norm_q)
            if not question_data:
                # No matching question in the answer key: skip or log
                continue
                
            unit = {
                "question_id": question_data.get("id"),
                "question_no": question_data["question_no"],
                "image_crops": [b.image_crop for b in blocks],
                "page_indices": [b.page_index for b in blocks],
                "key_text": question_data.get("key_text"),
                "rubric_json": question_data.get("rubric_json"),
                "max_marks": question_data["max_marks"]
            }
            grading_units.append(unit)
            
        # Sort grading units by question number order as defined in the official list
        q_order = {self._normalize_q_no(q["question_no"]): idx for idx, q in enumerate(questions)}
        grading_units.sort(key=lambda u: q_order.get(self._normalize_q_no(u["question_no"]), 999))
        
        return grading_units
