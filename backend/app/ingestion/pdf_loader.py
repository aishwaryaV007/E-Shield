import os
import pypdfium2 as pdfium
import numpy as np

class PDFLoader:
    """
    Utility class to load PDF documents and rasterize their pages into high-resolution images (numpy arrays).
    """
    @staticmethod
    def rasterize_pdf(pdf_path: str, dpi: int = 300) -> list[np.ndarray]:
        """
        Loads a PDF from the given file path and renders each page to a high-resolution BGR numpy array (for OpenCV).
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
            
        doc = pdfium.PdfDocument(pdf_path)
        images = []
        
        # Calculate scale based on standard PDF resolution (72 points per inch)
        scale = dpi / 72.0
        
        for page in doc:
            # Render page bitmap
            bitmap = page.render(scale=scale)
            pil_img = bitmap.to_pil()
            # Convert RGB (PIL) to BGR (OpenCV)
            img_bgr = np.array(pil_img)[:, :, ::-1].copy()
            images.append(img_bgr)
            
        doc.close()
        return images

    @staticmethod
    def rasterize_pdf_bytes(pdf_bytes: bytes, dpi: int = 300) -> list[np.ndarray]:
        """
        Loads a PDF from raw bytes and renders each page to a high-resolution BGR numpy array.
        """
        doc = pdfium.PdfDocument(pdf_bytes)
        images = []
        scale = dpi / 72.0
        
        for page in doc:
            bitmap = page.render(scale=scale)
            pil_img = bitmap.to_pil()
            img_bgr = np.array(pil_img)[:, :, ::-1].copy()
            images.append(img_bgr)
            
        doc.close()
        return images
