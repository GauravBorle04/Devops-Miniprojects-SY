from flask import Blueprint, request, jsonify

from app.services.student_service import StudentService

api_bp = Blueprint("api", __name__)

SERVICE_NAME = "Enterprise Student Record and Academic Management Platform"


@api_bp.route("/health", methods=["GET"])
def healthcheck():
    """Liveness and readiness endpoint for Kubernetes & Docker healthchecks."""
    return jsonify({
        "status": "UP",
        "service": SERVICE_NAME,
        "version": "1.0.0"
    }), 200


@api_bp.route("/students", methods=["POST"])
def register_student():
    data = request.get_json(silent=True) or {}
    try:
        student = StudentService.add_student(
            student_id=data.get("student_id"),
            name=data.get("name"),
            email=data.get("email"),
            semester=int(data.get("semester", 1))
        )
        return jsonify({"message": "Student registered successfully",
                        "student": student}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = StudentService.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@api_bp.route("/students/<student_id>/gpa", methods=["GET"])
def get_gpa(student_id):
    try:
        gpa = StudentService.calculate_gpa(student_id)
        return jsonify({"student_id": student_id, "gpa": gpa}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@api_bp.route("/courses", methods=["GET"])
def list_courses():
    q = request.args.get("q", "")
    courses = StudentService.search_courses(q)
    return jsonify({"count": len(courses), "courses": courses}), 200


@api_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json(silent=True) or {}
    try:
        course = StudentService.add_course(
            course_id=data.get("course_id"),
            title=data.get("title"),
            credits=int(data.get("credits", 3)),
            faculty_id=data.get("faculty_id"),
            slot=data.get("slot"),
            capacity=int(data.get("capacity", 30))
        )
        return jsonify({"message": "Course added successfully",
                        "course": course}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/enroll", methods=["POST"])
def enroll_student():
    data = request.get_json(silent=True) or {}
    try:
        enrollment = StudentService.enroll(
            student_id=data.get("student_id"),
            course_id=data.get("course_id")
        )
        return jsonify({"message": "Enrollment successful",
                        "enrollment": enrollment}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/drop", methods=["POST"])
def drop_course():
    data = request.get_json(silent=True) or {}
    try:
        enrollment = StudentService.drop(
            student_id=data.get("student_id"),
            course_id=data.get("course_id")
        )
        return jsonify({"message": "Course dropped successfully",
                        "enrollment": enrollment}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/marks", methods=["POST"])
def record_marks():
    data = request.get_json(silent=True) or {}
    try:
        enrollment = StudentService.record_marks(
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            marks=data.get("marks")
        )
        return jsonify({"message": "Marks recorded successfully",
                        "enrollment": enrollment}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
