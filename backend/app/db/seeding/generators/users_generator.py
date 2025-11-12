from app.shared.S3StorageInterface import S3StorageInterface
from app.core.exceptions import RoleNotFound
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db.db_schema import (
    PregnantWoman,
    Role,
)
from faker import Faker
import pathlib
import random
import os


class UsersGenerator:
    @staticmethod
    def generate_pregnant_women(
        db: Session,
        faker: Faker,
        password_hasher: PasswordHasher,
        profile_img_folder: str,
    ) -> list[PregnantWoman]:
        if not os.path.exists(profile_img_folder):
            raise ValueError(f"Profile image folder does not exist: {profile_img_folder}")

        print("Generating users (Pregnant Women)....")
        pregnant_role: Role | None = db.query(Role).filter(Role.label == "PregnantWoman").first()
        if pregnant_role is None:
            raise RoleNotFound("PregnantWoman")

        all_preg_women: list[PregnantWoman] = []
        for folder_item in pathlib.Path(profile_img_folder).iterdir():
            if not folder_item.is_file():
                continue
            full_filepath: str = folder_item.name
            if not full_filepath.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
            username = folder_item.stem # Exclude the extension

            preg_woman = PregnantWoman(
                username=username,
                role=pregnant_role,
                email=f"{username}@gmail.com",
                password_hash=password_hasher.hash(username),
                created_at=fake_created_at,
                due_date=(  # 30% chance of the "due date" being null
                    fake_created_at + timedelta(days=random.randint(20, 260)) if random.random() > 0.3 else None
                ),
            )
            db.add(preg_woman)
            db.flush()

            obj_key = S3StorageInterface.put_profile_img_from_filepath(preg_woman.id, str(folder_item))
            preg_woman.profile_img_key = obj_key
            # print("GenPregWom, Obj Key: ", obj_key)
            all_preg_women.append(preg_woman)
        db.commit()
        return all_preg_women

    # @staticmethod
    # def _create_unique_usernames(db: Session, faker: Faker, count: int) -> set[str]:
    #     existing_usernames = {row[0] for row in db.query(User.username).all()}
    #     new_usernames: set[str] = set()
    #
    #     while len(new_usernames) < count:
    #         username = faker.user_name()
    #         if username not in existing_usernames and username not in new_usernames:
    #             new_usernames.add(username)
    #
    #     return new_usernames
    #
    # @staticmethod
    # def generate_admins(db: Session, faker: Faker, password_hasher: PasswordHasher, count: int) -> list[Admin]:
    #     print("Generating users (Admins)....")
    #
    #     admin_role: Role | None = db.query(Role).filter(Role.label == "Admin").first()
    #     if admin_role is None:
    #         raise RoleNotFound("Admin")
    #
    #     all_admins: list[Admin] = []
    #     fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
    #     for username in fake_usernames:
    #         admin = Admin(
    #             username=username,
    #             role=admin_role,
    #             email=f'{username}@gmail.com',
    #             password_hash=password_hasher.hash(username),
    #             created_at=faker.date_time_between(start_date="-3y", end_date="now"),
    #         )
    #         db.add(admin)
    #         all_admins.append(admin)
    #     db.commit()
    #     return all_admins
    #
    # @staticmethod
    # def generate_pregnant_women(
    #         db: Session, faker: Faker, password_hasher: PasswordHasher, count: int
    # ) -> list[PregnantWoman]:
    #     print("Generating users (Pregnant Women)....")
    #
    #     pregnant_role: Role | None = db.query(Role).filter(Role.label == "PregnantWoman").first()
    #     if pregnant_role is None:
    #         raise RoleNotFound("PregnantWoman")
    #
    #     all_preg_women: list[PregnantWoman] = []
    #     fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
    #     for username in fake_usernames:
    #         fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
    #         preg_woman = PregnantWoman(
    #             username=username,
    #             role=pregnant_role,
    #             email=f'{username}@gmail.com',
    #             password_hash=password_hasher.hash(username),
    #             created_at=fake_created_at,
    #             due_date=fake_created_at + timedelta(days=random.randint(20, 260)),
    #         )
    #         db.add(preg_woman)
    #         all_preg_women.append(preg_woman)
    #     db.commit()
    #     return all_preg_women
    #
    # @staticmethod
    # def generate_volunteer_specialists(
    #         db: Session,
    #         faker: Faker,
    #         password_hasher: PasswordHasher,
    #         med_cred_options: list[MedicalCredentialOption],
    #         count: int,
    # ) -> list[VolunteerSpecialist]:
    #     print("Generating Users (Volunteer Specialists)....")
    #
    #     specialist_role: Role | None = db.query(Role).filter(Role.label == "VolunteerSpecialist").first()
    #     if specialist_role is None:
    #         raise RoleNotFound("VolunteerSpecialist")
    #
    #     # Randomly initialize a medical credential for this user (can be of any random type - doctor, nurse, etc....)
    #     # Don't initialize the 'credential_owner' yet, until specialist is created later....
    #     all_volunteer_specialists: list[VolunteerSpecialist] = []
    #     fake_usernames: set[str] = UsersGenerator._create_unique_usernames(db, faker, count)
    #     for username in fake_usernames:
    #         med_cred = MedicalCredential(
    #             credential_img_url="",  # Empty, for now.....
    #             credential_option=random.choice(med_cred_options),
    #         )
    #         volunteer_specialist = VolunteerSpecialist(
    #             username=username,
    #             first_name=faker.first_name(),
    #             last_name=faker.last_name(),
    #             role=specialist_role,
    #             email=f'{username}@gmail.com',
    #             password_hash=password_hasher.hash(username),
    #             medical_credential=med_cred,
    #             created_at=faker.date_time_between(start_date="-3y", end_date="now"),
    #         )
    #         db.add(volunteer_specialist)
    #         all_volunteer_specialists.append(volunteer_specialist)
    #     db.commit()
    #     return all_volunteer_specialists
