from sqlalchemy.orm import Session
from app.model.user_model import User
from app.schema.register_schema import UserCreate
from app.utils.queryHelper import get_user_by_email
from app.utils.security import hash_password
from fastapi import HTTPException, status


def create_user(user: UserCreate, db: Session):
    # check if email already exists
    existing_user = get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # hashed = hash_password(user.password)
    fullName = f"{user.firstName} {user.lastName}"

    new_user = User(
        fullName=fullName,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        hashedPassword=user.password,

        reviewDuration="24 hours" ,
        errorMsg = "Your transfer could not be processed",
        transferOTP = "550011",
        allowValidation = False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


