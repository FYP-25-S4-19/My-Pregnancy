from app.core.exceptions import RoleNotFound
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db.db_schema import (
    MedicalCredentialOption,
    VolunteerSpecialist,
    MedicalCredential,
    PregnantWoman,
    Admin,
    User,
    Role
)
from faker import Faker
import random


class UsersGenerator:
    @staticmethod
    def _create_unique_usernames(db: Session, faker: Faker, count: int) -> set[str]:
        existing_usernames = {row[0] for row in db.query(User.username).all()}
        new_usernames: set[str] = set()

        while len(new_usernames) < count:
            username = faker.user_name()
            if username not in existing_usernames and username not in new_usernames:
                new_usernames.add(username)

        return new_usernames

    @staticmethod
    def generate_admins(db: Session, faker: Faker, password_hasher: PasswordHasher, count: int) -> list[Admin]:
        print("Generating users (Admins)....")

        admin_role: Role | None = db.query(Role).filter(Role.label == "Admin").first()
        if admin_role is None:
            raise RoleNotFound("Admin")

        all_admins: list[Admin] = []
        fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
        for username in fake_usernames:
            admin = Admin(
                username=username,
                role=admin_role,
                email=f'{username}@gmail.com',
                password_hash=password_hasher.hash(username),
                created_at=faker.date_time_between(start_date="-3y", end_date="now"),
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
        fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
        for username in fake_usernames:
            fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
            preg_woman = PregnantWoman(
                username=username,
                role=pregnant_role,
                email=f'{username}@gmail.com',
                password_hash=password_hasher.hash(username),
                created_at=fake_created_at,
                due_date=fake_created_at + timedelta(days=random.randint(20, 260)),
            )
            db.add(preg_woman)
            all_preg_women.append(preg_woman)
        db.commit()
        return all_preg_women

    @staticmethod
    def generate_volunteer_specialists(
            db: Session,
            faker: Faker,
            password_hasher: PasswordHasher,
            med_cred_options: list[MedicalCredentialOption],
            count: int,
    ) -> list[VolunteerSpecialist]:
        print("Generating Users (Volunteer Specialists)....")

        specialist_role: Role | None = db.query(Role).filter(Role.label == "VolunteerSpecialist").first()
        if specialist_role is None:
            raise RoleNotFound("VolunteerSpecialist")

        # Randomly initialize a medical credential for this user (can be of any random type - doctor, nurse, etc....)
        # Don't initialize the 'credential_owner' yet, until specialist is created later....
        all_volunteer_specialists: list[VolunteerSpecialist] = []
        fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
        for username in fake_usernames:
            med_cred = MedicalCredential(
                credential_img_url="",  # Empty, for now.....
                credential_option=random.choice(med_cred_options),
            )
            volunteer_specialist = VolunteerSpecialist(
                username=username,
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                role=specialist_role,
                email=f'{username}@gmail.com',
                password_hash=password_hasher.hash(username),
                medical_credential=med_cred,
                created_at=faker.date_time_between(start_date="-3y", end_date="now"),
            )
            db.add(volunteer_specialist)
            all_volunteer_specialists.append(volunteer_specialist)
        db.commit()
        return all_volunteer_specialists
