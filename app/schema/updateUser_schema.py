from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobile: Optional[str] = None
    dob: Optional[datetime] = None
    created_at: Optional[datetime] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    hashedPassword: Optional[str] = None
    isAdmin: Optional[bool] = None
    isEmailVerified: Optional[bool] = None

    reviewDuration : Optional[str] = None
    errorMsg : Optional[str] = None
    transferOTP : Optional[str] = None
    allowValidation : Optional[bool] = None
    allowTransfer : Optional[bool] = None

    pin: Optional[str] = None
    hasSetPin: Optional[bool] = None

    class Config:
        # orm_mode = True
        from_attributes = True
