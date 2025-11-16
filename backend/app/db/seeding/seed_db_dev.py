from faker import Faker
from sqlalchemy.orm import Session

from app.core.password_hasher_config import get_password_hasher
from app.db.db_config import SessionLocal
from app.db.db_schema import CommunityThread, EduArticle, JournalEntry
from app.db.seeding.generators.defaults_generator import DefaultsGenerator
from app.db.seeding.generators.edu_articles_generator import EduArticlesGenerator
from app.db.seeding.generators.forum_content_generator import ForumContentGenerator
from app.db.seeding.generators.journal_and_metrics_generator import JournalAndMetricsGenerator
from app.db.seeding.generators.misc_generator import MiscGenerator
from app.db.seeding.generators.recipes_generator import RecipesGenerator
from app.db.seeding.generators.users_generator import UsersGenerator
from app.shared.utils import clear_db

if __name__ == "__main__":
    db_session: Session = SessionLocal()
    try:
        faker = Faker()
        password_hasher = get_password_hasher()
        clear_db(db_session)

        # ------- Initialize defaults -------
        binary_metrics, scalar_metrics = DefaultsGenerator.generate_defaults(db_session)
        print("Finished seeding the database defaults!\n")

        # --------- Generate users ---------
        preg_women, doctors, nutritionists = UsersGenerator.generate_users(
            db=db_session,
            faker=faker,
            password_hasher=password_hasher,
            preg_women_profiles_filepath="./app/db/seeding/images/profiles/pregnant_women",
            doctor_profiles_filepath="./app/db/seeding/images/profiles/volunteer_doctors",
            nutritionists_profiles_filepath="./app/db/seeding/images/profiles/nutritionists",
            qualifications_filepath="./app/db/seeding/images/qualifications",
        )
        all_users = preg_women + doctors + nutritionists
        print("Finished seeding the database users!\n")

        # ------- Generate forum content --------
        all_community_threads: list[CommunityThread] = ForumContentGenerator.generate_threads(
            db_session, faker, all_users, 30
        )
        ForumContentGenerator.generate_comments(db_session, faker, all_users, all_community_threads, 15)
        print("Finished seeding forum content!\n")

        # ---- Generation of journal entries (and corresponding 'random' metric logs) -----
        journal_entries: list[JournalEntry] = JournalAndMetricsGenerator.generate_journal_entries(
            db_session, faker, preg_women, 8
        )
        JournalAndMetricsGenerator.generate_journal_metric_logs(
            db_session, journal_entries, binary_metrics, scalar_metrics
        )
        print("Finished seeding metric logs (binary, scalar, BP)!\n")

        # ------ Generation of educational articles ---------
        edu_articles: list[EduArticle] = EduArticlesGenerator.generate_edu_articles(db_session, faker, 30)
        EduArticlesGenerator.generate_saved_edu_articles(db_session, edu_articles, preg_women)
        print("Finished seeding educational article content!\n")

        # -------- Generation of recipe data ---------
        RecipesGenerator.generate_all_recipes(db_session)
        print("Finished seeding all recipes!\n")

        # ------- Generation of miscellaneous content -------
        MiscGenerator.generate_user_feedback(db_session, faker, all_users, 0.25)
        MiscGenerator.generate_appointments(db_session, faker, doctors, preg_women, 0.7)
        print("Finished seeding miscellaneous content!\n")

        print("Finished seeding the database!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
