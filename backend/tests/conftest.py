import uuid
from datetime import datetime, timedelta
from typing import Any, Callable, Generator

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

# Use an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ========================================================================
# ========================== MISC FIXTURES ===============================
# ========================================================================
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


@pytest.fixture(scope="session")
def img_file_fixture() -> dict[str, tuple[str, bytes, str]]:
    return {"img_data": ("test_image.jpg", b"fake image bytes here", "image/jpeg")}


# ========================================================================
# ========================== ADMIN FIXTURES ==============================
# ========================================================================
@pytest.fixture(scope="function")
def admin(db_session: Session) -> Generator[Admin, Any, None]:
    admin = Admin(
        username="test_admin", email="admin@test.com", password_hash="hashed_password_123", role=UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    yield admin


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


# ========================================================================
# ===================== VOLUNTEER DOCTOR FIXTURES ========================
# ========================================================================
@pytest.fixture(scope="function")
def volunteer_doctor_factory(db_session: Session) -> Generator[Callable[..., VolunteerDoctor], Any, None]:
    def _create_doctor(**kwargs) -> VolunteerDoctor:
        unique_id = str(uuid.uuid4())

        # Create qualification if not provided
        if "qualification_id" not in kwargs:
            qualification = DoctorQualification(qualification_option=DoctorQualificationOption.MD)
            db_session.add(qualification)
            db_session.flush()
            kwargs["qualification_id"] = qualification.id

        defaults = {
            "username": f"doctor_{unique_id}",
            "role": UserRole.VOLUNTEER_DOCTOR,
            "email": f"doctor_{unique_id}@test.com",
            "password_hash": "hashed_password_123",
            "first_name": "John",
            "last_name": "Doe",
            "is_verified": True,
        }

        user_data = defaults | kwargs
        doctor = VolunteerDoctor(**user_data)
        db_session.add(doctor)
        db_session.commit()
        return doctor

    return _create_doctor


@pytest.fixture(scope="function")
def volunteer_doctor(volunteer_doctor_factory: Callable[..., VolunteerDoctor]) -> VolunteerDoctor:
    return volunteer_doctor_factory()


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


# ========================================================================
# ====================== PREGNANT WOMAN FIXTURES =========================
# ========================================================================
@pytest.fixture(scope="function")
def pregnant_woman_factory(db_session: Session) -> Generator[Callable[..., PregnantWoman], Any, None]:
    def _create_woman(**kwargs) -> PregnantWoman:
        unique_id = str(uuid.uuid4())
        defaults = {
            "username": f"mother_{unique_id}",
            "role": UserRole.PREGNANT_WOMAN.value,
            "email": f"mother_{unique_id}@test.com",
            "password_hash": "hashed_password_456",
        }

        user_data = defaults | kwargs
        mother = PregnantWoman(**user_data)
        db_session.add(mother)
        db_session.commit()
        return mother

    return _create_woman


@pytest.fixture(scope="function")
def pregnant_woman(pregnant_woman_factory: Callable[..., PregnantWoman]) -> PregnantWoman:
    return pregnant_woman_factory()


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


# ========================================================================
# ====================== NUTRITIONIST FIXTURES ===========================
# ========================================================================
@pytest.fixture(scope="function")
def nutritionist_factory(db_session: Session) -> Generator[Callable[..., Nutritionist], Any, None]:
    def _create_nutritionist(**kwargs) -> Nutritionist:
        unique_id = str(uuid.uuid4())

        # Create qualification if not provided
        if "qualification_id" not in kwargs:
            qualification = NutritionistQualification(
                qualification_option=NutritionistQualificationOption.CERTIFIED_NUTRITIONIST
            )
            db_session.add(qualification)
            db_session.flush()
            kwargs["qualification_id"] = qualification.id

        defaults = {
            "username": f"nutritionist_{unique_id}",
            "role": UserRole.NUTRITIONIST,
            "email": f"nutritionist_{unique_id}@test.com",
            "password_hash": "hashed_password_789",
            "first_name": "Jane",
            "last_name": "Smith",
            "is_verified": True,
        }

        user_data = defaults | kwargs
        nutritionist = Nutritionist(**user_data)
        db_session.add(nutritionist)
        db_session.commit()
        return nutritionist

    return _create_nutritionist


@pytest.fixture(scope="function")
def nutritionist(nutritionist_factory: Callable[..., Nutritionist]) -> Nutritionist:
    return nutritionist_factory()


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
