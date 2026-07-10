import os
from functools import lru_cache

import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


@lru_cache(maxsize=1)
def get_ocr() -> "HandwritingOCR":
    """Process-wide singleton — load TrOCR-large ONCE and reuse it across all requests
    (avoids re-loading ~1.3 GB from disk on every grade)."""
    return HandwritingOCR()


class HandwritingOCR:
    """
    Local handwriting OCR module using Hugging Face's microsoft/trocr-base-handwritten.
    Runs fully offline using cached weights in the models_cache directory.
    """
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            # Resolve models_cache path relative to this script
            default_cache = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../models_cache"))
            cache_dir = os.environ.get("MODEL_DIR", default_cache)
            
        self.cache_dir = cache_dir
        # trocr-large-handwritten measured ~91% char accuracy on our scripts vs base;
        # override with TROCR_MODEL env if a smaller/faster model is needed.
        self.model_name = os.environ.get("TROCR_MODEL", "microsoft/trocr-large-handwritten")
        
        # Load processor and model
        self.processor = TrOCRProcessor.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        
        # Move model to device (CPU by default, auto-detect GPU/MPS)
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def recognize_text(self, image: np.ndarray) -> dict:
        """
        Transcribes handwriting from the given image array.
        Computes token-level confidence scores from the model's logits.
        
        Args:
            image: A BGR or Grayscale numpy array representing the cropped answer region.
            
        Returns:
            A dict containing:
                - "text": The transcribed string.
                - "confidences": A list of float probabilities (0.0 to 1.0) for each generated token.
        """
        # Convert BGR/Grayscale to RGB PIL Image
        if len(image.shape) == 3:
            # BGR (numpy) -> RGB (PIL)
            image_rgb = image[:, :, ::-1].copy()
            pil_img = Image.fromarray(image_rgb)
        else:
            # Grayscale (numpy) -> RGB (PIL) (stack channels to make 3-channel image)
            image_rgb = np.stack([image, image, image], axis=-1)
            pil_img = Image.fromarray(image_rgb)
            
        # Process the image using TrOCR processor
        pixel_values = self.processor(images=pil_img, return_tensors="pt").pixel_values.to(self.device)
        
        # Generate transcription
        with torch.no_grad():
            outputs = self.model.generate(
                pixel_values,
                output_scores=True,
                return_dict_in_generate=True
            )
            
        # Decode the generated token IDs to string
        generated_ids = outputs.sequences[0]
        transcription = self.processor.batch_decode([generated_ids], skip_special_tokens=True)[0]
        
        # Calculate transition confidence probabilities from step logits
        confidences = []
        if hasattr(outputs, "scores") and outputs.scores:
            # Each element in scores is a tensor of logits for a generation step
            for step, logits in enumerate(outputs.scores):
                # Apply softmax to get token probabilities at this step
                probs = F.softmax(logits[0], dim=-1)
                
                # Retrieve the token ID that was actually generated at the next step (step 0 corresponds to token index 1)
                if step + 1 < len(generated_ids):
                    token_id = generated_ids[step + 1].item()
                    
                    # Exclude special tokens from the confidence calculation
                    if token_id in self.processor.tokenizer.all_special_ids:
                        continue
                        
                    token_prob = probs[token_id].item()
                    confidences.append(token_prob)
                    
        return {
            "text": transcription.strip(),
            "confidences": confidences
        }
