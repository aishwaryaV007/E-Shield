# RubricLens Assistive Engine
> Architectural specifications for semantic rubric alignment matching, Natural Language Inference (NLI) classification, and color-coded evidence highlights.

*Design / Planned — Not yet implemented*

---

## 1. Engine Purpose & Core Logic

**RubricLens** serves as an assistive tool for grading, aiming to reduce grading times by up to 50%. It matches student answer text with grading rubric guidelines, highlighting relevant points to simplify the grading process.

### Governing Principle
> **"Never auto-grade; the human assigns the mark."**
> The engine highlights supporting or contradicting text evidence but does not automatically assign scores or adjust grades.

```
                    ┌──────────────────────────────┐
                    │ Prose OCR Student Text Output│
                    └──────────────┬───────────────┘
                                   │
                                   ▼ (Retrieval Step)
                    ┌──────────────────────────────┐
                    │ Retrieve Candidate Sentences │
                    └──────────────┬───────────────┘
                                   │
                                   ▼ (NLI DeBERTa Inference)
                    ┌──────────────────────────────┐
                    │ Compare text against Rubric  │
                    └──────────────┬───────────────┘
              ┌────────────────────┴────────────────────┐
              │                                         │
       Entails Rubric?                         Contradicts Rubric?
              │                                         │
              ▼                                         ▼
     [ Highlight Green ]                        [ Highlight Red ]
```

---

## 2. Natural Language Inference (NLI) Classifier (`rubriclens.py`)

Simple keyword matching struggles with handwritten text due to wording variations and spelling errors. RubricLens solves this by using a local **Natural Language Inference (NLI)** cross-encoder model:

*   **Hypothesis:** The grading rubric guideline (e.g., *"States that energy is released as heat"*).
*   **Premise:** The student's OCR-extracted answer text (e.g., *"In this reaction, thermal energy is radiated outwards, warming up the surroundings"*).
*   **Model:** `cross-encoder/nli-deberta-v3-xsmall`.

The NLI model evaluates the premise against the hypothesis and outputs three probability scores: `Entailment`, `Contradiction`, and `Neutral`.

```python
# Planned implementation pattern
from sentence_transformers import CrossEncoder

class RubricLensEngine:
    def __init__(self):
        # Load local NLI model
        self.model = CrossEncoder("cross-encoder/nli-deberta-v3-xsmall")
        
    def analyze_sentence(self, student_sentence: str, rubric_guideline: str) -> dict:
        # Format input for cross-encoder
        scores = self.model.predict([(student_sentence, rubric_guideline)])[0]
        
        # Class labels returned by the cross-encoder: [Contradiction, Entailment, Neutral]
        contradiction, entailment, neutral = scores
        
        result = {
            "sentence": student_sentence,
            "classification": "NEUTRAL",
            "score": float(neutral)
        }
        
        if entailment > 0.65 and entailment > contradiction:
            result["classification"] = "ENTAILMENT"
            result["score"] = float(entailment)
        elif contradiction > 0.65 and contradiction > entailment:
            result["classification"] = "CONTRADICTION"
            result["score"] = float(contradiction)
            
        return result
```

---

## 3. Visual Dashboard Overlays

The classification results are displayed as color-coded text overlays in the Streamlit dashboard:

*   **Green Highlight (Entailment):** Indicates text segments that align with the rubric guidelines.
*   **Red Highlight (Contradiction):** Highlights text that contradicts the rubric (e.g., *"the heat is absorbed"* when the rubric requires *"heat is released"*).
*   **Neutral (Unchanged):** Unlabeled text.

This highlights relevant sections of the script for the grader, helping speed up evaluation while leaving final grading decisions to the human.

---

## 4. Related Documents

*   [OCR Module Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/ocr/README.md)
*   [Technology Stack Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TECH_STACK.md)
*   [Product Features List](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FEATURES.md)
