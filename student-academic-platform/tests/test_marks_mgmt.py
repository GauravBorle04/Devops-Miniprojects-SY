import pytest

from database.db import db
from app.services.student_service import StudentService, grade_for_marks


@pytest.fixture(autouse=True)
def run_around_tests():
    db.reset()
    yield
    db.reset()


@pytest.mark.parametrize("marks,letter,points", [
    (95, "A", 4.0),
    (85, "B", 3.0),
    (75, "C", 2.0),
    (65, "D", 1.0),
    (40, "F", 0.0),
])
def test_grade_boundaries(marks, letter, points):
    assert grade_for_marks(marks) == (letter, points)


def test_record_marks_success():
    StudentService.enroll("S101", "C101")
    record = StudentService.record_marks("S101", "C101", 92)
    assert record["marks"] == 92
    assert record["grade"] == "A"


def test_record_marks_out_of_range_rejected():
    StudentService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="between 0 and 100"):
        StudentService.record_marks("S101", "C101", 150)


def test_record_marks_non_numeric_rejected():
    StudentService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="must be a number"):
        StudentService.record_marks("S101", "C101", "ninety")


def test_record_marks_without_enrollment_rejected():
    with pytest.raises(ValueError, match="No active enrollment"):
        StudentService.record_marks("S101", "C101", 80)


def test_gpa_is_credit_weighted():
    # C101 = 4 credits, marks 90 -> 4.0 ; C102 = 4 credits, marks 70 -> 2.0
    StudentService.enroll("S101", "C101")
    StudentService.enroll("S101", "C102")
    StudentService.record_marks("S101", "C101", 90)
    StudentService.record_marks("S101", "C102", 70)
    assert StudentService.calculate_gpa("S101") == 3.0


def test_gpa_weighting_with_different_credits():
    # C102 (4 credits) marks 90 -> 4.0 ; C103 (3 credits) marks 60 -> 1.0
    # GPA = (4.0*4 + 1.0*3) / 7 = 2.71
    StudentService.enroll("S101", "C102")
    StudentService.enroll("S101", "C103")
    StudentService.record_marks("S101", "C102", 90)
    StudentService.record_marks("S101", "C103", 60)
    assert StudentService.calculate_gpa("S101") == 2.71


def test_gpa_zero_without_marks():
    StudentService.enroll("S101", "C101")
    assert StudentService.calculate_gpa("S101") == 0.0


def test_gpa_unknown_student_fails():
    with pytest.raises(ValueError, match="not found"):
        StudentService.calculate_gpa("S999")
