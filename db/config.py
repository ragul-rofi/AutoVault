import os
import psycopg2 # Keep for potential migration/debugging, though not directly used for ORM
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base # Import Base from models
from minio import Minio # Import Minio client
from minio.error import S3Error # Import S3Error

# Load environment variables from .env file
load_dotenv()

# DATABASE CONFIG (Fallback/Local Defaults)
DB_NAME = os.environ.get("DB_NAME", "autovault")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")

# MINIO CONFIG
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadminpassword")
MINIO_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME", "autovault-files")
MINIO_SECURE = os.environ.get("MINIO_SECURE", "False").lower() == "true" # Use True for HTTPS

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)

def create_minio_bucket():
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
            minio_client.make_bucket(MINIO_BUCKET_NAME)
            print(f"MinIO bucket '{MINIO_BUCKET_NAME}' created successfully.")
        else:
            print(f"MinIO bucket '{MINIO_BUCKET_NAME}' already exists.")
    except S3Error as e:
        print(f"Error checking/creating MinIO bucket: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with MinIO: {e}")



DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True
    )

def get_db_connection():
    """
    Legacy psycopg2 connection helper used by seed.py.
    """
    if DATABASE_URL:
        db_url = DATABASE_URL
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(db_url)

    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Dependency for getting a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
