import cv2
from .stage_preprocess_cv import preprocess_column, preprocess_image_for_ocr
from .stage_ocr_runner import get_text_from_image_data
from .stage_nlp_extract import (
    clean_ocr_errors_smart, clean_text,
    extract_emails_from_ocr, find_phone_number,
    find_full_name, find_applied_position, find_years_experience,
    extract_education_level, extract_languages, extract_frameworks, extract_databases
)


def extract_text_from_cv(file_path: str):
    image = cv2.imread(file_path)
    if image is None:
        return "", f"Cannot read file: {file_path}"

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    left = gray[:, :int(w * 0.40)]
    right = gray[:, int(w * 0.60):]

    mean_left = float(left.mean())
    mean_right = float(right.mean())
    TH = 80

    is_dark_left = mean_left < mean_right - TH
    is_dark_right = mean_right < mean_left - TH

    if is_dark_left:
        split = int(w * 0.42)
        L = preprocess_column(gray[:, :split], True)
        R = preprocess_column(gray[:, split:], False)
        raw = get_text_from_image_data(L) + "\n\n" + get_text_from_image_data(R)

    elif is_dark_right:
        split = int(w * 0.58)
        L = preprocess_column(gray[:, :split], False)
        R = preprocess_column(gray[:, split:], True)
        raw = get_text_from_image_data(L) + "\n\n" + get_text_from_image_data(R)

    else:
        try:
            temp = preprocess_image_for_ocr(file_path)
            raw = get_text_from_image_data(temp)
        except:
            raw = get_text_from_image_data(image)

    if not raw or not raw.strip():
        return "", "No text found"

    return raw, None


def parse_cv(file_path: str):
    raw, err = extract_text_from_cv(file_path)
    if err:
        return {"error": err, "raw_ocr_text": raw}

    text = clean_text(clean_ocr_errors_smart(raw))
    contact = text[:1000]

    return {
        "full_name": find_full_name(contact),
        "email": extract_emails_from_ocr(contact),
        "phone_number": find_phone_number(contact),
        "applied_position": find_applied_position(text),
        "education_level": extract_education_level(text),
        "years_experience": find_years_experience(text),
        "languages": extract_languages(text),
        "frameworks": extract_frameworks(text),
        "databases": extract_databases(text),
        "raw_ocr_text": raw,
    }
