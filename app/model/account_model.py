from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, func
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, index=True)
    accountType = Column(String)
    accountName = Column(String)
    accountNumber = Column(String, unique=True, index=True)
    routingNumber = Column(String, unique=True, index=True)
    status = Column(Boolean, default=True)
    approvedAccount = Column(Boolean, default=False)
    accountBalance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
