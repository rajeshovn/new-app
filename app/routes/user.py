from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.role import Role
from ..schemas.user import UserCreate
from ..utils.database import SessionLocal
from ..utils.auth import get_password_hash
from ..utils.logger import log_action
from ..utils.email import send_verification_email  # We'll create this function
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Assign the default role (customer)
    default_role = db.query(Role).filter(Role.name == "customer").first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Default role not found")

    # Generate a verification token
    verification_token = secrets.token_urlsafe(32)
    token_expires_at = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours

    # Create new user
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_no=user.phone_no,
        password=hashed_password,
        role_id=default_role.id,
        is_active=False,  # Inactive until email verification
        verification_token=verification_token,
        token_expires_at=token_expires_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send verification email
    send_verification_email(user.email, verification_token)

    # Log the action
    log_action(db, db_user.id, "register", "127.0.0.1")  # Replace with actual IP

    return {"message": "User registered successfully. Please check your email to verify your account."}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    # Find the user with the matching token
    db_user = db.query(User).filter(User.verification_token == token).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Check if the token has expired
    if db_user.token_expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token has expired")

    # Activate the user
    db_user.is_active = True
    db_user.verification_token = None
    db_user.token_expires_at = None
    db.commit()

    return {"message": "Email verified successfully. Your account is now active."}

@router.post("/resend-verification-email")
def resend_verification_email(email: str, db: Session = Depends(get_db)):
    # Find the user by email
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user is already active
    if db_user.is_active:
        raise HTTPException(status_code=400, detail="User is already active")

    # Generate a new verification token
    verification_token = secrets.token_urlsafe(32)
    token_expires_at = datetime.utcnow() + timedelta(hours=24)

    # Update the user's token
    db_user.verification_token = verification_token
    db_user.token_expires_at = token_expires_at
    db.commit()

    # Send the new verification email
    send_verification_email(db_user.email, verification_token)

    return {"message": "Verification email sent successfully."}