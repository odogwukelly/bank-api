from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr
from app.schema.account_schema import AccountResponse
from app.schema.register_schema import UserResponse

# Login Schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    userData:  Optional[UserResponse] = None
    userAccount:  Optional[List[AccountResponse]] = None
    access_token: str


     
