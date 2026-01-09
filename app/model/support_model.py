from sqlalchemy import Column, DateTime, Integer, String, func
from app.db.database import Base

class Support(Base):
    __tablename__ = "supports"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer)
    email = Column(String)
    category = Column(String)
    subject = Column(String)
    mobile = Column(String)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())