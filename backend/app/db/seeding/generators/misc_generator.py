from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.db_schema import (
    AppointmentStatus,
    VolunteerDoctor,
    UserAppFeedback,
    PregnantWoman,
    Appointment,
    User,
)
from faker import Faker
from math import floor
import random


class MiscGenerator:
    @staticmethod
    def generate_user_feedback(db: Session, faker: Faker, all_users: list[User], fraction_of_mothers: float):
        print("Generating user feedback....")

        sample_size: int = int(len(all_users) * max(min(fraction_of_mothers, 1), 0))
        rand_users: list[User] = random.sample(population=all_users, k=sample_size)
        for user in rand_users:
            user_feedback = UserAppFeedback(
                author=user, rating=random.randint(1, 5), content=faker.sentence(random.randint(1, 5))
            )
            db.add(user_feedback)
        db.commit()

    @staticmethod
    def generate_appointments(
        db: Session,
        faker: Faker,
        all_doctors: list[VolunteerDoctor],
        all_mothers: list[PregnantWoman],
        fraction_of_mothers: float,
    ):
        print("Generating appointments....")

        mothers_sample_size = int(len(all_mothers) * max(min(fraction_of_mothers, 1), 0))
        mothers_sample: list[PregnantWoman] = random.sample(population=all_mothers, k=mothers_sample_size)
        for mother in mothers_sample:
            doctors_sample_size = random.randint(0, floor(len(all_doctors) * 0.3))
            doctors_sample: list[VolunteerDoctor] = random.sample(population=all_doctors, k=doctors_sample_size)
            for dr in doctors_sample:
                rand_time: datetime = faker.date_time_between(
                    start_date=mother.created_at,
                    end_date=(
                        mother.created_at + timedelta(days=random.randint(1, 15), minutes=random.randint(0, 1000))
                    ),
                )
                db.add(
                    Appointment(
                        volunteer_doctor=dr,
                        mother=mother,
                        start_time=rand_time,
                        status=random.choice(list(AppointmentStatus)),
                    )
                )
        db.commit()
