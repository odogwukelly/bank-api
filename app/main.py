from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.router import account_router, card_router, getUser_router, login_router, otp_router, register_router, send_mail, support_router, transaction_router, updateUser_router
from fastapi.staticfiles import StaticFiles

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banking API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")

# Auth Routers
app.include_router(register_router.router, prefix="/api/users", tags=["Users Auth"])
app.include_router(login_router.router, prefix="/api/users", tags=["Users Auth"])
app.include_router(otp_router.router, prefix="/api/users/otp", tags=["Users Auth"])

# User Data Router
app.include_router(send_mail.router, prefix="/api/users", tags=["Send Mail"])
app.include_router(getUser_router.router, prefix="/api/users", tags=["Users Data"])
app.include_router(updateUser_router.router, prefix="/api/users/update", tags=["Users Data"])

app.include_router(account_router.router, prefix="/api/users/account", tags=["User Account"])

app.include_router(transaction_router.router, prefix="/api/users/transaction", tags=["User Transaction"])

app.include_router(support_router.router, prefix="/api/users", tags=["User Support"])

app.include_router(card_router.router, prefix="/api/users", tags=["User Card"])

@app.get("/api/")
def root():
    return {"message": "🚀 Welcome to Banking API"}
