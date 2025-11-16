import os
from cv_extract.stage_parse_cv import parse_cv
from cv_extract.stage_export_cv import save_csv, save_json


def main():
    src = input("Enter path to image or folder: ").strip()
    if not src:
        print("No path provided.")
        return

    records = []

    if os.path.isdir(src):
        for fn in sorted(os.listdir(src)):
            if fn.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                info = parse_cv(os.path.join(src, fn))
                info["file_name"] = fn
                records.append(info)
    else:
        info = parse_cv(src)
        info["file_name"] = os.path.basename(src)
        records.append(info)

    if not records:
        print("Nothing extracted.")
        return

    j_path = save_json(records)
    c_path = save_csv(records)

    print("\nSaved:")
    print(j_path)
    print(c_path)


if __name__ == "__main__":
    main()
