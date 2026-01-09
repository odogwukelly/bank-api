from typing import List, Optional
from pydantic import BaseModel
from app.schema.account_schema import AccountResponse
from app.schema.register_schema import UserResponse


class getUserResponse(BaseModel):
    userData:  Optional[UserResponse] = None
    userAccount: Optional[List[AccountResponse]] = None  

class getAllUserResponse(BaseModel):
    totalUsers: int
    userData:  Optional[List[UserResponse]] = None
    
    
 