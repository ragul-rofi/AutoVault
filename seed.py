import os
import psycopg2
import hashlib
import io
from db.config import get_db_connection, minio_client, MINIO_BUCKET_NAME
from utils.auth import hash_password

BASE_STORAGE_PATH = os.path.join(os.getcwd(), "uploads")

def calculate_hash(content_bytes):
    return hashlib.sha256(content_bytes).hexdigest()

def create_and_store_file(machine_id, filename, content):
    content_bytes = content.encode('utf-8')
    relative_path = f"uploads/{machine_id}/{filename}"
    
    # 1. Store on local filesystem
    folder = os.path.join(BASE_STORAGE_PATH, str(machine_id))
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        f.write(content_bytes)

    # 2. Try MinIO upload if accessible
    try:
        object_name = f"{machine_id}/{filename}"
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            minio_client.make_bucket(MINIO_BUCKET_NAME)
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            object_name,
            io.BytesIO(content_bytes),
            length=len(content_bytes),
            content_type="text/plain"
        )
    except Exception as e:
        print(f"  (Note: MinIO sync skipped for {filename}: {e})")

    return relative_path

def seed_database():
    print("Connecting to the database...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Please check your .env file or environment variables (e.g. DATABASE_URL).")
        return

    print("Dropping existing tables for a clean slate...")
    try:
        cur.execute("""
            DROP TABLE IF EXISTS audit_logs CASCADE;
            DROP TABLE IF EXISTS file_versions CASCADE;
            DROP TABLE IF EXISTS machines CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
        """)
        conn.commit()
    except Exception as e:
        print(f"Error dropping tables: {e}")
        conn.rollback()

    print("Executing schema.sql to create tables...")
    schema_path = os.path.join("db", "schema.sql")
    if not os.path.exists(schema_path):
        print(f"schema.sql not found at {schema_path}")
        return

    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        cur.execute(schema_sql)
        conn.commit()
        print("Schema successfully built!")
    except Exception as e:
        print(f"Error building schema: {e}")
        conn.rollback()
        return

    print("Seeding Users...")
    users_data = [
        ("John Doe", "john.doe@autovault.com", "admin", "admin123"),
        ("Jane Smith", "jane.smith@autovault.com", "engineer", "engineer123"),
        ("Bob Johnson", "bob.johnson@autovault.com", "viewer", "viewer123"),
        ("Sarah Connor", "sarah.connor@autovault.com", "admin", "ops123")
    ]
    user_ids = {}
    for name, email, role, pw in users_data:
        hashed_pw = hash_password(pw)
        cur.execute("""
            INSERT INTO users (name, email, role, password)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (name, email, role, hashed_pw))
        user_ids[email] = cur.fetchone()[0]
    conn.commit()
    print("Users seeded!")

    admin_id = user_ids["john.doe@autovault.com"]
    engineer_id = user_ids["jane.smith@autovault.com"]
    viewer_id = user_ids["bob.johnson@autovault.com"]
    ops_id = user_ids["sarah.connor@autovault.com"]

    print("Seeding Machines...")
    machines_data = [
        (101, "CNC Milling Center - MillAlpha"),
        (102, "PLC Assembly Line - LineBeta"),
        (103, "Precision Lathe - LatheGamma"),
        (104, "5-Axis Machining Center - Apex5X"),
        (105, "Robotic Laser Cutter - BeamX")
    ]
    for mid, mname in machines_data:
        cur.execute("""
            INSERT INTO machines (id, machine_name)
            VALUES (%s, %s);
        """, (mid, mname))
    conn.commit()
    print("Machines seeded!")

    print("Creating mock files on storage disk and seeding File Versions...")

    # 1. pump_housing.nc versions for Machine 101
    ph_v1_content = """%
O1001 (PUMP HOUSING V1)
G21 G90 G40 G80
G28 G91 Z0
M06 T01
M03 S2000
G00 X0 Y0
G01 Z-5.0 F100
X50.0 F200
Y50.0
X0
Y0
M30
%"""
    ph_v2_content = """%
O1001 (PUMP HOUSING V2 - FEEDRATE OPTIMIZED)
G21 G90 G40 G80
G28 G91 Z0
M06 T01
M03 S2200
G00 X0 Y0
G01 Z-5.0 F120
X50.0 F250
Y50.0
X0
Y0
M30
%"""

    path_ph_v1 = create_and_store_file(101, "pump_housing_v1.nc", ph_v1_content)
    hash_ph_v1 = calculate_hash(ph_v1_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("pump_housing.nc", 101, admin_id, 1, hash_ph_v1, path_ph_v1))

    path_ph_v2 = create_and_store_file(101, "pump_housing_v2.nc", ph_v2_content)
    hash_ph_v2 = calculate_hash(ph_v2_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("pump_housing.nc", 101, admin_id, 2, hash_ph_v2, path_ph_v2))

    # 2. turbine_blade.nc versions for Machine 102
    tb_v1_content = """%
O2002 (TURBINE BLADE V1)
G00 X10 Y10 Z50
G01 Z-2.0 F50
X20 Y20 F100
G00 Z50
M30
%"""
    tb_v2_content = """%
O2002 (TURBINE BLADE V2)
G00 X10 Y10 Z50
G01 Z-2.0 F55
X22 Y22 F110
G00 Z50
M30
%"""
    tb_v3_content = """%
O2002 (TURBINE BLADE V3 - FINAL PRECISION)
G00 X10 Y10 Z50
G01 Z-2.0 F60
X25 Y25 F120
G00 Z50
M30
%"""

    path_tb_v1 = create_and_store_file(102, "turbine_blade_v1.nc", tb_v1_content)
    hash_tb_v1 = calculate_hash(tb_v1_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("turbine_blade.nc", 102, engineer_id, 1, hash_tb_v1, path_tb_v1))

    path_tb_v2 = create_and_store_file(102, "turbine_blade_v2.nc", tb_v2_content)
    hash_tb_v2 = calculate_hash(tb_v2_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("turbine_blade.nc", 102, engineer_id, 2, hash_tb_v2, path_tb_v2))

    path_tb_v3 = create_and_store_file(102, "turbine_blade_v3.nc", tb_v3_content)
    hash_tb_v3 = calculate_hash(tb_v3_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("turbine_blade.nc", 102, engineer_id, 3, hash_tb_v3, path_tb_v3))

    # 3. valve_seal.gcode versions for Machine 103
    vs_v1_content = """; VALVE SEAL V1
G28 ; Home axes
G92 E0 ; Reset Extruder
G1 Z2.0 F3000
G1 X10.1 Y20 F5000.0
M104 S200
M140 S60
M30"""
    vs_v2_content = """; VALVE SEAL V2 - WARM BED
G28 ; Home axes
G92 E0 ; Reset Extruder
G1 Z2.0 F3000
G1 X10.1 Y20 F5000.0
M104 S205 ; Higher nozzle temp
M140 S65 ; Higher bed temp
M30"""

    path_vs_v1 = create_and_store_file(103, "valve_seal_v1.gcode", vs_v1_content)
    hash_vs_v1 = calculate_hash(vs_v1_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("valve_seal.gcode", 103, admin_id, 1, hash_vs_v1, path_vs_v1))

    path_vs_v2 = create_and_store_file(103, "valve_seal_v2.gcode", vs_v2_content)
    hash_vs_v2 = calculate_hash(vs_v2_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("valve_seal.gcode", 103, admin_id, 2, hash_vs_v2, path_vs_v2))

    # 4. bracket_arm.cnc for Machine 104
    ba_v1_content = """%
O5001 (BRACKET ARM 5AXIS V1)
G90 G21 G17 G40 G80
G0 B45 C90
G01 X150 Y200 Z50 F1500
M30
%"""
    path_ba_v1 = create_and_store_file(104, "bracket_arm_v1.cnc", ba_v1_content)
    hash_ba_v1 = calculate_hash(ba_v1_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("bracket_arm.cnc", 104, ops_id, 1, hash_ba_v1, path_ba_v1))

    # 5. housing_bracket.tap for Machine 105
    hb_v1_content = """(LASER CUTTER HOUSING BRACKET V1)
M103 (Laser Power On)
G00 X0 Y0
G01 X100 F500
G01 Y100
G01 X0
G01 Y0
M104 (Laser Power Off)
M30"""
    path_hb_v1 = create_and_store_file(105, "housing_bracket_v1.tap", hb_v1_content)
    hash_hb_v1 = calculate_hash(hb_v1_content.encode('utf-8'))
    cur.execute("""
        INSERT INTO file_versions (file_name, machine_id, uploaded_by, version_no, file_hash, storage_path)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, ("housing_bracket.tap", 105, engineer_id, 1, hash_hb_v1, path_hb_v1))

    conn.commit()
    print("Files and File Versions seeded!")

    print("Seeding Audit Logs...")
    audit_logs_data = [
        (viewer_id, 101, "DOWNLOAD", "pump_housing.nc", 1, "2026-07-20 09:45:00"),
        (admin_id, 101, "DIFF", "pump_housing.nc", 2, "2026-07-21 11:04:15"),
        (engineer_id, 102, "UPLOAD", "turbine_blade.nc", 3, "2026-07-22 13:15:42"),
        (admin_id, 101, "ROLLBACK", "pump_housing.nc", 1, "2026-07-23 14:32:10"),
        (ops_id, 104, "UPLOAD", "bracket_arm.cnc", 1, "2026-07-24 16:20:00")
    ]
    for uid, mid, action, fname, ver, tstamp in audit_logs_data:
        cur.execute("""
            INSERT INTO audit_logs (user_id, machine_id, action, file_name, target_version, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (uid, mid, action, fname, ver, tstamp))
    conn.commit()
    print("Audit logs seeded!")

    cur.close()
    conn.close()
    print("\nDatabase seeding completed successfully! AutoVault is ready for action.")

if __name__ == "__main__":
    seed_database()
