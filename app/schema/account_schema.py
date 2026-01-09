from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AccountBase(BaseModel):
    userID: int
    accountBalance: Optional[float] = None
    status: bool
    accountType: str
    accountName: str
    
    approvedAccount : Optional[bool] = None
    reviewDuration : Optional[str] = None
    errorMsg : Optional[str] = None
    transferOTP : Optional[str] = None
    allowValidation : Optional[bool] = None

class AccountResponse(BaseModel):
    id:  Optional[int] = None
    userID:  Optional[int] = None
    accountNumber: Optional[str] = None
    accountBalance: Optional[float] = None
    approvedAccount: Optional[bool] = None
    status: Optional[bool] = None
    accountType: Optional[str] = None
    accountName: Optional[str] = None
    routingNumber: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    userID: int | None = None
    accountBalance: float | None = None
    status: bool | None = None
    accountType: str | None = None
    accountName: str | None = None
    routingNumber: str | None = None
    created_at: Optional[datetime] = None
    reviewDuration : Optional[str] = None
    errorMsg : Optional[str] = None
    transferOTP : Optional[str] = None
    allowValidation : Optional[bool] = None
    approvedAccount : Optional[bool] = None

class AccountOut(AccountBase):
    accountNumber: Optional[str] = None
    routingNumber: Optional[str] = None
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


    class Config:
        # orm_mode = True
        from_attributes = True
