from db.config import get_db_session
from db.models import User, UserRole
from passlib.hash import pbkdf2_sha256

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

def authenticate_user(email, password):
    try:
        db = next(get_db_session()) # Get a session
        user = db.query(User).filter(User.email == email).first()

        if user:
            # Verify the provided password against the stored hash
            if verify_password(password, user.password):
                role_value = user.role.value if hasattr(user.role, "value") else user.role
                return {'id': user.id, 'name': user.name, 'role': role_value}
        
        return None # None if not found or password does not match
    except Exception as e:
        print("Database error: (authenticate user)", e)
        return None
    finally:
        db.close()

def get_user_role(user_id):
    try:
        db = next(get_db_session()) # Get a session
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return user.role.value if hasattr(user.role, "value") else user.role
    except Exception as e:
        print("Database Error (get_user_role): ", e)
        return None
    finally:
        db.close()
