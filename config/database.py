import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./verifintern.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # Needed only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get the DB session in API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()