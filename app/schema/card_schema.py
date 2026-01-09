from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CardBase(BaseModel):
    userID: int
    accountID: int
    cardBalance: Optional[float] = None
    status: bool
    cardType: str
    cardName: str
    expiresAt: Optional[datetime] = None
     

class CardResponse(BaseModel):
    id:  Optional[int] = None
    accountID:  Optional[int] = None
    userID:  Optional[int] = None
    cardNumber: Optional[str] = None
    cvv: Optional[str] = None
    cardBalance: Optional[float] = None
    status: Optional[bool] = None
    cardType: Optional[str] = None
    cardName: Optional[str] = None
    expiresAt: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    id:  Optional[int] = None
    accountID:  Optional[int] = None
    userID:  Optional[int] = None
    cardNumber: Optional[str] = None
    cvv: Optional[str] = None
    cardBalance: Optional[float] = None
    status: Optional[bool] = None
    cardType: Optional[str] = None
    cardName: Optional[str] = None
    expiresAt: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



    class Config:
        # orm_mode = True
        from_attributes = True
