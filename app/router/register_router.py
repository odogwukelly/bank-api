from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller.register_controller import create_user
from app.db.database import get_db
from app.schema.register_schema import UserCreate, UserResponse


router = APIRouter()

@router.post("/register")
def register_route(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user(user, db)
    return { "msg": "Account Created Successfully"}
