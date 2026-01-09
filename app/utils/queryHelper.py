from sqlalchemy.orm import Session
from app.model.account_model import Account
from app.model.user_model import User
from fastapi import HTTPException, status


def get_all_users(db: Session):
    user = db.query(User).all()
    return user

def count_users(db: Session):
    user_count = db.query(User).count()
    return user_count


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_id(userID: int, db: Session):
    user = db.query(User).filter(User.id == userID).first()
    return user


def get_user_id_by_email(email: str, db: Session) -> int:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.id


def get_account_by_user_id(userID: int, db: Session):
    account = db.query(Account).filter(Account.userID == userID).all()
    return account