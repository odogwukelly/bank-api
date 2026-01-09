from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# DATABASE_URL = "sqlite:///./banking.db"  # You can replace this with PostgreSQL later
DATABASE_URL = "postgresql://postgres:test123@localhost:5432/firmfrontierbankDB"  # You can replace this with PostgreSQL later
# DATABASE_URL = "postgresql://bankuser:test123@127.00.1:5432/firmfrontierbankDB"

engine = create_engine(
    DATABASE_URL
    # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
