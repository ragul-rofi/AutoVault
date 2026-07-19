from flask import Blueprint, jsonify

from db.config import get_db_session
from db.models import User, Machine, FileVersion, AuditLog
from routes.auth_routes import require_role

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/metrics", methods=["GET"])
@require_role("admin")
def get_metrics():
    db = next(get_db_session())
    try:
        metrics = {
            "users": db.query(User).count(),
            "machines": db.query(Machine).count(),
            "file_versions": db.query(FileVersion).count(),
            "audit_logs": db.query(AuditLog).count(),
        }
        return jsonify({"status": "success", "metrics": metrics}), 200
    finally:
        db.close()
