from app.core.db_config import SessionLocal
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db_schema import User, Role
from sqlalchemy import text
from faker import Faker
import os

faker = Faker()


def clear_db(db: Session):
    # TODO
    pass


def initialize_roles(db: Session):
    role = Role(label="PregnantWoman")
    db.add(role)


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
