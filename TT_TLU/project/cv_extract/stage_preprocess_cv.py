import cv2
import numpy as np
import os
from typing import Optional


def preprocess_image_for_ocr(img_path: str, out_path: Optional[str] = None) -> str:
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {img_path}")

    img = cv2.equalizeHist(img)
    img = cv2.medianBlur(img, 3)
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    img_dilated = cv2.dilate(img_bin, kernel, iterations=1)

    if out_path is None:
        out_path = os.path.join(os.getcwd(), "cleaned_cv.png")

    cv2.imwrite(out_path, img_dilated)
    return out_path


def preprocess_column(column_gray, is_dark_bg=False):
    if is_dark_bg:
        col_inverted = cv2.bitwise_not(column_gray)
        return cv2.adaptiveThreshold(
            col_inverted, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    else:
        return cv2.adaptiveThreshold(
            column_gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
