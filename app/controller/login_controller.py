from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.utils.queryHelper import get_account_by_user_id, get_user_by_email
from app.utils.security import verify_password, create_access_token

def login_user(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address"
        )
    if (password != user.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        ) 
    
    token = create_access_token({"sub": user.email})
    user_accounts = get_account_by_user_id(user.id, db)

    
    # return the user details together with the token
    return {
        "userData": user,
        "userAccount": user_accounts,
        "access_token": token       
    }
