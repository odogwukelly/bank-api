from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TransactionBase(BaseModel):
    userID: int
    accountID: int
    amount: float = 0.0
    cardID:  Optional[int] = None
    status:  Optional[str] = None
    type:  Optional[str] = None
    title:  Optional[str] = None
    category:  Optional[str] = None
    desc:  Optional[str] = None
    created_at:  Optional[datetime] = None

class TransactionResponse(BaseModel):
    id: int
    userID: Optional[int] = None
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    amount: Optional[float] = None
    status:  Optional[str] = None
    type:  Optional[str] = None
    title:  Optional[str] = None
    category:  Optional[str] = None
    desc:  Optional[str] = None
    created_at:  Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    status:  Optional[str] = None
    type:  Optional[str] = None
    title:  Optional[str] = None
    category:  Optional[str] = None
    desc:  Optional[str] = None
    created_at:  Optional[datetime] = None

    class Config:
        # orm_mode = True
        from_attributes = True
