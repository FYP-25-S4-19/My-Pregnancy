from fastapi import FastAPI

from sqlalchemy import text
from app.db_config import SessionLocal
from app.entities.educational_articles.edu_articles_router import edu_articles_router


app = FastAPI()
app.include_router(edu_articles_router)


def test_connection():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT version()"))
        version = result.scalar()
        print("PostgreSQL version:", version)
    except Exception as e:
        print(f"Exception while connecting....{e}")
    finally:
        db.close()


@app.get("/")
def index():
    print("Testing connection....")
    print(test_connection())
    return "Hello World"
