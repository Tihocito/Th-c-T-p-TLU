def input_jd_form():
    print("\n=== Job Description Input ===\n")

    job_title = input("Job title: ")

    exp = input("Experience (years): ")
    try:
        exp = int(exp)
    except:
        exp = None

    languages = input("Languages (comma separated): ")
    languages = [x.strip() for x in languages.split(",") if x.strip()]

    frameworks = input("Frameworks (comma separated): ")
    frameworks = [x.strip() for x in frameworks.split(",") if x.strip()]

    databases = input("Databases (comma separated): ")
    databases = [x.strip() for x in databases.split(",") if x.strip()]

    education = input("Education level: ")

    return {
        "job_title": job_title,
        "required_experience_years": exp,
        "required_languages": languages,
        "required_frameworks": frameworks,
        "required_databases": databases,
        "education_level": education,
    }
