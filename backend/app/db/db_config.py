import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or ""
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in '.env' file'")

# --------------------------------------------------------------------------
# Synchronous Database Connection
# Used for: Scripts, Seeding, Alembic Migrations (often)
# --------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --------------------------------------------------------------------------
# Asynchronous Database Connection
# Used for: FastAPI Application
# --------------------------------------------------------------------------
# SQLAlchemy's async engine requires the driver to be specified in the URL.
# We replace the standard postgresql:// scheme with postgresql+asyncpg://
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

async_engine = create_async_engine(ASYNC_DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db():
    """
    Dependency for FastAPI routers.
    Yields an asynchronous database session.
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
