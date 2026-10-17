import pytest

from database.db import db
from app.services.student_service import StudentService


@pytest.fixture(autouse=True)
def run_around_tests():
    db.reset()
    yield
    db.reset()


def test_enroll_and_drop_lifecycle():
    record = StudentService.enroll("S101", "C101")
    assert record["status"] == "ACTIVE"
    assert db.courses["C101"]["enrolled"] == 1
    assert db.students["S101"]["active_credits"] == 4

    dropped = StudentService.drop("S101", "C101")
    assert dropped["status"] == "DROPPED"
    assert db.courses["C101"]["enrolled"] == 0
    assert db.students["S101"]["active_credits"] == 0


def test_duplicate_enrollment_rejected():
    StudentService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="already enrolled"):
        StudentService.enroll("S101", "C101")


def test_timetable_conflict_rejected():
    # C101 and C103 share slot MON-09
    StudentService.enroll("S101", "C101")
    with pytest.raises(ValueError, match="conflict"):
        StudentService.enroll("S101", "C103")


def test_credit_limit_enforcement():
    # Add five 4-credit courses in separate slots, 18 credit limit
    for i in range(1, 6):
        StudentService.add_course(
            f"X{i}", f"Extra {i}", 4, "F201", f"SLOT-{i}")
    for i in range(1, 5):
        StudentService.enroll("S101", f"X{i}")  # 16 credits
    with pytest.raises(ValueError, match="Credit limit exceeded"):
        StudentService.enroll("S101", "X5")  # would be 20


def test_course_capacity_enforced():
    StudentService.add_course("C777", "Tiny Class", 2, "F201", "SAT-09", 1)
    StudentService.enroll("S101", "C777")
    with pytest.raises(ValueError, match="is full"):
        StudentService.enroll("S102", "C777")


def test_enroll_unknown_student_or_course():
    with pytest.raises(ValueError, match="not registered"):
        StudentService.enroll("S999", "C101")
    with pytest.raises(ValueError, match="not found in catalog"):
        StudentService.enroll("S101", "C999")


def test_drop_without_enrollment_fails():
    with pytest.raises(ValueError, match="No active enrollment"):
        StudentService.drop("S101", "C101")


def test_drop_invalid_ids_fail():
    with pytest.raises(ValueError, match="Invalid student or course"):
        StudentService.drop("S999", "C101")
