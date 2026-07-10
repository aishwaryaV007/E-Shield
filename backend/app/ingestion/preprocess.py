import cv2
import numpy as np

def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Estimates the skew angle of the page layout and rotates it to align upright.
    Uses contours and minAreaRect on non-zero coordinates.
    """
    # Convert to grayscale if necessary
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Binarize thresholding to find boundaries
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Get non-zero pixel coordinates
    pts = np.column_stack(np.where(thresh > 0))
    if len(pts) == 0:
        return image # Empty page

    # Get the minimum area bounding box enclosing the text pixels
    rect = cv2.minAreaRect(pts)
    angle = rect[-1]

    # Normalize the angle for deskewing
    # cv2.minAreaRect returns angles between -90 and 0 degrees (or 0 and 90 in some OpenCV versions)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Ignore tiny rotations to avoid interpolation quality loss
    if abs(angle) < 0.2:
        return image

    # Limit maximum correction angle to avoid false 90-degree rotations on complex pages
    if abs(angle) > 15:
        # Ignore high angles as they are usually layout anomalies
        return image

    # Perform the rotation
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated

def denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Applies a bilateral filter to smooth paper background noise while preserving sharp handwriting strokes.
    """
    # Bilateral filter needs color/grayscale 8-bit image
    # d=9 is pixel neighborhood diameter, sigmaColor=75, sigmaSpace=75
    denoised = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    return denoised

def binarize_image(image: np.ndarray) -> np.ndarray:
    """
    Converts image to grayscale and applies adaptive Gaussian thresholding.
    Outputs a clean 8-bit single-channel black-and-white binary image.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
        
    # Adaptive thresholding handles shadows/gradients better than global thresholding
    binarized = cv2.adaptiveThreshold(
        gray, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )
    return binarized

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Spine preprocessing pipeline: Deskew -> Denoise -> Binarize.
    """
    # 1. Correct any page skew/rotation first
    deskewed = deskew_image(image)
    # 2. Denoise to smooth out paper texture/grain
    denoised = denoise_image(deskewed)
    # 3. Convert to clean binary format
    binarized = binarize_image(denoised)
    
    return binarized
