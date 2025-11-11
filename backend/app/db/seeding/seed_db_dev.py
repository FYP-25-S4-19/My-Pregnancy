from app.db.seeding.generators.journal_and_metrics_generator import JournalAndMetricsGenerator
from app.db.seeding.generators.forum_content_generator import ForumContentGenerator
from app.db.seeding.generators.edu_articles_generator import EduArticlesGenerator
from app.db.seeding.generators.defaults_generator import DefaultsGenerator
from app.db.seeding.generators.users_generator import UsersGenerator
from app.db.seeding.generators.misc_generator import MiscGenerator
from app.db.db_config import SessionLocal
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db.db_schema import (
    MedicalCredentialOption,
    VolunteerSpecialist,
    EduArticleCategory,
    CommunityThread,
    PregnantWoman,
    BinaryMetric,
    JournalEntry,
    EduArticle,
    Admin,
    User,
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

        # Generate users
        preg_women: list[PregnantWoman] = UsersGenerator.generate_pregnant_women(db_session, faker, password_hasher, 30)
        admins: list[Admin] = UsersGenerator.generate_admins(db_session, faker, password_hasher, 4)
        specialists: list[VolunteerSpecialist] = UsersGenerator.generate_volunteer_specialists(
            db_session, faker, password_hasher, med_cred_options, 12
        )
        all_users: list[User] = preg_women + admins + specialists

        # Generate forum content
        all_community_threads: list[CommunityThread] = ForumContentGenerator.generate_threads(
            db_session, faker, all_users, 35
        )
        ForumContentGenerator.generate_comments(db_session, faker, all_users, all_community_threads, 15)

        # Generation of journal entries (and corresponding 'random' metric logs)
        journal_entries: list[JournalEntry] = JournalAndMetricsGenerator.generate_journal_entries(
            db_session, faker, preg_women, 50
        )
        JournalAndMetricsGenerator.generate_journal_binary_metric_logs(db_session, journal_entries, all_metric_options)

        # Generation of educational articles
        edu_articles: list[EduArticle] = EduArticlesGenerator.generate_edu_articles(
            db_session, faker, edu_article_categories, 30
        )
        EduArticlesGenerator.generate_saved_edu_articles(db_session, edu_articles, preg_women)

        # Generation of miscellaneous content
        MiscGenerator.generate_user_feedback(db_session, faker, all_users, 15)
        MiscGenerator.generate_bump_entries(db_session, faker, preg_women)
        MiscGenerator.generate_consultations(db_session, faker, specialists, preg_women)

        print("Finished seeding the database!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
