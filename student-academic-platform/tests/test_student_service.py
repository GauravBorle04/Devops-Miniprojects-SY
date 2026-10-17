import pytest

from database.db import db
from app.services.student_service import StudentService


@pytest.fixture(autouse=True)
def run_around_tests():
    db.reset()
    yield
    db.reset()


def test_add_student_success():
    student = StudentService.add_student(
        "S200", "Grace Hopper", "grace@navy.mil", 2)
    assert student["student_id"] == "S200"
    assert student["name"] == "Grace Hopper"
    assert student["active_credits"] == 0


def test_add_duplicate_student_raises_error():
    with pytest.raises(ValueError, match="already exists"):
        StudentService.add_student("S101", "Duplicate Alice", "a2@edu.com")


def test_add_student_missing_fields_raises_error():
    with pytest.raises(ValueError, match="mandatory"):
        StudentService.add_student("S300", "", "x@edu.com")


def test_add_student_invalid_email_raises_error():
    with pytest.raises(ValueError, match="valid email"):
        StudentService.add_student("S301", "No Email", "not-an-email")


def test_get_student_lookup():
    assert StudentService.get_student("S101")["name"] == "Alice Johnson"
    assert StudentService.get_student("S999") is None


def test_delete_student_success():
    assert StudentService.delete_student("S102") is True
    assert StudentService.get_student("S102") is None


def test_delete_unknown_student_fails():
    with pytest.raises(ValueError, match="not found"):
        StudentService.delete_student("S999")


def test_delete_student_with_enrollments_fails():
    StudentService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="active enrollments"):
        StudentService.delete_student("S101")


def test_add_and_search_courses():
    StudentService.add_course("C900", "Machine Learning", 4, "F201", "FRI-10")
    assert StudentService.get_course("C900")["credits"] == 4
    assert len(StudentService.search_courses("machine")) == 1
    assert len(StudentService.search_courses("")) == 4


def test_add_duplicate_course_raises_error():
    with pytest.raises(ValueError, match="already exists"):
        StudentService.add_course("C101", "Dup", 3, "F201", "FRI-10")


def test_add_course_invalid_credits_raises_error():
    with pytest.raises(ValueError, match="at least 1"):
        StudentService.add_course("C901", "Bad", 0, "F201", "FRI-11")


def test_add_course_invalid_capacity_raises_error():
    with pytest.raises(ValueError, match="capacity"):
        StudentService.add_course("C902", "Bad", 3, "F201", "FRI-12", 0)


def test_add_course_missing_fields_raises_error():
    with pytest.raises(ValueError, match="mandatory"):
        StudentService.add_course("C903", "", 3, "F201", "FRI-13")
