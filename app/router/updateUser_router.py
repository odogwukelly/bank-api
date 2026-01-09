from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.controller.updateUser_controller import update_user
from app.db.database import get_db
from app.schema.updateUser_schema import UserUpdate

router = APIRouter()

@router.put("/{user_id}", response_model=UserUpdate)
def update_user_data(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(user_id, data, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
