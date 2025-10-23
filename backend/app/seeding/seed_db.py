from app.core.db_config import SessionLocal
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db_schema import User, Role
from sqlalchemy import text
from faker import Faker
import os

faker = Faker()
password_hasher = PasswordHasher()


def clear_db(db: Session):
    table_names = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")).scalars().all()

    # Disable foreign key constraints
    db.execute(text("SET session_replication_role = 'replica';"))

    # Truncate all tables
    for table in table_names:
        if table not in ["alembic_version"]:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))

    # Re-enable foreign key constraints
    db.execute(text("SET session_replication_role = 'origin';"))
    db.commit()


def initialize_roles(db: Session):
    for role in ["PregnantWoman", "VolunteerSpecialist", "Admin", "Nutritionist"]:
        role = Role(label=role)
        db.add(role)
    db.commit()


if __name__ == "__main__":
    db_session: Session = SessionLocal()
    try:
        clear_db(db_session)
        initialize_roles(db_session)

        db_session.commit()
        print("Finished seeding the database!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
