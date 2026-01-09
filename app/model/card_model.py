from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, func
from app.db.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, index=True)
    accountID = Column(Integer, index=True)
    cardType = Column(String)
    cardName = Column(String)
    cvv = Column(String)
    expiresAt = Column(DateTime(timezone=True), server_default=func.now())
    cardNumber = Column(String, unique=True, index=True)
    status = Column(Boolean, default=True)
    cardBalance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())