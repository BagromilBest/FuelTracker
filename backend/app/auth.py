from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import hashlib
from . import models, database

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
# NOTE: In production, use environment variable: os.getenv("SECRET_KEY")
SECRET_KEY = "your-secret-key-change-in-production-please-use-environment-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def _pre_hash_password(password: str) -> str:
    """Pre-hash password with SHA-256 to handle bcrypt's 72-byte limit.
    
    bcrypt has a maximum password length of 72 bytes. To securely support
    longer passwords without silent truncation, we pre-hash with SHA-256
    which produces a consistent 64-character hex string (well under 72 bytes).
    
    This approach:
    - Prevents silent truncation of long passwords
    - Maintains security by using a cryptographic hash
    - Ensures consistent hashing regardless of password length
    
    NOTE: This pre-hashing was added to fix the 72-byte limit issue.
    For new deployments, all passwords will use this pre-hashing.
    The bcrypt layer still adds its own unique salt for each hash.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with SHA-256 pre-hashing.
    
    Pre-hashes the password with SHA-256 before bcrypt to handle
    the 72-byte bcrypt limit securely.
    """
    pre_hashed = _pre_hash_password(password)
    return pwd_context.hash(pre_hashed)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.
    
    Pre-hashes the password with SHA-256 before verification to match
    the hashing process.
    """
    pre_hashed = _pre_hash_password(plain_password)
    return pwd_context.verify(pre_hashed, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db)
):
    """Dependency to verify admin authentication."""
    token = credentials.credentials
    payload = verify_token(token)
    
    # Verify admin exists in database
    admin = db.query(models.Admin).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    
    return admin


def ensure_admin(db: Session):
    """Ensure admin exists with default password if not present.
    
    NOTE: Default password "Bagr123" is used as per requirements.
    In production, consider requiring password setup on first run.
    """
    admin = db.query(models.Admin).first()
    if not admin:
        default_password = "Bagr123"  # As per requirements
        admin = models.Admin(password_hash=hash_password(default_password))
        db.add(admin)
        db.commit()
        db.refresh(admin)
    return admin


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db)
):
    """Dependency to verify user authentication."""
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user


def get_current_user_or_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(database.get_db)
):
    """Dependency to verify user or admin authentication."""
    token = credentials.credentials
    payload = verify_token(token)
    
    is_admin = payload.get("sub") == "admin"
    user_id = payload.get("user_id")
    
    if is_admin:
        admin = db.query(models.Admin).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin not found",
            )
        return {"type": "admin", "admin": admin}
    elif user_id:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )
        return {"type": "user", "user": user}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
