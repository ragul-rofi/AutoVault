from flask import Blueprint, jsonify, request, send_file, session

from routes.auth_routes import require_role
from utils.file_utils import (
    save_file_and_log,
    get_files_by_machine,
    rollback_file_version,
    get_file_path,
    get_file_diff,
    insert_audit_log,
    get_file_content_by_version,
    save_edited_file_content,
)

file_bp = Blueprint("files", __name__)


def _resolve_user_id():
    user = session.get("user")
    if user and user.get("id"):
        return user.get("id")

    header_user_id = request.headers.get("X-User-Id")
    if header_user_id:
        try:
            return int(header_user_id)
        except ValueError:
            return None

    return None


@file_bp.route("/upload", methods=["POST"])
@require_role("admin", "engineer")
def upload_file():
    file = request.files.get("file")
    machine_id = request.form.get("machine_id")
    uploaded_by = request.form.get("uploaded_by") or _resolve_user_id()

    if not file or not machine_id or not uploaded_by:
        return jsonify({"status": "fail", "message": "file, machine_id, uploaded_by required"}), 400

    try:
        machine_id = int(machine_id)
        uploaded_by = int(uploaded_by)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid machine_id or uploaded_by"}), 400

    response, status = save_file_and_log(file, machine_id, uploaded_by)
    return jsonify(response), status


@file_bp.route("/files/<int:machine_id>", methods=["GET"])
@require_role("admin", "engineer", "viewer")
def list_files(machine_id):
    files = get_files_by_machine(machine_id)
    if files is None:
        return jsonify({"status": "fail", "message": "No files found"}), 404
    return jsonify({"status": "success", "files": files}), 200


@file_bp.route("/rollback", methods=["POST"])
@require_role("admin")
def rollback_file():
    payload = request.get_json(silent=True) or request.form or {}
    machine_id = payload.get("machine_id")
    file_name = payload.get("file_name")
    rollback_to_version = payload.get("rollback_to_version") or payload.get("target_version")
    uploaded_by = payload.get("uploaded_by") or _resolve_user_id()

    if not machine_id or not file_name or not rollback_to_version or not uploaded_by:
        return jsonify({"status": "fail", "message": "machine_id, file_name, rollback_to_version, uploaded_by required"}), 400

    try:
        machine_id = int(machine_id)
        rollback_to_version = int(rollback_to_version)
        uploaded_by = int(uploaded_by)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid numeric values"}), 400

    response, status = rollback_file_version(machine_id, file_name, rollback_to_version, uploaded_by)
    return jsonify(response), status


@file_bp.route("/download", methods=["POST"])
@require_role("admin", "engineer", "viewer")
def download_file():
    payload = request.get_json(silent=True) or request.form or {}
    machine_id = payload.get("machine_id")
    file_name = payload.get("file_name")
    version_no = payload.get("version_no")
    user_id = payload.get("user_id") or _resolve_user_id()

    if not machine_id or not file_name or not version_no:
        return jsonify({"status": "fail", "message": "machine_id, file_name, version_no required"}), 400

    try:
        machine_id = int(machine_id)
        version_no = int(version_no)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid numeric values"}), 400

    file_path = get_file_path(machine_id, file_name, version_no)
    if not file_path:
        return jsonify({"status": "fail", "message": "File not found"}), 404

    if user_id:
        try:
            insert_audit_log(int(user_id), machine_id, "DOWNLOAD", file_name, version_no)
        except Exception:
            pass

    return send_file(file_path, as_attachment=True, download_name=file_name)


@file_bp.route("/diff", methods=["POST"])
@require_role("admin", "engineer")
def diff_file():
    payload = request.get_json(silent=True) or request.form or {}
    machine_id = payload.get("machine_id")
    file_name = payload.get("file_name")
    version_a = payload.get("version_a")
    version_b = payload.get("version_b")
    user_id = payload.get("user_id") or _resolve_user_id()

    if not machine_id or not file_name or not version_a or not version_b:
        return jsonify({"status": "fail", "message": "machine_id, file_name, version_a, version_b required"}), 400

    try:
        machine_id = int(machine_id)
        version_a = int(version_a)
        version_b = int(version_b)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid numeric values"}), 400

    diff, error = get_file_diff(machine_id, file_name, version_a, version_b)
    if error:
        return jsonify({"status": "fail", "message": error}), 404

    if user_id:
        try:
            insert_audit_log(int(user_id), machine_id, "DIFF", file_name, version_b)
        except Exception:
            pass

    return jsonify({"status": "Success", "diff": diff}), 200


@file_bp.route("/file-content", methods=["GET", "POST"])
@require_role("admin", "engineer", "viewer")
def file_content():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
    else:
        payload = request.args

    machine_id = payload.get("machine_id")
    file_name = payload.get("file_name")
    version_no = payload.get("version_no")

    if not machine_id or not file_name or not version_no:
        return jsonify({"status": "fail", "message": "machine_id, file_name, version_no required"}), 400

    try:
        machine_id = int(machine_id)
        version_no = int(version_no)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid numeric values"}), 400

    content, error = get_file_content_by_version(machine_id, file_name, version_no)
    if error:
        return jsonify({"status": "fail", "message": error}), 404

    return jsonify({"status": "success", "content": content, "file_name": file_name, "version_no": version_no}), 200


@file_bp.route("/files/save-content", methods=["POST"])
@require_role("admin", "engineer")
def save_file_content():
    payload = request.get_json(silent=True) or {}
    machine_id = payload.get("machine_id")
    file_name = payload.get("file_name")
    content = payload.get("content")
    uploaded_by = payload.get("uploaded_by") or _resolve_user_id()

    if not machine_id or not file_name or content is None or not uploaded_by:
        return jsonify({"status": "fail", "message": "machine_id, file_name, content, uploaded_by required"}), 400

    try:
        machine_id = int(machine_id)
        uploaded_by = int(uploaded_by)
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid machine_id or uploaded_by"}), 400

    response, status = save_edited_file_content(machine_id, file_name, content, uploaded_by)
    return jsonify(response), status

