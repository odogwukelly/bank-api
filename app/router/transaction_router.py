from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.database import get_db
from app.model import account_model, transaction_model
from app.schema import account_schema, transaction_schema
from app.utils.helper import generate_account_number, generate_routing_number
from app.utils.queryHelper import get_user_by_id


router = APIRouter()

@router.post("/create")
def create_transaction(transaction: transaction_schema.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = transaction_model.Transaction(
        userID = transaction.userID,
        cardID = transaction.cardID,
        accountID = transaction.accountID,
        amount = transaction.amount,
        status = transaction.status,
        type = transaction.type,
        title = transaction.title,
        category = transaction.category,
        desc = transaction.desc,
        created_at = transaction.created_at
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=list[transaction_schema.TransactionResponse])
def get_transactions(user_id: int = Query(None), account_id: int = Query(None),db: Session = Depends(get_db)):
    if user_id is not None and account_id is not None:
        # ✅ Filter by both user_id and account_id
        transactions = db.query(transaction_model.Transaction).filter(
            and_(
                transaction_model.Transaction.userID == user_id,
                transaction_model.Transaction.accountID == account_id
            )
        ).all()
    elif user_id is not None:
        # ✅ Filter only by user_id
        transactions = db.query(transaction_model.Transaction).filter(
            transaction_model.Transaction.userID == user_id
        ).all()
    elif account_id is not None:
        # ✅ Filter only by account_id
        transactions = db.query(transaction_model.Transaction).filter(
            transaction_model.Transaction.accountID == account_id
        ).all()
    else:
        # ✅ Return all transactions
        transactions = db.query(transaction_model.Transaction).all()

    return transactions


@router.get("/get/{user_id}", response_model=List[transaction_schema.TransactionResponse])
def get_transaction_by_user_id(user_id: int, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.Transaction).filter(transaction_model.Transaction.userID == user_id).all()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/get-transaction/{transaction_id}", response_model=transaction_schema.TransactionResponse)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.Transaction).filter(transaction_model.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=transaction_schema.TransactionResponse)
def update_transaction(transaction_id: int, update_data: transaction_schema.TransactionUpdate, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.Transaction).filter(transaction_model.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    if update_data.amount is not None:
        transaction.amount = update_data.amount

    if update_data.status is not None:
        transaction.status = update_data.status

    if update_data.type is not None:
        transaction.type = update_data.type

    if update_data.title is not None:
        transaction.title = update_data.title

    if update_data.category is not None:
        transaction.category = update_data.category

    if update_data.desc is not None:
        transaction.desc = update_data.desc

    if update_data.created_at is not None:
        transaction.created_at = update_data.created_at

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(transaction_model.Transaction).filter(transaction_model.Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
