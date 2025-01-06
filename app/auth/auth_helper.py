# auth/auth_helper.py
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from utils.security import verify_password, create_access_token
from models.user import User
from sqlalchemy.orm import Session

"""
def authenticate_user(db: Session, username: str, password: str, required_role: str = None):
    user = db.query(User).filter(User.username == username).first()
    
    # Verifica las credenciales
    if user is None or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verifica el rol, si es necesario
    if required_role and user.role != required_role:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied: {required_role} role required"
        )
    
    return user
"""
# Authenticate the user based on username and password
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user



# Create a JWT token
def create_jwt_token(user: User):
    return create_access_token(data={"sub": user.username, "role": user.role})


from passlib.context import CryptContext

# Set up a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain-text password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


