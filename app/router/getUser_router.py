from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.account_model import Account
from app.model.transaction_model import Transaction
from app.model.user_model import User
from app.schema.getUser_schema import getAllUserResponse, getUserResponse
from app.utils.image_upload import delete_image, save_image
import os
from app.baseUrl import BaseUrl

SERVER_URL = BaseUrl.profileUrl


router = APIRouter()


@router.put("/upload-profile/{user_id}")
async def upload_profile_image(user_id: int, file: UploadFile, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Delete old image if it exists
    if user.profile_image:
        delete_image(user.profile_image)

    # ✅ Save new image to 'images/profiles/'
    relative_path = save_image(file, subfolder="profiles")

    # ✅ Build public URL for frontend
    image_url = f"{SERVER_URL}/{relative_path.replace(os.sep, '/')}"  # normalize slashes

    # ✅ Update user record
    user.profile_image = relative_path
    user.profileUrl = image_url
    db.commit()
    db.refresh(user)

    return {
        "message": "Profile image updated successfully",
        "image_url": image_url
    }


@router.delete("/delete-profile/{user_id}")
async def delete_profile_image(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile_image:
        deleted = delete_image(user.profile_image)
        if deleted:
            user.profile_image = None
            db.commit()
            return {"message": "Profile image deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Image not found")

    raise HTTPException(status_code=400, detail="User has no profile image")



@router.get("/get/all", response_model=getAllUserResponse)
def get_all_user_data(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    user_list = []

    for u in users:
        # Fetch all accounts linked to this user
        user_accounts = db.query(Account).filter(Account.userID == u.id).all()
        
        # Calculate total balance for all accounts
        total_balance = sum([acc.accountBalance for acc in user_accounts])
        
        # Append user info with total balance
        user_list.append({
            "id": u.id,
            "fullName": u.fullName,
            "email": u.email,
            "totalBalance": total_balance,
            "firstName": u.firstName,
            "lastName": u.lastName,
            "dob": u.dob,
            "address": u.address,
            "isAdmin": u.isAdmin,
            "isEmailVerified": u.isEmailVerified,
            "mobile": u.mobile,
            "created_at": u.created_at,
            "updated_at": u.updated_at,
            "reviewDuration" : u.reviewDuration,
            "errorMsg" : u.errorMsg,
            "transferOTP" : u.transferOTP,
            "hashedPassword": u.hashedPassword,
            "allowValidation" : u.allowValidation,
            "allowTransfer" : u.allowTransfer,
            "pin": u.pin,
            "hasSetPin": u.hasSetPin,
            "profile_image": u.profile_image,
            "profileUrl": u.profileUrl

        })

    # Return users with count
    return {
        "totalUsers": len(users),
        "userData": user_list
    }


@router.get("/get/{user_id}", response_model=getUserResponse)
def get_user_data(user_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.userID == user_id).all()
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        user_accounts = db.query(Account).filter(Account.userID == user.id).all()
        total_balance = sum([acc.accountBalance for acc in user_accounts])

        user_data = {
            "id": user.id,
            "fullName": user.fullName,
            "email": user.email,
            "totalBalance": total_balance,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "dob": user.dob,
            "address": user.address,
            "isAdmin": user.isAdmin,
            "isEmailVerified": user.isEmailVerified,
            "mobile": user.mobile,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "hashedPassword": user.hashedPassword,
            "pin": user.pin,
            "hasSetPin": user.hasSetPin,
            "profile_image": user.profile_image,
            "profileUrl": user.profileUrl,
            "reviewDuration" : user.reviewDuration,
            "errorMsg" : user.errorMsg,
            "transferOTP" : user.transferOTP,
            "allowValidation" : user.allowValidation,
            "allowTransfer" : user.allowTransfer,
        }

        # return {"userData": [user_data], "totalUsers": 1}
    return { "userData": user_data, "userAccount": account }


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    account = db.query(Account).filter(Account.userID == user_id).all()
    transaction = db.query(Transaction).filter(Transaction.userID == user_id).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.profile_image:
        try:
            delete_image(user.profile_image)  # remove from disk
            print(f"Image deleted for user {user.fullName},")
        except Exception as e:
            print(f"Error deleting profile image: {e}")

    if account :
        for acc in account:
            db.delete(acc)

    if transaction :
        for transact in transaction:
            db.delete(transact)

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}











