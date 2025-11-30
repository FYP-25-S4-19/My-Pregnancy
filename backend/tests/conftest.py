import uuid
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Awaitable, Callable

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.pool import StaticPool

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

# Use an in-memory SQLite database for testing with aiosqlite
# check_same_thread=False is needed for SQLite with async
engine: AsyncEngine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ========================================================================
# ========================== MISC FIXTURES ===============================
# ========================================================================
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def img_file_fixture() -> tuple[str, bytes, str]:
    """
    If you have a 'multipart/form-data' endpoint that requires an image upload,
    you can use this fixture to provide a valid PNG image file for testing.
    ...
    Say that your endpoint accepts a parameter named `le_random_image: UploadFile = File(...)`,
    then in your test you can pass it in like so:
    ...
    async def test_your_endpoint(client: AsyncClient, img_file_fixture: tuple[str, bytes, str]):
        file_name, file_bytes, content_type = img_file_fixture
        response = await client.post(
            "/your-endpoint",
            files={"le_random_image": (file_name, file_bytes, content_type)},
        )
    """
    valid_png = (  # Minimal 1x1 PNG
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return ("test_image.png", valid_png, "image/png")


# ========================================================================
# ========================== ADMIN FIXTURES ==============================
# ========================================================================
CreateAdminCallable = Callable[
    ...,  # Accepts any keyword arguments (**kwargs)
    Awaitable[Admin],  # Must return an awaitable object (a coroutine) that resolves to Admin
]


@pytest_asyncio.fixture(scope="function")
async def admin_factory(db_session: AsyncSession, **kwargs: Any) -> CreateAdminCallable:
    async def _create_admin(**kwargs) -> Admin:
        unique_id = str(uuid.uuid4())
        defaults = {
            "role": UserRole.ADMIN,
            "email": f"admin_{unique_id}@test.com",
            "hashed_password": "hashed_password_123",
            "first_name": "Admin",
            "last_name": "McAdminface",
        }

        user_data = defaults | kwargs
        admin = Admin(**user_data)
        db_session.add(admin)
        await db_session.commit()
        return admin

    return _create_admin


@pytest_asyncio.fixture(scope="function")
async def admin(admin_factory: CreateAdminCallable) -> Admin:
    return await admin_factory()


@pytest_asyncio.fixture(scope="function")
async def authenticated_admin_client(client: AsyncClient, admin: Admin) -> tuple[AsyncClient, Admin]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(admin.id),
            role=admin.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"
    return client, admin


# ========================================================================
# ===================== VOLUNTEER DOCTOR FIXTURES ========================
# ========================================================================
CreateDoctorCallable = Callable[
    ...,  # Accepts any keyword arguments (**kwargs)
    Awaitable[VolunteerDoctor],  # Must return an awaitable object (a coroutine) that resolves to VolunteerDoctor
]


@pytest_asyncio.fixture(scope="function")
async def volunteer_doctor_factory(db_session: AsyncSession) -> CreateDoctorCallable:
    async def _create_doctor(**kwargs) -> VolunteerDoctor:
        unique_id = str(uuid.uuid4())

        if "qualification" not in kwargs:
            qualification = DoctorQualification(qualification_option=DoctorQualificationOption.MD)
        else:
            qualification = kwargs.pop("qualification")

        defaults = {
            "role": UserRole.VOLUNTEER_DOCTOR,
            "email": f"doctor_{unique_id}@test.com",
            "hashed_password": "hashed_password_123",
            "first_name": "John",
            "last_name": "Doe",
        }

        user_data = defaults | kwargs
        doctor = VolunteerDoctor(**user_data)
        doctor.qualification = qualification

        db_session.add(doctor)
        await db_session.commit()
        await db_session.refresh(doctor, attribute_names=["qualification"])
        return doctor

    return _create_doctor


@pytest_asyncio.fixture(scope="function")
async def volunteer_doctor(volunteer_doctor_factory: CreateDoctorCallable) -> VolunteerDoctor:
    return await volunteer_doctor_factory()


@pytest_asyncio.fixture(scope="function")
async def authenticated_doctor_client(
    client: AsyncClient, volunteer_doctor: VolunteerDoctor
) -> tuple[AsyncClient, VolunteerDoctor]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(volunteer_doctor.id),
            role=volunteer_doctor.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"
    return client, volunteer_doctor


# ========================================================================
# ====================== PREGNANT WOMAN FIXTURES =========================
# ========================================================================
CreatePregnantWomanCallable = Callable[
    ...,  # Accepts any keyword arguments (**kwargs)
    Awaitable[PregnantWoman],  # Must return an awaitable object (a coroutine) that resolves to PregnantWoman
]


@pytest_asyncio.fixture(scope="function")
async def pregnant_woman_factory(db_session: AsyncSession) -> CreatePregnantWomanCallable:
    async def _create_woman(**kwargs) -> PregnantWoman:
        unique_id = str(uuid.uuid4())
        defaults = {
            "first_name": unique_id,
            "middle_name": unique_id,
            "last_name": unique_id,
            "role": UserRole.PREGNANT_WOMAN,
            "email": f"mother_{unique_id}@test.com",
            "hashed_password": "hashed_password_456",
        }
        user_data = defaults | kwargs
        mother = PregnantWoman(**user_data)
        db_session.add(mother)
        await db_session.commit()
        return mother

    return _create_woman


@pytest_asyncio.fixture(scope="function")
async def pregnant_woman(pregnant_woman_factory: CreatePregnantWomanCallable) -> PregnantWoman:
    return await pregnant_woman_factory()


@pytest_asyncio.fixture(scope="function")
async def authenticated_pregnant_woman_client(
    client: AsyncClient, pregnant_woman: PregnantWoman
) -> tuple[AsyncClient, PregnantWoman]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(pregnant_woman.id),
            role=pregnant_woman.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"
    return client, pregnant_woman


# ========================================================================
# ====================== NUTRITIONIST FIXTURES ===========================
# ========================================================================
CreateNutritionistCallable = Callable[
    ...,  # Accepts any keyword arguments (**kwargs)
    Awaitable[Nutritionist],  # Must return an awaitable object (a coroutine) that resolves to Nutritionist
]


@pytest_asyncio.fixture(scope="function")
async def nutritionist_factory(db_session: AsyncSession) -> CreateNutritionistCallable:
    async def _create_nutritionist(**kwargs) -> Nutritionist:
        unique_id = str(uuid.uuid4())

        # Create qualification if not provided
        if "qualification_id" not in kwargs:
            qualification = NutritionistQualification(
                qualification_option=NutritionistQualificationOption.CERTIFIED_NUTRITIONIST
            )
            db_session.add(qualification)
            await db_session.flush()
            kwargs["qualification_id"] = qualification.id

        defaults = {
            "role": UserRole.NUTRITIONIST,
            "email": f"nutritionist_{unique_id}@test.com",
            "hashed_password": "hashed_password_789",
            "first_name": "Jane",
            "last_name": "Smith",
        }

        user_data = defaults | kwargs
        nutritionist = Nutritionist(**user_data)
        db_session.add(nutritionist)
        await db_session.commit()
        return nutritionist

    return _create_nutritionist


@pytest_asyncio.fixture(scope="function")
async def nutritionist(nutritionist_factory: CreateNutritionistCallable) -> Nutritionist:
    return await nutritionist_factory()


@pytest_asyncio.fixture(scope="function")
async def authenticated_nutritionist_client(
    client: AsyncClient, nutritionist: Nutritionist
) -> tuple[AsyncClient, Nutritionist]:
    jwt_token: str = create_access_token(
        token_data=TokenData(
            sub=str(nutritionist.id),
            role=nutritionist.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
    )
    client.headers["Authorization"] = f"Bearer {jwt_token}"
    return client, nutritionist
