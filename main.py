from flask import Flask, request, jsonify, send_file, session, Blueprint
import os
from functools import wraps
from flask_cors import CORS

# Import blueprints
from routes.auth_routes import auth_bp, require_role
from routes.file_routes import file_bp
from routes.machine_routes import machine_bp
from routes.metrics_routes import metrics_bp
from routes.audit_routes import audit_bp

# Import ORM models and session management for utility functions (if needed directly in main.py)
from db.config import get_db_session, create_minio_bucket
from db.models import User, Machine, FileVersion, AuditLog, UserRole, AuditAction # Add these imports

# Import utility functions (these should now use ORM internally)
from utils.auth import authenticate_user, hash_password, get_user_role
from utils.file_utils import save_file_and_log, get_files_by_machine, rollback_file_version, get_file_path, get_file_diff, insert_audit_log

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "autovault-dev-secret")
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(file_bp)
app.register_blueprint(machine_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(audit_bp)

@app.route('/')
def home():
    return "AutoVault backend is running."

if __name__ == '__main__':
    create_minio_bucket() # Ensure MinIO bucket exists
    # Try loading Gunicorn bindings, otherwise use native Flask debug server locally
    app.run(host='0.0.0.0', port=5000, debug=True)