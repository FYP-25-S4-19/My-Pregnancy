from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.db_schema import (
    VolunteerSpecialist,
    PregnantWoman,
    ConsultStatus,
    Consultation,
    UserFeedback,
    User,
    BumpEntry,
)
from faker import Faker
from math import floor
import random


class MiscGenerator:
    @staticmethod
    def generate_user_feedback(db: Session, faker: Faker, all_users: list[User], count: int):
        print("Generating user feedback....")

        sample_size = min(len(all_users), count)
        rand_users: list[User] = random.sample(population=all_users, k=sample_size)
        for user in rand_users:
            user_feedback = UserFeedback(
                author=user, rating=random.randint(1, 5), content=faker.sentence(random.randint(1, 5))
            )
            db.add(user_feedback)
        db.commit()

    @staticmethod
    def generate_bump_entries(db: Session, faker: Faker, all_mothers: list[PregnantWoman]) -> None:
        print("Generating bump entries.....")

        mothers_sample_size: int = random.randint(0, len(all_mothers))
        mothers_sample: list[PregnantWoman] = random.sample(population=all_mothers, k=mothers_sample_size)
        for mother in mothers_sample:
            bump_entry = BumpEntry(
                uploader=mother,
                bump_img_url="",  # Leave empty for now
                date=faker.date_time_between(start_date=mother.created_at, end_date=datetime.now()),
            )
            db.add(bump_entry)
        db.commit()

    @staticmethod
    def generate_consultations(
        db: Session, faker: Faker, all_specialists: list[VolunteerSpecialist], all_mothers: list[PregnantWoman]
    ):
        print("Generating consultations....")

        mothers_sample_size: int = random.randint(0, len(all_mothers))
        mothers_sample: list[PregnantWoman] = random.sample(population=all_mothers, k=mothers_sample_size)
        for mother in mothers_sample:
            specialists_sample_size: int = random.randint(0, floor(len(all_specialists) * 0.7))
            specialists_sample: list[VolunteerSpecialist] = random.sample(
                population=all_specialists, k=specialists_sample_size
            )
            for specialist in specialists_sample:
                rand_time: datetime = faker.date_time_between(
                    start_date=mother.created_at,
                    end_date=(
                        mother.created_at + timedelta(days=random.randint(1, 15), minutes=random.randint(0, 1000))
                    ),
                )
                consult = Consultation(
                    volunteer_specialist=specialist,
                    mother=mother,
                    start_time=rand_time,
                    status=random.choice([ConsultStatus.MISSED, ConsultStatus.PENDING, ConsultStatus.COMPLETED]),
                )
                db.add(consult)
        db.commit()
