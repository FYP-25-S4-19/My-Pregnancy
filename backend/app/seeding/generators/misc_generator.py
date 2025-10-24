from app.db_schema import User, UserFeedback
from sqlalchemy.orm import Session
from faker import Faker
import random


class MiscGenerator:
    @staticmethod
    def generate_user_feedback(db: Session, faker: Faker, all_users: list[User], count: int):
        sample_size = min(len(all_users), count)
        rand_users: list[User] = random.sample(population=all_users, k=sample_size)
        for user in rand_users:
            user_feedback = UserFeedback(
                author=user, rating=random.randint(1, 5), content=faker.sentence(random.randint(1, 5))
            )
            db.add(user_feedback)
        db.commit()
