# 1. FILE PURPOSE: Split a page image into single text-line crops via horizontal projection.
# 2. RESPONSIBILITIES: binarize, mask margins (left rule + right bleed-through), find line bands,
#    return each line's box and whether it starts at the left margin (a question header).
# 3. DEPENDS ON / USED BY: OpenCV, numpy; used by pipeline/model_a_reader.py.
import cv2
import numpy as np

HEADER_X_FRAC = 0.11   # lines starting left of this are treated as question headers


def segment_lines(rgb: np.ndarray) -> list[dict]:
    """Return line boxes as dicts: {y0,y1,x0,x1,is_header}."""
    H, W = rgb.shape[:2]
    gray = cv2.GaussianBlur(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), (3, 3), 0)
    _, binv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    binv[:, : int(0.085 * W)] = 0     # left vertical margin rule
    binv[:, int(0.965 * W):] = 0      # right reverse-page bleed-through
    binv = cv2.morphologyEx(binv, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

    proj = np.convolve(binv.sum(axis=1).astype(float), np.ones(9) / 9, mode="same")
    thr = max(proj.max() * 0.06, 255 * 8)
    on = proj > thr

    bands, start = [], None
    for y in range(H):
        if on[y] and start is None:
            start = y
        elif not on[y] and start is not None:
            bands.append((start, y)); start = None
    if start is not None:
        bands.append((start, H))

    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] < 12:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(list(b))

    lines = []
    for y0, y1 in merged:
        if y1 - y0 < 18:
            continue
        yy0, yy1 = max(0, y0 - 8), min(H, y1 + 8)
        cols = np.where(binv[yy0:yy1].sum(axis=0) > 0)[0]
        if len(cols) == 0:
            continue
        x0, x1 = max(0, int(cols[0]) - 10), min(W, int(cols[-1]) + 12)
        lines.append({"y0": yy0, "y1": yy1, "x0": x0, "x1": x1,
                      "is_header": (x0 / W) <= HEADER_X_FRAC})
    return lines
