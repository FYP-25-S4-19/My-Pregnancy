from sqlalchemy import text

from app.db.db_config import engine

if __name__ == "__main__":
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
        print("Database has been nuked!")
    except Exception as e:
        print(f"Exception occurred while nuking database: {e}")
