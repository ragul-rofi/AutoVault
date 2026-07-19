from flask import Blueprint, jsonify

from db.config import get_db_session
from db.models import Machine
from routes.auth_routes import require_role

machine_bp = Blueprint("machines", __name__)


@machine_bp.route("/machines", methods=["GET"])
@require_role("admin", "engineer", "viewer")
def list_machines():
    db = next(get_db_session())
    try:
        machines = db.query(Machine).order_by(Machine.id).all()
        payload = [
            {"id": machine.id, "machine_name": machine.machine_name}
            for machine in machines
        ]
        return jsonify({"status": "success", "machines": payload}), 200
    finally:
        db.close()
