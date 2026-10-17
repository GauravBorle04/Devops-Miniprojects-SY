from flask import Blueprint, jsonify

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
