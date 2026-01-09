from sqlalchemy.orm import Session
from app.model.user_model import User
from app.schema.updateUser_schema import UserUpdate
from app.utils.security import hash_password

def update_user(user_id: int, update_data: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
        
    db.commit()
    db.refresh(user)
    updated_user = db.query(User).filter(User.id == user_id).first()
    return updated_user
