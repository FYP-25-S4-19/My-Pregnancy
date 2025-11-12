from app.shared.S3StorageInterface import S3StorageInterface
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
            if not folder_item.name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            fake_created_at: datetime = faker.date_time_between(start_date="-3y", end_date="now")
            username = folder_item.stem  # Exclude the extension

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
            all_preg_women.append(preg_woman)
        db.commit()
        return all_preg_women

    @staticmethod
    def generate_volunteer_specialists(
        db: Session,
        faker: Faker,
        password_hasher: PasswordHasher,
        med_cred_options: list[MedicalCredentialOption],
        profile_img_folder: str,
        med_degrees_img_folder: str,
    ) -> list[VolunteerSpecialist]:
        if not os.path.exists(profile_img_folder):
            raise ValueError(f"Profile image folder does not exist: {profile_img_folder}")
        if not os.path.exists(med_degrees_img_folder):
            raise ValueError(f"Profile image folder does not exist: {med_degrees_img_folder}")

        print("Generating Users (Volunteer Specialists)....")
        specialist_role: Role | None = db.query(Role).filter(Role.label == "VolunteerSpecialist").first()
        if specialist_role is None:
            raise RoleNotFound("VolunteerSpecialist")

        # Randomly initialize a medical credential for this user (can be of any random type - doctor, nurse, etc....)
        # Don't initialize the 'credential_owner' yet, until specialist is created later....
        all_volunteer_specialists: list[VolunteerSpecialist] = []
        for folder_item in pathlib.Path(profile_img_folder).iterdir():
            if not folder_item.is_file():
                continue
            if not folder_item.name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            fullname = folder_item.stem
            fullname_parts = fullname.split("_")

            med_cred = MedicalCredential(
                credential_img_key="",  # Empty, for now.....
                credential_option=random.choice(med_cred_options),
            )
            db.add(med_cred)

            volunteer_specialist = VolunteerSpecialist(
                username=fullname,  # Feels like doctors really should be using their full name only
                first_name=fullname_parts[0],
                middle_name=fullname_parts[1] if len(fullname_parts) >= 3 else "",
                last_name=fullname_parts[2] if len(fullname_parts) >= 3 else fullname_parts[1],
                role=specialist_role,
                email=f"{fullname}@gmail.com",
                password_hash=password_hasher.hash(fullname),
                medical_credential=med_cred,
                created_at=faker.date_time_between(start_date="-3y", end_date="now"),
            )
            db.add(volunteer_specialist)
            db.flush()

            # Random image from "med_degrees_img_folder" for the medical credential
            degree_img_filepath = random.choice(list(pathlib.Path(med_degrees_img_folder).iterdir()))
            degree_s3_key = S3StorageInterface.put_med_degree_img_from_filepath(
                volunteer_specialist.id, str(degree_img_filepath)
            )
            if degree_s3_key is None:
                raise ValueError("Failed to upload medical degree image to S3 storage")
            volunteer_specialist.medical_credential.credential_img_key = degree_s3_key

            # Assign the profile picture
            profile_img_filepath = str(folder_item)
            profile_s3_key = S3StorageInterface.put_profile_img_from_filepath(
                volunteer_specialist.id, profile_img_filepath
            )
            if profile_s3_key is None:
                raise ValueError("Failed to upload profile image to S3 storage")
            volunteer_specialist.profile_img_key = profile_s3_key

            med_cred.credential_owner = volunteer_specialist
            all_volunteer_specialists.append(volunteer_specialist)
        db.commit()
        return all_volunteer_specialists

    # @staticmethod
    # def generate_admins(
    #     db: Session, faker: Faker, password_hasher: PasswordHasher, count: int
    # ) -> list[Admin]:
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
