def new_student_record(student_id, name, email, semester=1):
    """Build a validated student record."""
    if not student_id or not name or not email:
        raise ValueError(
            "All student fields (student_id, name, email) are mandatory.")
    if "@" not in email:
        raise ValueError("A valid email address is required.")
    return {
        "student_id": student_id,
        "name": name,
        "email": email,
        "semester": semester,
        "active_credits": 0
    }
