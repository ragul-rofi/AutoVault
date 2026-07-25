from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum as SqlEnum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserRole(str, Enum):
    admin = "admin"
    engineer = "engineer"
    viewer = "viewer"

class AuditAction(str, Enum):
    UPLOAD = "UPLOAD"
    ROLLBACK = "ROLLBACK"
    DOWNLOAD = "DOWNLOAD"
    DIFF = "DIFF"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(SqlEnum(UserRole, name="userrole", native_enum=False), nullable=False)
    password = Column(String, nullable=False)

class Machine(Base):
    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, nullable=False)

class FileVersion(Base):
    __tablename__ = 'file_versions'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    machine_id = Column(Integer, ForeignKey('machines.id', ondelete='CASCADE'))
    uploaded_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    version_no = Column(Integer, nullable=False)
    upload_time = Column(DateTime, server_default=func.now())
    file_hash = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    file_content = Column(String, nullable=True)

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    machine_id = Column(Integer, ForeignKey('machines.id', ondelete='CASCADE'))
    action = Column(SqlEnum(AuditAction, name="auditaction", native_enum=False), nullable=False)
    file_name = Column(String, nullable=False)
    target_version = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
