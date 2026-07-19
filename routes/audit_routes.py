from flask import Blueprint, jsonify, request

from db.config import get_db_session
from db.models import AuditLog, User, Machine
from routes.auth_routes import require_role

audit_bp = Blueprint("audit", __name__)


@audit_bp.route("/audit-logs", methods=["GET"])
@require_role("admin")
def get_audit_logs():
    """
    Paginated, filterable audit log endpoint.
    Query params:
        page (int): Page number, default 1
        per_page (int): Items per page, default 50
        user_id (int): Filter by user
        machine_id (int): Filter by machine
        action (str): Filter by action type (UPLOAD, ROLLBACK, DOWNLOAD, DIFF)
    """
    db = next(get_db_session())
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 50, type=int)
        user_id = request.args.get("user_id", type=int)
        machine_id = request.args.get("machine_id", type=int)
        action = request.args.get("action", type=str)

        query = db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if machine_id:
            query = query.filter(AuditLog.machine_id == machine_id)
        if action:
            query = query.filter(AuditLog.action == action)

        total = query.count()
        logs = (
            query
            .order_by(AuditLog.timestamp.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        # Resolve user names and machine names
        user_ids = list(set(log.user_id for log in logs if log.user_id))
        machine_ids = list(set(log.machine_id for log in logs if log.machine_id))

        users_map = {}
        if user_ids:
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            users_map = {u.id: u.name for u in users}

        machines_map = {}
        if machine_ids:
            machines = db.query(Machine).filter(Machine.id.in_(machine_ids)).all()
            machines_map = {m.id: m.machine_name for m in machines}

        payload = []
        for log in logs:
            payload.append({
                "id": log.id,
                "user_id": log.user_id,
                "user_name": users_map.get(log.user_id, "Unknown"),
                "machine_id": log.machine_id,
                "machine_name": machines_map.get(log.machine_id, f"Machine {log.machine_id}"),
                "action": log.action.value if hasattr(log.action, 'value') else log.action,
                "file_name": log.file_name,
                "target_version": log.target_version,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
            })

        return jsonify({
            "status": "success",
            "logs": payload,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }), 200
    finally:
        db.close()
