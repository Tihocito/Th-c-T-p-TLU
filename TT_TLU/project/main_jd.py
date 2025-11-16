from jd_extract.stage_jd_form import input_jd_form
from jd_extract.stage_jd_validate import validate_jd
from jd_extract.stage_jd_export import save_jds_to_csv


def main():
    all_jds = []
    print("Enter JD entries.\n")

    while True:
        jd = input_jd_form()
        res = validate_jd(jd)
        print("Validation:", res)

        if res["valid"]:
            all_jds.append(jd)
        else:
            print("JD not saved due to validation errors.")

        if input("Add another JD? (y/N): ").lower() != "y":
            break

    if all_jds:
        path = save_jds_to_csv(all_jds)
        print("Saved:", path)
    else:
        print("No JD saved.")


if __name__ == "__main__":
    main()
