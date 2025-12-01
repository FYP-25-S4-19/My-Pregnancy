import random
from datetime import datetime

from faker import Faker
from sqlalchemy.orm import Session

from app.db.db_schema import CommentLike, CommunityThread, PregnantWoman, ThreadComment, User


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
        return all_community_threads

    @staticmethod
    def generate_thread_comments(
        db: Session,
        faker: Faker,
        all_users: list[User],
        all_community_threads: list[CommunityThread],
        max_comments_per_thread: int,
    ) -> list[ThreadComment]:
        print("Generating thread comments....")

        all_thread_comments: list[ThreadComment] = []
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
                all_thread_comments.append(comment)

        db.add_all(all_thread_comments)
        return all_thread_comments

    @staticmethod
    def generate_comment_likes(
        db: Session, all_mothers: list[PregnantWoman], all_thread_comments: list[ThreadComment]
    ) -> None:
        print("Generating comment likes.....")

        for comment in all_thread_comments:
            num_likes: int = random.randint(0, len(all_mothers))
            random_likers: list[PregnantWoman] = random.sample(all_mothers, num_likes)
            for mother in random_likers:
                comment.comment_likes.append(CommentLike(comment=comment, liker=mother))
                db.add(comment)
