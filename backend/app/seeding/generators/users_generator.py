from app.exceptions.general_exceptions import RoleNotFound
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db_schema import (
    VolunteerSpecialist,
    PregnantWoman,
    Admin,
    Role,
)
from faker import Faker
import random


class UsersGenerator:
    @staticmethod
    def generate_admins(db: Session, faker: Faker, password_hasher: PasswordHasher, count: int) -> list[Admin]:
        print("Generating users (Admins)....")

        admin_role: Role | None = db.query(Role).filter(Role.label == "Admin").first()
        if admin_role is None:
            raise RoleNotFound("Admin")

        all_admins: list[Admin] = []
        fake_username: str = faker.user_name()
        fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
        for _ in range(count):
            admin = Admin(
                username=fake_username,
                role=admin_role,
                email=faker.email(),
                password_hash=password_hasher.hash(fake_username),
                created_at=fake_created_at,
            )
            db.add(admin)
            all_admins.append(admin)
        db.commit()
        return all_admins

    @staticmethod
    def generate_pregnant_women(
        db: Session, faker: Faker, password_hasher: PasswordHasher, count: int
    ) -> list[PregnantWoman]:
        print("Generating users (Pregnant Women)....")

        pregnant_role: Role | None = db.query(Role).filter(Role.label == "PregnantWoman").first()
        if pregnant_role is None:
            raise RoleNotFound("PregnantWoman")

        all_preg_women: list[PregnantWoman] = []
        for _ in range(count):
            fake_username: str = faker.user_name()
            fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
            fake_due_date: datetime = fake_created_at + timedelta(days=random.randint(20, 260))

            preg_woman = PregnantWoman(
                username=fake_username,
                role=pregnant_role,
                email=faker.email(),
                password_hash=password_hasher.hash(fake_username),
                created_at=fake_created_at,
                due_date=fake_due_date,
            )
            db.add(preg_woman)
            all_preg_women.append(preg_woman)
        db.commit()
        return all_preg_women

    # TODO: Tightly coupled to medical credentials
    # @staticmethod
    # def generate_volunteer_specialists(
    #     db: Session, count: int, faker: Faker, password_hasher: PasswordHasher
    # ) -> list[VolunteerSpecialist]:
    #     print("Initializing Users (Volunteer Specialists)....")
    #
    #     specialist_role: Role | None = db.query(Role).filter(Role.label == "VolunteerSpecialist").first()
    #     if specialist_role is None:
    #         raise RoleNotFound("VolunteerSpecialist")
    #
    #     all_volunteer_specialists: list[VolunteerSpecialist] = []
    #     fake_username: str = faker.user_name()
    #     fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
    #     for _ in range(count):
    #         volunteer_specialist = VolunteerSpecialist(
    #             username=fake_username,
    #             role=specialist_role,
    #             email=faker.email(),
    #             password_hash=password_hasher.hash(fake_username),
    #             created_at=fake_created_at,
    #         )
    #         db.add(volunteer_specialist)
    #         all_volunteer_specialists.append(volunteer_specialist)
    #     db.commit()
    #     return all_volunteer_specialists
