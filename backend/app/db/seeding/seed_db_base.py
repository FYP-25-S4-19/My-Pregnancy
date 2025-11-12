from app.db.seeding.generators.defaults_generator import DefaultsGenerator
from app.core.password_hasher_config import get_password_hasher
from app.db.db_config import SessionLocal
from app.shared.utils import clear_db
from sqlalchemy.orm import Session
from faker import Faker


if __name__ == "__main__":
    db_session: Session = SessionLocal()
    try:
        faker = Faker()
        password_hasher = get_password_hasher()

        clear_db(db_session)

        # Initialize defaults
        med_cred_options, edu_article_categories, all_metric_options = DefaultsGenerator.generate_defaults(db_session)
        print("Finished seeding the database defaults!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
