from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import random
from sqlalchemy.orm import Session
from app.model.otp_model import OTP
from app.model.user_model import User


# --- JWT CONFIG ---
SECRET_KEY = "YOUR_SECRET_KEY"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*60

# --- PASSWORD CONFIG ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72  # bcrypt limit

def hash_password(password: str) -> str:
    # Validate length in bytes
    if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password too long. Maximum length is {MAX_BCRYPT_BYTES} bytes."
        )
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

def generate_otp(db: Session, email: str, expiry_minutes: int = 10):
    """Generate and store OTP in database"""
    otp_value = str(random.randint(100000, 999999))  # 6-digit OTP
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    # Delete any existing OTP for this email
    db.query(OTP).filter(OTP.email == email, OTP.is_used == False).delete()

    # Store new OTP
    otp_record = OTP(email=email, otp=otp_value, expires_at=expires_at)
    db.add(otp_record)
    db.commit()
    db.refresh(otp_record)

    return otp_value


def verify_otp(email: str, otp: str, db: Session):
    """Verify OTP stored in database and update user verification status"""

    otp_record = (
        db.query(OTP)
        .filter(OTP.email == email, OTP.is_used == False)
        .order_by(OTP.created_at.desc())
        .first()
    )

    if not otp_record:
        return False, "No OTP found for this email"

    # Check if expired
    if otp_record.is_expired():
        return False, "OTP expired"

    # Check validity
    if otp_record.otp != otp:
        return False, "Invalid OTP"

    # Mark OTP as used
    otp_record.is_used = True
    db.commit()

    # Update user verification
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False, "User not found"

    user.isEmailVerified = True
    db.commit()

    return True, "OTP verified and email confirmed successfully"


