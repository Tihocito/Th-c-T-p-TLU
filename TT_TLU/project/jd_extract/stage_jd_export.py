import csv
import os

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_jds_to_csv(jds, fname="jd_catalog.csv"):
    if not jds:
        return None

    path = os.path.join(OUTPUT_DIR, fname)
    keys = sorted({k for jd in jds for k in jd})

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for jd in jds:
            writer.writerow(jd)

    return path
