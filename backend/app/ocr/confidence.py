import numpy as np

def answer_confidence(confidences: list[float]) -> float:
    """
    Computes the aggregate confidence score of an OCR transcription.
    Returns the average probability of the generated tokens, or 1.0 if no tokens were produced (e.g., blank answer).
    """
    if not confidences:
        return 1.0
    return float(np.mean(confidences))

def needs_human_check(score: float, threshold: float = 0.8) -> bool:
    """
    Flags whether the overall transcription confidence score is below the threshold,
    requiring manual verification by a human evaluator.
    """
    return score < threshold
