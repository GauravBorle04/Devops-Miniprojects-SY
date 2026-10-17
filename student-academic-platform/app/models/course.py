def new_course_record(course_id, title, credits, faculty_id, slot,
                      capacity=30):
    """Build a validated course record."""
    if not course_id or not title or not faculty_id or not slot:
        raise ValueError(
            "All course fields (course_id, title, faculty_id, slot) "
            "are mandatory.")
    if credits < 1:
        raise ValueError("Course credits must be at least 1.")
    if capacity < 1:
        raise ValueError("Course capacity must be at least 1.")
    return {
        "course_id": course_id,
        "title": title,
        "credits": credits,
        "faculty_id": faculty_id,
        "slot": slot,
        "capacity": capacity,
        "enrolled": 0
    }
