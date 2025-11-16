from paddleocr import PaddleOCR

ocr_instance = PaddleOCR(lang="en", use_textline_orientation=True)

def get_text_from_image_data(image_data):
    try:
        result = ocr_instance.ocr(image_data, cls=True)
        if not result or not result[0]:
            return ""
        lines = []
        for line in result[0]:
            txt, score = line[1]
            if score is None or score >= 0.3:
                lines.append(txt)
        return "\n".join(lines)
    except Exception as e:
        print(f"[ocr_runner] OCR error: {e}")
        return ""
