from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, func
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, index=True)
    accountID = Column(Integer, index=True)
    cardID = Column(Integer, index=True)
    type = Column(String)
    category = Column(String)
    title = Column(String)
    desc = Column(String)
    status = Column(String)
    amount = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
