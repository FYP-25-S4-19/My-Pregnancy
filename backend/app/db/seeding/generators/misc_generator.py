import random
from datetime import datetime, timedelta
from math import floor

from faker import Faker
from sqlalchemy.orm import Session

from app.db.db_schema import (
    Appointment,
    AppointmentStatus,
    KickTrackerDataPoint,
    KickTrackerSession,
    PregnantWoman,
    User,
    UserAppFeedback,
    VolunteerDoctor,
)


class MiscGenerator:
    @staticmethod
    def generate_user_app_feedback(db: Session, faker: Faker, all_users: list[User], fraction_of_mothers: float):
        print("Generating user app feedback....")

        sample_size: int = int(len(all_users) * max(min(fraction_of_mothers, 1), 0))
        rand_users: list[User] = random.sample(population=all_users, k=sample_size)
        for user in rand_users:
            user_feedback = UserAppFeedback(
                author=user, rating=random.randint(1, 5), content=faker.sentence(random.randint(1, 5))
            )
            db.add(user_feedback)

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

    @staticmethod
    def generate_kick_tracker_sessions(
        db: Session, faker: Faker, all_mothers: list[PregnantWoman]
    ) -> list[KickTrackerSession]:
        print("Generating kick tracker sessions....")

        sample_size: int = random.randint(0, len(all_mothers))
        mothers_sample: list[PregnantWoman] = random.sample(population=all_mothers, k=sample_size)

        kick_tracker_sessions: list[KickTrackerSession] = []
        for mother in mothers_sample:
            rand_session_count: int = random.randint(1, 5)
            for _ in range(rand_session_count):
                session_start: datetime = faker.date_time_between(
                    start_date=mother.created_at, end_date=datetime.now() - timedelta(days=1)
                )

                kick_session = KickTrackerSession(
                    mother=mother,
                    started_at=session_start,
                    ended_at=session_start + timedelta(minutes=random.randint(30, 150)),
                )

                rand_kick_count: int = random.randint(1, 18)
                for _ in range(rand_kick_count):
                    random_kick = KickTrackerDataPoint(
                        kick_at=faker.date_time_between(
                            start_date=kick_session.started_at, end_date=kick_session.ended_at
                        ),
                        session=kick_session,
                    )
                    kick_session.kicks.append(random_kick)
                kick_tracker_sessions.append(kick_session)

        db.add_all(kick_tracker_sessions)
        return kick_tracker_sessions
