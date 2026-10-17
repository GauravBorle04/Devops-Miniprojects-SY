from flask import Blueprint, render_template

from database.db import db

web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET"])
def dashboard():
    """Simple web dashboard so the running app is visible in a browser."""
    return render_template(
        "index.html",
        students=list(db.students.values()),
        courses=list(db.courses.values()),
        enrollments=db.enrollments,
    )
