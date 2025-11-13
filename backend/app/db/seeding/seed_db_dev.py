from app.db.db_schema import PregnantWoman, Admin, VolunteerDoctor, Nutritionist
from app.db.seeding.generators.defaults_generator import DefaultsGenerator
from app.db.seeding.generators.users_generator import UsersGenerator
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
        DefaultsGenerator.generate_defaults(db_session)
        print("Finished seeding the database defaults!")

        # Generate users
        preg_women, doctors, nutritionists = UsersGenerator.generate_users(
            db=db_session,
            faker=faker,
            password_hasher=password_hasher,
            preg_women_profiles_filepath="./app/db/seeding/images/profiles/pregnant_women",
            doctor_profiles_filepath="./app/db/seeding/images/profiles/volunteer_doctors",
            nutritionists_profiles_filepath="./app/db/seeding/images/profiles/nutritionists",
            qualifications_filepath="./app/db/seeding/images/qualifications",
        )
        print("Finished seeding the dev database users!")
        # admins: list[Admin] = UsersGenerator(
        #     db_session, faker, password_hasher, 4
        # )
        # all_users: list[User] = preg_women + admins + specialists

        # # Generate forum content
        # all_community_threads: list[CommunityThread] = ForumContentGenerator.generate_threads(
        #     db_session, faker, all_users, 35
        # )
        # ForumContentGenerator.generate_comments(db_session, faker, all_users, all_community_threads, 15)
        #
        # # Generation of journal entries (and corresponding 'random' metric logs)
        # journal_entries: list[JournalEntry] = JournalAndMetricsGenerator.generate_journal_entries(
        #     db_session, faker, preg_women, 50
        # )
        # JournalAndMetricsGenerator.generate_journal_binary_metric_logs(db_session, journal_entries, all_metric_options)
        #
        # # Generation of educational articles
        # edu_articles: list[EduArticle] = EduArticlesGenerator.generate_edu_articles(
        #     db_session, faker, edu_article_categories, 30
        # )
        # EduArticlesGenerator.generate_saved_edu_articles(db_session, edu_articles, preg_women)
        #
        # # Generation of miscellaneous content
        # MiscGenerator.generate_user_feedback(db_session, faker, all_users, 15)
        # MiscGenerator.generate_bump_entries(db_session, faker, preg_women)
        # MiscGenerator.generate_consultations(db_session, faker, specialists, preg_women)
        #
        print("Finished seeding the database!")
    except Exception as e:
        print(f"Exception occurred while seeding database: {e}")
    finally:
        db_session.close()
