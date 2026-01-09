from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# Registeration Schema
class UserBase(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    fullName: Optional[str] = None
    dob: Optional[datetime] = None
    totalBalance: Optional[float] = None
    isAdmin: Optional[bool] = None
    isEmailVerified: Optional[bool] = None
    address: Optional[str] = None
    mobile: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    hashedPassword: Optional[str] = None
    profile_image: Optional[str] = None
    profileUrl: Optional[str] = None

    pin: Optional[str] = None
    hasSetPin: Optional[bool] = None

    reviewDuration : Optional[str] = None
    errorMsg : Optional[str] = None
    transferOTP : Optional[str] = None
    allowValidation : Optional[bool] = None
    allowTransfer : Optional[bool] = None

    class Config:
        from_attributes = True

