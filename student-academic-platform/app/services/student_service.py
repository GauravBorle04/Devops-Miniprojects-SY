from datetime import datetime, timezone

from database.db import db
from app.models.student import new_student_record
from app.models.course import new_course_record

MAX_CREDITS_PER_SEMESTER = 18


def grade_for_marks(marks):
    """Convert marks (0-100) into a (letter, grade_points) tuple."""
    if marks >= 90:
        return "A", 4.0
    if marks >= 80:
        return "B", 3.0
    if marks >= 70:
        return "C", 2.0
    if marks >= 60:
        return "D", 1.0
    return "F", 0.0


def _now():
    return datetime.now(timezone.utc).isoformat()


class StudentService:
    """Encapsulates the business rules of the Student Record Platform."""

    # ---------------------------------------------------------- students
    @staticmethod
    def add_student(student_id, name, email, semester=1):
        if student_id in db.students:
            raise ValueError(f"Student with ID '{student_id}' already exists.")
        record = new_student_record(student_id, name, email, semester)
        db.students[student_id] = record
        return record

    @staticmethod
    def get_student(student_id):
        return db.students.get(student_id)

    @staticmethod
    def delete_student(student_id):
        student = db.students.get(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not found.")
        if student["active_credits"] > 0:
            raise ValueError(
                f"Cannot delete student '{student_id}' "
                "with active enrollments.")
        del db.students[student_id]
        return True

    # ----------------------------------------------------------- courses
    @staticmethod
    def add_course(course_id, title, credits, faculty_id, slot, capacity=30):
        if course_id in db.courses:
            raise ValueError(f"Course with ID '{course_id}' already exists.")
        record = new_course_record(
            course_id, title, credits, faculty_id, slot, capacity)
        db.courses[course_id] = record
        return record

    @staticmethod
    def get_course(course_id):
        return db.courses.get(course_id)

    @staticmethod
    def search_courses(query=""):
        q = query.lower().strip()
        if not q:
            return list(db.courses.values())
        return [
            c for c in db.courses.values()
            if q in c["title"].lower() or q in c["course_id"].lower()
        ]

    # ------------------------------------------------------- enrollments
    @staticmethod
    def _active_enrollments(student_id):
        return [
            e for e in db.enrollments
            if e["student_id"] == student_id and e["status"] == "ACTIVE"
        ]

    @staticmethod
    def enroll(student_id, course_id):
        student = db.students.get(student_id)
        if not student:
            raise ValueError(f"Student '{student_id}' not registered.")
        course = db.courses.get(course_id)
        if not course:
            raise ValueError(f"Course '{course_id}' not found in catalog.")

        active = StudentService._active_enrollments(student_id)

        # Rule 1: no duplicate enrollment
        if any(e["course_id"] == course_id for e in active):
            raise ValueError(
                f"Student '{student_id}' is already enrolled "
                f"in '{course_id}'.")
        # Rule 2: course capacity
        if course["enrolled"] >= course["capacity"]:
            raise ValueError(f"Course '{course['title']}' is full.")
        # Rule 3: timetable conflict
        for e in active:
            if db.courses[e["course_id"]]["slot"] == course["slot"]:
                raise ValueError(
                    f"Enrollment conflict: slot {course['slot']} is "
                    "already taken.")
        # Rule 4: credit limit per semester
        if student["active_credits"] + course["credits"] > \
                MAX_CREDITS_PER_SEMESTER:
            raise ValueError(
                "Credit limit exceeded "
                f"(Max: {MAX_CREDITS_PER_SEMESTER}).")

        course["enrolled"] += 1
        student["active_credits"] += course["credits"]
        record = {
            "enrollment_id": f"E-{len(db.enrollments) + 1:04d}",
            "student_id": student_id,
            "course_id": course_id,
            "enrolled_at": _now(),
            "status": "ACTIVE",
            "marks": None
        }
        db.enrollments.append(record)
        return record

    @staticmethod
    def drop(student_id, course_id):
        student = db.students.get(student_id)
        course = db.courses.get(course_id)
        if not student or not course:
            raise ValueError("Invalid student or course ID.")
        for e in StudentService._active_enrollments(student_id):
            if e["course_id"] == course_id:
                e["status"] = "DROPPED"
                e["dropped_at"] = _now()
                course["enrolled"] -= 1
                student["active_credits"] -= course["credits"]
                return e
        raise ValueError(
            f"No active enrollment found for student '{student_id}' "
            f"and course '{course_id}'.")

    # ------------------------------------------------------------- marks
    @staticmethod
    def record_marks(student_id, course_id, marks):
        if not isinstance(marks, (int, float)) or isinstance(marks, bool):
            raise ValueError("Marks must be a number.")
        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100.")
        for e in StudentService._active_enrollments(student_id):
            if e["course_id"] == course_id:
                letter, points = grade_for_marks(marks)
                e["marks"] = marks
                e["grade"] = letter
                e["grade_points"] = points
                return e
        raise ValueError(
            f"No active enrollment found for student '{student_id}' "
            f"and course '{course_id}'.")

    @staticmethod
    def calculate_gpa(student_id):
        if student_id not in db.students:
            raise ValueError(f"Student '{student_id}' not found.")
        total_points = 0.0
        total_credits = 0
        for e in StudentService._active_enrollments(student_id):
            if e["marks"] is None:
                continue
            credits = db.courses[e["course_id"]]["credits"]
            total_points += e["grade_points"] * credits
            total_credits += credits
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)
