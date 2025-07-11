from flask import Flask, request,jsonify
from utils.auth import authenticate_user
from utils.file_utils import save_file_and_log 

app = Flask(__name__)

@app.route('/')

def home():
    return "AutoVault backend is running."


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')


    user = authenticate_user(email,password)
    if user:
        return jsonify({
            "status":"success",
            "id" : user[0],
            "name" : user[1],
            "role" : user[2]
        })
    else:
        return jsonify({
            "status" : "fail",
            "message" : "Invalid Credentials"
        }),401
    

@app.route('/upload',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "fail", "message": "No file part"}), 400
    file = request.files['files']
    machine_name = request.form.get('machine_name')
    uploaded_by = request.form.get('uploaded_by')

    if not all([file,machine_name, uploaded_by]):
        return jsonify({"status": "fail", "message": "Missing required fields"}), 400
    
    result, staus = save_file_and_log(file, machine_name, int(uploaded_by))
    return jsonify(result), status # type: ignore

if __name__ == '__main__':
    app.run(debug=True)