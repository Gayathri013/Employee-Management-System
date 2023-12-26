from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker , declarative_base
from config import settings
from typing import Generator

SQLAlchemy_DB_URL = settings.datadase_url

engine = create_engine(SQLAlchemy_DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db() -> Generator:

    try:
        db = SessionLocal()
        yield db
        
    finally:
        db.close()