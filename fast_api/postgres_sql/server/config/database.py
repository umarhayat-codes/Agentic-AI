from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(DATABASE_URL)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
