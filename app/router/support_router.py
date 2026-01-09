from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model import account_model, support_model
from app.model.transaction_model import Transaction
from app.schema import account_schema, support_schema
from app.utils.helper import generate_account_number, generate_routing_number
from app.utils.queryHelper import get_user_by_id

router = APIRouter()


@router.post("/create/support")
def create_support(support: support_schema.SupportCreate, db: Session = Depends(get_db)):
    db_support = support_model.Support(
        userID=support.userID,
        email = support.email,
        category = support.category,
        subject = support.subject,
        mobile = support.mobile,
        message = support.message,
        created_at = support.created_at
    )

    db.add(db_support)
    db.commit()
    db.refresh(db_support)
    return {"msg": "Support created successfully"}


@router.get("/get/all/support", response_model=List[support_schema.SupportResponse])
def get_all_support(db: Session = Depends(get_db)):
    supports = db.query(support_model.Support).all()
    if not supports:
        raise HTTPException(status_code=404, detail="No supports found")
    return supports


@router.get("/get/support/{user_id}", response_model=List[support_schema.SupportResponse])
def get_support_by_user_id(user_id: int, db: Session = Depends(get_db)):

    support = db.query(support_model.Support).filter(support_model.Support.userID == user_id).all()
    if not support:
        raise HTTPException(status_code=404, detail="support not found")
    return support


@router.delete("/delete/support/{user_id}")
def delete_support_by_user_id(user_id: int, db: Session = Depends(get_db)):

    support = db.query(support_model.Support).filter(support_model.Support.userID == user_id).first()
    if not support:
        raise HTTPException(status_code=404, detail="support not found")
    
    db.delete(support)
    db.commit()
    return {"msg": "Support deleted successfully"}


