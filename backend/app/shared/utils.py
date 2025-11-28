import jwt
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import TokenData
from app.core.settings import settings


def clear_db(db: Session):
    print("Clearing the database....\n")
    db.execute(text("SET session_replication_role = 'replica';"))  # Disable foreign key constraints

    table_names = db.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';")).scalars().all()
    for table in table_names:  # Truncate all tables
        if table not in ["alembic_version"]:
            db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))

    db.execute(text("SET session_replication_role = 'origin';"))  # Re-enable foreign key constraints
    db.commit()


def create_access_token(token_data: TokenData) -> str:
    return jwt.encode(token_data.model_dump(), settings.SECRET_KEY, algorithm="HS256")


def is_valid_image(upload_file: UploadFile) -> bool:
    try:
        Image.open(upload_file.file)
        upload_file.file.seek(0)
        return True
    except UnidentifiedImageError:
        upload_file.file.seek(0)
        return False
