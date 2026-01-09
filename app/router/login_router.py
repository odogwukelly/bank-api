from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.login_schema import LoginRequest, TokenResponse
from app.controller.login_controller import login_user
from app.schema.register_schema import UserResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login_route(body: LoginRequest, db: Session = Depends(get_db)):
    return login_user(body.email, body.password, db)
    


