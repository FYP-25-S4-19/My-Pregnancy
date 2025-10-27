from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status, HTTPException
from app.core.settings import settings
from app.db.db_config import get_db
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db.db_schema import User
from pydantic import BaseModel
from datetime import datetime
import jwt

ph = PasswordHasher()
bearer_scheme = HTTPBearer()


def get_password_hasher() -> PasswordHasher:
    return ph


class TokenData(BaseModel):
    sub: str
    role: str
    exp: datetime


def get_current_user(token_data: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token: str = token_data.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        token_data = TokenData(**payload)
    except Exception:
        raise credentials_exception

    user: User | None = db.query(User).filter(User.id == token_data.sub).first()
    if user is None:
        raise credentials_exception
    return user


def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.label != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Requires '{required_role}' role.",
            )
        return current_user
    return role_checker