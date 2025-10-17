import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or ""
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in '.env' file'")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    print(f"Calling 'get_db()', database URL is {DATABASE_URL}")
    db: Session = SessionLocal()
    try:
        res = db.execute(text("SELECT 1"))
        print("Result of test query: ", res)
        yield db
    finally:
        db.close()
