from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SupportBase(BaseModel):
    email : Optional[str] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    mobile : Optional[str] = None
    message: Optional[str] = None
    created_at:  Optional[datetime] = None


class SupportCreate(SupportBase):
    userID: int


class SupportResponse(SupportBase):
    userID: int
    

    class Config:
        # orm_mode = True
        from_attributes = True
