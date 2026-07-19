from functools import wraps
from flask import Blueprint, jsonify, request, session

from utils.auth import authenticate_user, get_user_role

auth_bp = Blueprint("auth", __name__)


def _resolve_role():
    user = session.get("user")
    if user and user.get("role"):
        return user.get("role")

    header_role = request.headers.get("X-User-Role")
    if header_role:
        return header_role

    header_user_id = request.headers.get("X-User-Id")
    if header_user_id:
        try:
            return get_user_role(int(header_user_id))
        except ValueError:
            return None

    return None


def require_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = _resolve_role()
            if not role:
                return jsonify({"status": "fail", "message": "Unauthorized"}), 403

            if roles and role not in roles:
                return jsonify({"status": "fail", "message": "Forbidden"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        return jsonify({"status": "fail", "message": "Email and password required"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

    session["user"] = user
    return jsonify({"status": "success", **user}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status": "success"}), 200
