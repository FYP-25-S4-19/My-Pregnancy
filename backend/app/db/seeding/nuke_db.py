from app.db.db_config import engine
from app.db.db_schema import Base
from sqlalchemy import text

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
            conn.commit()
        Base.metadata.drop_all(engine)
    except Exception as e:
        print(f"Exception occurred while nuking database: {e}")
