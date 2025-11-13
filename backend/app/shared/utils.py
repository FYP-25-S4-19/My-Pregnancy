from sqlalchemy.orm import Session
from sqlalchemy import text


def clear_db(db: Session):
    print("Clearing the database....\n")
    db.execute(text("SET session_replication_role = 'replica';"))  # Disable foreign key constraints

    table_names = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")).scalars().all()
    for table in table_names:  # Truncate all tables
        if table not in ["alembic_version"]:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))

    db.execute(text("SET session_replication_role = 'origin';"))  # Re-enable foreign key constraints
    db.commit()
