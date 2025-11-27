from datetime import datetime
from typing import Type, TypeVar

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.db.db_config import get_db
from app.db.db_schema import User

bearer_scheme = HTTPBearer()


class TokenData(BaseModel):
    sub: str
    role: str
    exp: datetime


async def get_current_user(
    token_data: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token: str = token_data.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        token_data_obj = TokenData(**payload)
    except Exception:
        raise credentials_exception

    query = select(User).where(User.id == token_data_obj.sub)
    result = await db.execute(query)
    user: User | None = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user


T = TypeVar("T", bound=User)


def require_role(required_role: Type[T]):
    def role_checker(current_user: User = Depends(get_current_user)) -> T:
        if not isinstance(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: User is not of required type '{required_role.__name__}'",
            )
        return current_user

    return role_checker
