import json
import csv
import os

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_json(records, fname="cv_extracted.json"):
    path = os.path.join(OUTPUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return path


def save_csv(records, fname="cv_extracted.csv"):
    if not records:
        return None

    path = os.path.join(OUTPUT_DIR, fname)
    keys = sorted({k for r in records for k in r})

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()

        for r in records:
            row = {
                k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                for k, v in r.items()
            }
            writer.writerow(row)

    return path
