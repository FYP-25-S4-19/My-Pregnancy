from app.db_schema import CommunityThread, User, ThreadComment
from sqlalchemy.orm import Session
from datetime import datetime
from faker import Faker
import random


class ForumContentGenerator:
    @staticmethod
    def generate_threads(db: Session, faker: Faker, all_users: list[User], count: int) -> list[CommunityThread]:
        print("Generating community threads....")

        all_community_threads: list[CommunityThread] = []
        for _ in range(count):
            user: User = random.choice(all_users)
            thread = CommunityThread(
                creator=user,
                title=faker.sentence(nb_words=random.randint(3, 9)),
                content=faker.paragraph(nb_sentences=random.randint(3, 10)),
                posted_at=faker.date_time_between(start_date=user.created_at, end_date=datetime.now()),
            )
            all_community_threads.append(thread)
            db.add(thread)
        db.commit()
        return all_community_threads

    @staticmethod
    def generate_comments(
        db: Session,
        faker: Faker,
        all_users: list[User],
        all_community_threads: list[CommunityThread],
        max_comments_per_thread: int,
    ) -> None:
        print("Generating thread comments....")

        for community_thread in all_community_threads:
            random_user: User = random.choice(all_users)
            num_comments = random.randint(0, max_comments_per_thread)
            for _ in range(num_comments):
                comment = ThreadComment(
                    thread=community_thread,
                    commenter=random_user,
                    commented_at=faker.date_time_between(start_date="-2y", end_date=datetime.now()),
                    content=faker.paragraph(nb_sentences=random.randint(2, 12)),
                )
                db.add(comment)
        db.commit()
