from app.db.seeding.generators.defaults_generator import DefaultsGenerator
from app.db.db_config import SessionLocal
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db.db_schema import (
    MedicalCredentialOption,
    EduArticleCategory,
    BinaryMetric,
)
from sqlalchemy import text
from faker import Faker


def clear_db(db: Session):
    print("Clearing the database....")
    db.execute(text("SET session_replication_role = 'replica';"))  # Disable foreign key constraints

    table_names = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")).scalars().all()
    for table in table_names:  # Truncate all tables
        if table not in ["alembic_version"]:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))

    db.execute(text("SET session_replication_role = 'origin';"))  # Re-enable foreign key constraints
    db.commit()


if __name__ == "__main__":
    db_session: Session = SessionLocal()
    try:
        faker = Faker()
        password_hasher = PasswordHasher()

        clear_db(db_session)

        # Initialize defaults
        DefaultsGenerator.init_roles(db_session)
        med_cred_options: list[MedicalCredentialOption] = DefaultsGenerator.init_med_cred_options(db_session)
        edu_article_categories: list[EduArticleCategory] = DefaultsGenerator.init_edu_article_categories(db_session)
        DefaultsGenerator.init_binary_metric_categories(db_session)
        all_metric_options: list[BinaryMetric] = DefaultsGenerator.init_binary_metrics(db_session)

        print("Finished seeding the database!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
