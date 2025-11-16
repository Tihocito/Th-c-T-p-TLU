def validate_jd(jd):
    errors = []

    if not jd.get("job_title"):
        errors.append("Job title cannot be empty.")

    if jd.get("required_experience_years") is None:
        errors.append("Experience years must be a number.")

    if not jd.get("required_languages"):
        errors.append("Required languages cannot be empty.")

    return {"valid": len(errors) == 0, "errors": errors}
