from datetime import datetime, timedelta
from typing import Any, Generator

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import TokenData
from app.core.settings import settings
from app.db.db_config import get_db
from app.db.db_schema import (
    Admin,
    Base,
    DoctorQualification,
    DoctorQualificationOption,
    Nutritionist,
    NutritionistQualification,
    NutritionistQualificationOption,
    PregnantWoman,
    UserRole,
    VolunteerDoctor,
)
from app.main import app
from app.shared.utils import create_access_token

# # Use an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, Any, None]:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, Any, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin(db_session: Session) -> Generator[Admin, Any, None]:
    admin = Admin(
        username="test_admin", email="admin@test.com", password_hash="hashed_password_123", role=UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    yield admin


@pytest.fixture(scope="function")
def volunteer_doctor(db_session: Session) -> Generator[VolunteerDoctor, Any, None]:
    qualification = DoctorQualification(qualification_option=DoctorQualificationOption.MD)
    db_session.add(qualification)
    db_session.flush()

    doctor = VolunteerDoctor(
        username="test_doctor",
        role=UserRole.VOLUNTEER_DOCTOR,
        email="doctor@test.com",
        password_hash="hashed_password_123",
        first_name="John",
        last_name="Doe",
        qualification_id=qualification.id,
        is_verified=True,
    )
    db_session.add(doctor)
    db_session.commit()
    yield doctor


@pytest.fixture(scope="function")
def pregnant_woman(db_session: Session) -> Generator[PregnantWoman, Any, None]:
    mother = PregnantWoman(
        username="test_mother",
        role=UserRole.PREGNANT_WOMAN,
        email="unique_mail@gmail.com",
        password_hash="hashed_password_456",
    )
    db_session.add(mother)
    db_session.commit()
    yield mother


@pytest.fixture(scope="function")
def nutritionist(db_session: Session) -> Generator[Nutritionist, Any, None]:
    qualification = NutritionistQualification(
        qualification_option=NutritionistQualificationOption.CERTIFIED_NUTRITIONIST
    )
    db_session.add(qualification)
    db_session.flush()

    nutritionist = Nutritionist(
        username="test_nutritionist",
        first_name="John",
        last_name="Doe",
        role=UserRole.NUTRITIONIST,
        email="unique_mail@gmail.com",
        password_hash="hashed_password_789",
        qualification_id=qualification.id,
        is_verified=True,
    )
    db_session.add(nutritionist)
    db_session.commit()
    yield nutritionist


@pytest.fixture(scope="function")
def authenticated_admin_client(client: TestClient, admin: Admin) -> Generator[tuple[TestClient, Admin], Any, None]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(admin.id),
            role=admin.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"

    yield client, admin
    client.headers.pop("Authorization", None)


@pytest.fixture(scope="function")
def authenticated_doctor_client(
    client: TestClient, volunteer_doctor: VolunteerDoctor
) -> Generator[tuple[TestClient, VolunteerDoctor], Any, None]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(volunteer_doctor.id),
            role=volunteer_doctor.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"

    yield client, volunteer_doctor
    client.headers.pop("Authorization", None)


@pytest.fixture(scope="function")
def authenticated_pregnant_woman_client(
    client: TestClient, pregnant_woman: PregnantWoman
) -> Generator[tuple[TestClient, PregnantWoman], Any, None]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(pregnant_woman.id),
            role=pregnant_woman.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"

    yield client, pregnant_woman
    client.headers.pop("Authorization", None)


@pytest.fixture(scope="function")
def authenticated_nutritionist_client(
    client: TestClient, nutritionist: Nutritionist
) -> Generator[tuple[TestClient, Nutritionist], Any, None]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(nutritionist.id),
            role=nutritionist.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"

    yield client, nutritionist
    client.headers.pop("Authorization", None)


@pytest.fixture(scope="session")
def img_file_fixture() -> dict[str, tuple[str, bytes, str]]:
    return {"img_data": ("test_image.jpg", b"fake image bytes here", "image/jpeg")}
