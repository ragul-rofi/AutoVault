import os
import hashlib
import logging
import psycopg2
from db.config import DB_NAME, DB_USER, DB_PORT, DB_HOST, DB_PASSWORD

# Set of allowed file extensions (corrected)
ALLOWED_EXTENSIONS = {'.nc', '.cnc', '.gcode', '.tap','.txt'}

# Allow only specific file types
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
    # e.g., test.NC -> .nc (lowered) -> check if allowed

# Calculate hash of file content
def calculate_hash(file_content):
    sha256 = hashlib.sha256()
    sha256.update(file_content)
    return sha256.hexdigest()

# Fetch machine ID by name
def get_machine_id(machine_id):
    logging.warning(f"Looking up machine_id: {machine_id}") 
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT id FROM machines WHERE id = %s", (machine_id,))
        result = cur.fetchone()
        logging.warning(f"Lookup result: {result}")
        cur.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        logging.error("Database Error (get_machine_id): %s", e)
        return None

# Get next version number for a given file on a machine
def get_next_version(file_name, machine_id):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(version_no) FROM file_versions
            WHERE file_name = %s AND machine_id = %s
        """, (file_name, machine_id))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return (result[0] or 0) + 1
    except Exception as e:
        logging.error("Database Error (get_next_version): %s", e)
        return 1

# Main function to save file and log into DB
def save_file_and_log(file, machine_id, uploaded_by):
    filename = file.filename

    # 1. Validate file extension
    if not allowed_file(filename):
        return {"status": "fail", "message": "File type not allowed"}, 400

    # 2. Read and hash content
    content = file.read()
    file_hash = calculate_hash(content)

    
    # 3. Get machine ID
    db_machine_id = get_machine_id(machine_id)
    if db_machine_id is None:
        return {"status": "fail", "message": "Invalid machine id"}, 400
    machine_id = db_machine_id



    # 4. Get next version
    version_no = get_next_version(filename, machine_id)
    versioned_name = f"{os.path.splitext(filename)[0]}_v{version_no}{os.path.splitext(filename)[1]}"
    
    # 5. Save file to disk
    folder_path = os.path.join("uploads", str(machine_id))
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, versioned_name)

    try:
        with open(save_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        logging.error("File Save Error: %s", e)
        return {"status": "fail", "message": "Failed to save file"}, 500

    # 6. Insert into DB
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO file_versions (
                file_name, machine_id, uploaded_by,
                version_no, file_hash, storage_path
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (filename, machine_id, uploaded_by, version_no, file_hash, save_path))
        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": "success",
            "message": "File uploaded successfully",
            "version_no": version_no,
            "storage_path": save_path
        }, 200

    except Exception as e:
        logging.error("Database Insert Error: %s", e)
        return {"status": "fail", "message": "Internal server error"}, 500
