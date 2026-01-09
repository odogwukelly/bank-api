from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.user_model import User
from app.utils.emailService import send_otp_email
from app.utils.security import generate_otp, verify_otp

router = APIRouter()
time = 5
class EmailRequest(BaseModel):
    email: EmailStr

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str

@router.post("/send-otp")
def send_otp_route(data: EmailRequest, db: Session = Depends(get_db)):
    otp = generate_otp(db, data.email)
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        pass
    sent = send_otp_email(data.email, otp, time, user.fullName )
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    return {"msg": "OTP sent successfully"}


# @router.post("/verify-otp")
# def verify_otp_route(data: VerifyOtpRequest, db: Session = Depends(get_db)):
#     is_valid, message = verify_otp(data.email, data.otp, db)
#     return {"success": is_valid, "message": message}

@router.post("/verify-otp")
def verify_otp_route(data: VerifyOtpRequest, db: Session = Depends(get_db)):
    is_valid, message = verify_otp(data.email, data.otp, db)
    
    if not is_valid:
        # ❌ Wrong OTP or expired or not found
        raise HTTPException(status_code=400, detail=message)

    # ✅ OTP verified successfully
    return {"success": True, "message": message}

