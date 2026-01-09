from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model import account_model
from app.model.card_model import Card
from app.model.transaction_model import Transaction
from app.schema import account_schema
from app.utils.helper import generate_account_number, generate_routing_number
from app.utils.queryHelper import get_user_by_id

router = APIRouter()


# ✅ Create Account
@router.post("/create")
def create_account(account: account_schema.AccountCreate, db: Session = Depends(get_db)):
    routingNumber = generate_routing_number()
    account_number = generate_account_number()
    db_account = account_model.Account(
        userID=account.userID,
        accountNumber=account_number,
        accountType=account.accountType,
        accountName=account.accountName,
        routingNumber= routingNumber
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# 📥 Get All Accounts
@router.get("/", response_model=list[account_schema.AccountOut])
def get_accounts(user_id: int = Query(None), db: Session = Depends(get_db)):
    if user_id is not None:
        # Filter by user_id if provided
        accounts = db.query(account_model.Account).filter(account_model.Account.userID == user_id).all()
    else:
        # Otherwise return all accounts
        accounts = db.query(account_model.Account).all()
    return accounts

# 📥 Get Single Account by Account Number
@router.get("/number/{account_number}", response_model=account_schema.AccountOut)
def get_account_by_number(account_number: int, db: Session = Depends(get_db)):
    account = db.query(account_model.Account).filter(account_model.Account.accountNumber == str(account_number)).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# 📥 Get Single Account by ID
@router.get("/{account_id}", response_model=account_schema.AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(account_model.Account).filter(account_model.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# ✍️ Update Account
@router.put("/{account_id}", response_model=account_schema.AccountOut)
def update_account(account_id: int, update_data: account_schema.AccountUpdate, db: Session = Depends(get_db)):
    account = db.query(account_model.Account).filter(account_model.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if update_data.userID is not None:
        account.userID = update_data.userID
    if update_data.accountBalance is not None:
        account.accountBalance = update_data.accountBalance
    if update_data.approvedAccount is not None:
        account.approvedAccount = update_data.approvedAccount
    if update_data.created_at is not None:
        account.created_at = update_data.created_at
    db.commit()
    db.refresh(account)
    return account

# ❌ Delete Account
@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(account_model.Account).filter(account_model.Account.id == account_id).first()
    transaction = db.query(Transaction).filter(Transaction.accountID == account_id).all()
    card = db.query(Card).filter(Card.accountID == account_id).all()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if transaction :
        for transact in transaction:
            db.delete(transact)

    if card :
        for cd in card:
            db.delete(cd)
    
    db.delete(account)
    db.commit()
    return {"message": "Account deleted successfully"}
