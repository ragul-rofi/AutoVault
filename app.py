from flask import Flask, request, jsonify
from utils.auth import authenticate_user
from utils.file_utils import save_file_and_log 
from utils.file_utils import get_files_by_machine
from utils.file_utils import rollback_file_version
from functools import wraps
from utils.auth import get_user_role


def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            user_id = data.get('uploaded_by') or data.get('user_id')  # flexible field name

            if not user_id:
                return jsonify({"status": "fail", "message": "Missing user ID"}), 400

            role = get_user_role(user_id)
            if role not in allowed_roles:
                return jsonify({"status": "fail", "message": "Access denied"}), 403

            return f(*args, **kwargs)
        return wrapped
    return decorator

app = Flask(__name__)

@app.route('/')
def home():
    return "AutoVault backend is running."


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if user:
        return jsonify({
            "status": "success",
            "id": user[0],
            "name": user[1],
            "role": user[2]
        })
    else:
        return jsonify({
            "status": "fail",
            "message": "Invalid Credentials"
        }), 401


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "fail", "message": "No file part"}), 400

    file = request.files['file']
    machine_id = request.form.get('machine_id')
    uploaded_by = request.form.get('uploaded_by')


    try:
        machine_id = int(machine_id)
        uploaded_by = int(uploaded_by)
    except (ValueError, TypeError):
        return jsonify({"status": "fail", "message": "Invalid machine_id or uploaded_by"}), 400

    if not all([file, machine_id, uploaded_by]):
        return jsonify({"status": "fail", "message": "Missing required fields"}), 400

    result, status = save_file_and_log(file, machine_id, uploaded_by)
    return jsonify(result), status

@app.route('/files/<int:machine_id>', methods=['GET'])
def list_files(machine_id):
    files = get_files_by_machine(machine_id)
    if files is not None:
        return jsonify({
            "status" : "success",
            "files": files
        }), 200
    else:
        return jsonify({
            "status" : "fail",
            "message" : "Invalid machine id"
        }), 400
    

@app.route('/rollback', methods=['POST'])
@require_role('admin')
def rollback_file():
    data = request.get_json()

    machine_id = data.get('machine_id')
    file_name = data.get('file_name')
    target_version = data.get('target_version')
    uploaded_by = data.get('uploaded_by')

    try:
        machine_id = int(machine_id)
        target_version = int(target_version)
        uploaded_by = int(uploaded_by)
    except (ValueError, TypeError):
        return jsonify({
            "status" : "fail",
            "message" : "Invalid input types"
        }), 400
    
    if not all([machine_id,file_name,target_version, uploaded_by]):
        return jsonify({
            "status" : "fail",
            "message" : "Missing fields"
        }), 400
    
    result, status = rollback_file_version(machine_id, file_name, target_version, uploaded_by)
    return jsonify(result),status



if __name__ == '__main__':
    app.run(debug=True)