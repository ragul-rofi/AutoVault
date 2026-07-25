import os, difflib, hashlib, logging, io, tempfile
from sqlalchemy import func
from db.config import get_db_session, minio_client, MINIO_BUCKET_NAME
from db.models import User, Machine, FileVersion, AuditLog, AuditAction
from minio.error import S3Error

# Set of allowed file extensions
ALLOWED_EXTENSIONS = {'.nc', '.cnc', '.gcode', '.tap', '.txt'}

# Allow only specific file types
def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# Calculate hash of file content
def calculate_hash(file_content):
    sha256 = hashlib.sha256()
    sha256.update(file_content)
    return sha256.hexdigest()

# Central Audit Logging function
def insert_audit_log(user_id, machine_id, action, file_name, target_version=None):
    db = next(get_db_session())
    try:
        audit_log_entry = AuditLog(
            user_id=user_id,
            machine_id=machine_id,
            action=AuditAction(action), # Convert string action to Enum
            file_name=file_name,
            target_version=target_version
        )
        db.add(audit_log_entry)
        db.commit()
        db.refresh(audit_log_entry)
        logging.info("Audit log successfully inserted: %s - %s", action, file_name)
    except Exception as e:
        db.rollback()
        logging.error("Failed to insert audit log in database: %s", e)
    finally:
        db.close()

# Fetch machine ID by name/id
def get_machine_id(machine_id):
    logging.warning(f"Looking up machine_id: {machine_id}") 
    db = next(get_db_session())
    try:
        machine = db.query(Machine).filter(Machine.id == machine_id).first()
        logging.warning(f"Lookup result: {machine}")
        return machine.id if machine else None
    except Exception as e:
        logging.error("Database Error (get_machine_id): %s", e)
        return None
    finally:
        db.close()

# Get next version number for a given file on a machine
def get_next_version(file_name, machine_id):
    db = next(get_db_session())
    try:
        max_version = db.query(func.max(FileVersion.version_no)).filter(
            FileVersion.file_name == file_name,
            FileVersion.machine_id == machine_id
        ).scalar()
        return (max_version or 0) + 1
    except Exception as e:
        logging.error("Database Error (get_next_version): %s", e)
        return 1
    finally:
        db.close()

# Main function to save file and log into DB
def save_file_and_log(file, machine_id, uploaded_by):
    filename = file.filename

    # 1. Validate file extension
    if not allowed_file(filename):
        return {"status": "fail", "message": "File type not allowed"}, 400

    # 2. Read content for hashing and then reset stream for MinIO upload
    file_content_bytes = file.read() # Read content once for hashing
    file_hash = calculate_hash(file_content_bytes)
    file.seek(0) # Reset stream position to the beginning

    # 3. Get machine ID
    db_machine_id = get_machine_id(machine_id) # This function now uses ORM
    if db_machine_id is None:
        return {"status": "fail", "message": "Invalid machine id"}, 400
    # machine_id = db_machine_id # This is already correct if get_machine_id returns id

    # 4. Get next version
    version_no = get_next_version(filename, machine_id) # This function now uses ORM
    versioned_name = f"{os.path.splitext(filename)[0]}_v{version_no}{os.path.splitext(filename)[1]}"
    
    # 5. Save file (Try MinIO first, fallback to local disk)
    object_name = f"{machine_id}/{versioned_name}"
    save_path = object_name
    saved_to_minio = False

    try:
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            object_name,
            file.stream,
            length=len(file_content_bytes),
            content_type=file.content_type or "application/octet-stream"
        )
        saved_to_minio = True
    except Exception as e:
        logging.warning("MinIO unavailable, saving file locally: %s", e)
        local_dir = os.path.join(os.getcwd(), "uploads", str(machine_id))
        os.makedirs(local_dir, exist_ok=True)
        local_filepath = os.path.join(local_dir, versioned_name)
        with open(local_filepath, "wb") as f:
            f.write(file_content_bytes)
        save_path = f"uploads/{machine_id}/{versioned_name}"

    # 6. Insert into DB and write audit log
    db = next(get_db_session())
    try:
        new_file_version = FileVersion(
            file_name=filename,
            machine_id=machine_id,
            uploaded_by=uploaded_by,
            version_no=version_no,
            file_hash=file_hash,
            storage_path=save_path
        )
        db.add(new_file_version)
        db.commit()
        db.refresh(new_file_version)

        # Write immutable audit trail entry
        insert_audit_log(uploaded_by, machine_id, 'UPLOAD', filename, version_no)

        return {
            "status": "success",
            "message": "File uploaded successfully",
            "version_no": new_file_version.version_no,
            "storage_path": new_file_version.storage_path
        }, 200

    except Exception as e:
        db.rollback()
        logging.error("Database Insert Error: %s", e)
        return {"status": "fail", "message": "Internal server error"}, 500
    finally:
        db.close()

# Get files method
def get_files_by_machine(machine_id):
    db = next(get_db_session())
    try:
        logging.warning(f"Fetching files for machine_id: {machine_id}")
        file_versions = db.query(FileVersion).filter(
            FileVersion.machine_id == machine_id
        ).order_by(FileVersion.file_name, FileVersion.version_no).all()

        logging.warning(f"Fetched rows: {file_versions}")

        if not file_versions:
            return None

        files = []
        for fv in file_versions:
            files.append({
                "file_name": fv.file_name,
                "version_no": fv.version_no,
                "uploaded_by": fv.uploaded_by,
                "file_hash": fv.file_hash,
                "storage_path": fv.storage_path,
                "created_at": fv.upload_time.isoformat()
            })

        return files
    
    except Exception as e:
        logging.error("Database Error (get_files_by_machine): %s", e)
        return None
    finally:
        db.close()

# Helper to read file content from MinIO or Local disk
def read_file_content_bytes(storage_path):
    try:
        response = minio_client.get_object(MINIO_BUCKET_NAME, storage_path)
        content = response.read()
        response.close()
        response.release_conn()
        return content
    except Exception as e:
        logging.warning(f"MinIO read failed for {storage_path}, checking local disk fallback: {e}")
        
        # Check relative or absolute local path
        possible_paths = [
            storage_path,
            os.path.join(os.getcwd(), storage_path),
            os.path.join(os.getcwd(), "uploads", storage_path),
        ]
        for p in possible_paths:
            if os.path.exists(p) and os.path.isfile(p):
                with open(p, "rb") as f:
                    return f.read()
        raise FileNotFoundError(f"File not found in MinIO or local storage: {storage_path}")

# Rollback func
def rollback_file_version(machine_id, file_name, rollback_to_version, uploaded_by):
    db = next(get_db_session())
    try:
        logging.warning(f"Rolling back {file_name} on machine {machine_id} to v{rollback_to_version}")
        old_file_version = db.query(FileVersion).filter(
            FileVersion.machine_id == machine_id,
            FileVersion.file_name == file_name,
            FileVersion.version_no == rollback_to_version
        ).first()

        if not old_file_version:
            return {"status": "fail", "message": "Version not found"}, 404
        
        file_hash = old_file_version.file_hash
        old_storage_path = old_file_version.storage_path

        try:
            content = read_file_content_bytes(old_storage_path)
        except Exception as e:
            logging.error(f"Error reading file for rollback: {e}")
            return {"status": "fail", "message": "Source file missing in storage"}, 500

        new_version = get_next_version(file_name, machine_id)
        versioned_name = f"{os.path.splitext(file_name)[0]}_v{new_version}{os.path.splitext(file_name)[1]}"
        new_object_name = f"{machine_id}/{versioned_name}"
        save_path = new_object_name

        try:
            minio_client.put_object(
                MINIO_BUCKET_NAME,
                new_object_name,
                io.BytesIO(content),
                length=len(content),
                content_type="application/octet-stream"
            )
        except Exception as e:
            logging.warning("MinIO put failed during rollback, saving locally: %s", e)
            local_dir = os.path.join(os.getcwd(), "uploads", str(machine_id))
            os.makedirs(local_dir, exist_ok=True)
            local_filepath = os.path.join(local_dir, versioned_name)
            with open(local_filepath, "wb") as f:
                f.write(content)
            save_path = f"uploads/{machine_id}/{versioned_name}"

        new_file_version = FileVersion(
            file_name=file_name,
            machine_id=machine_id,
            uploaded_by=uploaded_by,
            version_no=new_version,
            file_hash=file_hash,
            storage_path=save_path
        )
        db.add(new_file_version)
        db.commit()
        db.refresh(new_file_version)

        insert_audit_log(uploaded_by, machine_id, 'ROLLBACK', file_name, rollback_to_version)

        return {
            "status": "success",
            "message": f"Rolled back to v{rollback_to_version} → new version v{new_version}",
            "version_no": new_version,
            "storage_path": save_path
        }, 200
    
    except Exception as e:
        db.rollback()
        logging.error("Rollback Error: %s", e)
        return {"status": "fail", "message": "Internal server error"}, 500
    finally:
        db.close()
    
# Get file path func
def get_file_path(machine_id, file_name, version_no):
    db = next(get_db_session())
    try:
        file_version = db.query(FileVersion).filter(
            FileVersion.machine_id == machine_id,
            FileVersion.file_name == file_name,
            FileVersion.version_no == version_no
        ).first()

        if not file_version:
            return None

        storage_path = file_version.storage_path

        # Create temporary file from storage (MinIO or Local)
        content = read_file_content_bytes(storage_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
            temp_file.write(content)
            return temp_file.name
    except Exception as e:
        logging.error("Error retrieving file path: %s", e)
        return None
    finally:
        db.close()
    
# Get file difference func
def get_file_diff(machine_id, file_name, version_a, version_b):
    path_a = get_file_path(machine_id, file_name, version_a)
    path_b = get_file_path(machine_id, file_name, version_b)

    if not path_a or not path_b:
        return None, f"Version {version_a} or {version_b} not found in database"
    
    try:
        with open(path_a, 'r') as f1, open(path_b, 'r') as f2:
            lines_a = f1.read().splitlines()
            lines_b = f2.read().splitlines()

            diff = list(difflib.unified_diff(
                lines_a,
                lines_b,
                fromfile=f"{file_name}_v{version_a}",
                tofile=f"{file_name}_v{version_b}",
                lineterm=""
            ))

            return diff, None
    except Exception as e:
        return None, f"Diff error: {str(e)}"