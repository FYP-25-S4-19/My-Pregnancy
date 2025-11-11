from app.db.db_config import engine
from sqlalchemy import text

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Dropping schema public CASCADE...")
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            print("Recreating schema public...")
            conn.execute(text("CREATE SCHEMA public;"))
    except Exception as e:
        print(f"Exception occurred while nuking database: {e}")
