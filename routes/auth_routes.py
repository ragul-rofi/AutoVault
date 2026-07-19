from functools import wraps
from flask import Blueprint, jsonify, request, session

from db.config import get_db_session
from db.models import User, UserRole
from utils.auth import authenticate_user, hash_password, get_user_role

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


# Admin User Management Routes
@auth_bp.route("/users", methods=["GET"])
@require_role("admin")
def list_users():
    db = next(get_db_session())
    try:
        users = db.query(User).order_by(User.id).all()
        payload = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            }
            for u in users
        ]
        return jsonify({"status": "success", "users": payload}), 200
    finally:
        db.close()


@auth_bp.route("/users", methods=["POST"])
@require_role("admin")
def create_user():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    email = payload.get("email")
    role_str = payload.get("role", "viewer")
    password = payload.get("password", "password123")

    if not name or not email:
        return jsonify({"status": "fail", "message": "Name and email required"}), 400

    db = next(get_db_session())
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return jsonify({"status": "fail", "message": "Email already registered"}), 400

        hashed_pw = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            role=UserRole(role_str) if role_str in UserRole.__members__ else UserRole.viewer,
            password=hashed_pw,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return jsonify({
            "status": "success",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role.value if hasattr(new_user.role, "value") else str(new_user.role),
            }
        }), 201
    finally:
        db.close()


@auth_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@require_role("admin")
def update_user_role(user_id):
    payload = request.get_json(silent=True) or {}
    new_role = payload.get("role")

    if not new_role or new_role not in ["admin", "engineer", "viewer"]:
        return jsonify({"status": "fail", "message": "Invalid role"}), 400

    db = next(get_db_session())
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u:
            return jsonify({"status": "fail", "message": "User not found"}), 404

        u.role = UserRole(new_role)
        db.commit()
        return jsonify({"status": "success", "message": f"Updated role to {new_role}"}), 200
    finally:
        db.close()


@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_role("admin")
def delete_user(user_id):
    db = next(get_db_session())
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u:
            return jsonify({"status": "fail", "message": "User not found"}), 404

        db.delete(u)
        db.commit()
        return jsonify({"status": "success", "message": "User deleted"}), 200
    finally:
        db.close()
