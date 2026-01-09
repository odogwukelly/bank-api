from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    mobile = Column(String)
    dob = Column(DateTime)
    address = Column(String)
    email = Column(String, unique=True, index=True)
    hashedPassword = Column(String)
    isAdmin = Column(Boolean, default=False)
    isEmailVerified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    reviewDuration = Column(String)
    errorMsg = Column(String)
    transferOTP = Column(String)
    allowValidation = Column(Boolean, default=False)
    allowTransfer = Column(Boolean, default=False)

    pin = Column(String)
    hasSetPin = Column(Boolean, default=False)
    profile_image = Column(String, nullable=True)
    profileUrl = Column(String, nullable=True)



