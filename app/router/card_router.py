from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.card_model import Card
from app.model.transaction_model import Transaction
from app.schema.card_schema import CardCreate, CardResponse, CardUpdate
from app.utils.helper import generate_card_number, generate_cvv
from app.utils.queryHelper import get_user_by_id

router = APIRouter()
MaxLimit = 3

# ✅ Create Card
@router.post("/card/create")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    cardCount = db.query(Card).filter(Card.userID == card.userID).count()

    if (cardCount + 1) > MaxLimit :
        raise HTTPException(status_code=400, detail=" Card Max Limit Reached")
    
    card_number = generate_card_number()
    cvv = generate_cvv()

    newCard = Card(
        userID=card.userID,
        accountID=card.accountID,
        cardNumber=card_number,
        cardType=card.cardType,
        cardBalance=card.cardBalance,
        cardName=card.cardName,
        cvv=cvv,
        expiresAt= card.expiresAt
    )
    db.add(newCard)
    db.commit()
    db.refresh(newCard)
    return newCard


@router.get("/card/all", response_model=list[CardResponse])
def get_all_cards(user_id: int = Query(None), db: Session = Depends(get_db)):
    if user_id is not None:
        # Filter by user_id if provided
        cards = db.query(Card).filter(Card.userID == user_id).all()
    else:
        # Otherwise return all accounts
        cards = db.query(Card).all()
    return cards


@router.get("/card/{card_id}", response_model=CardResponse)
def get_card_by_id(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card




@router.put("/card/{card_id}", response_model=CardResponse)
def update_card_by_id(card_id: int, update_data: CardUpdate, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    

    if update_data.userID is not None:
        card.userID = update_data.userID
    if update_data.cardBalance is not None:
        card.cardBalance = update_data.cardBalance
    if update_data.created_at is not None:
        card.created_at = update_data.created_at
    if update_data.cvv is not None:
        card.cvv = update_data.cvv
    if update_data.expiresAt is not None:
        card.expiresAt = update_data.expiresAt

    db.commit()
    db.refresh(card)
    return card



@router.delete("/card/{card_id}")
def delete_card_by_id(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    transaction = db.query(Transaction).filter(Transaction.accountID == card.accountID).all()
    if transaction :
        for transact in transaction:
            db.delete(transact)
    
    db.delete(card)
    db.commit()
    return {"message": "Card deleted successfully"}
