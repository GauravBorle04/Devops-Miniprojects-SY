import pytest

from app import create_app
from database.db import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        db.reset()
        yield client
        db.reset()


def test_healthcheck_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "UP"
    assert "Student Record" in json_data["service"]


def test_dashboard_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Record" in response.data


def test_api_list_courses(client):
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.get_json()["count"] >= 3


def test_api_register_and_get_student(client):
    payload = {"student_id": "S500", "name": "Test User",
               "email": "t@edu.com", "semester": 2}
    created = client.post("/api/students", json=payload)
    assert created.status_code == 201
    fetched = client.get("/api/students/S500")
    assert fetched.status_code == 200
    assert fetched.get_json()["name"] == "Test User"
    assert client.get("/api/students/NOPE").status_code == 404


def test_api_register_student_validation_error(client):
    response = client.post("/api/students", json={"student_id": "S501"})
    assert response.status_code == 400


def test_api_add_course(client):
    payload = {"course_id": "C500", "title": "AI Basics", "credits": 3,
               "faculty_id": "F201", "slot": "THU-09"}
    assert client.post("/api/courses", json=payload).status_code == 201
    assert client.post("/api/courses", json=payload).status_code == 400


def test_api_enroll_drop_marks_and_gpa(client):
    enroll = {"student_id": "S101", "course_id": "C101"}
    response = client.post("/api/enroll", json=enroll)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Enrollment successful"

    marks = client.post("/api/marks", json={
        "student_id": "S101", "course_id": "C101", "marks": 88})
    assert marks.status_code == 200

    gpa = client.get("/api/students/S101/gpa")
    assert gpa.status_code == 200
    assert gpa.get_json()["gpa"] == 3.0

    drop = client.post("/api/drop", json=enroll)
    assert drop.status_code == 200


def test_api_error_paths(client):
    assert client.post("/api/enroll", json={}).status_code == 400
    assert client.post("/api/drop", json={}).status_code == 400
    assert client.post("/api/marks", json={}).status_code == 400
    assert client.get("/api/students/NOPE/gpa").status_code == 404
