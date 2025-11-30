from typing import Type, TypeVar

from fastapi import Depends, HTTPException, status

from app.core.users import current_active_user
from app.db.db_schema import User

# class TokenData(BaseModel):
#     sub: str
#     role: str
#     exp: datetime


T = TypeVar("T", bound=User)


def require_role(required_role: Type[T]):
    def role_checker(current_user: User = Depends(current_active_user)) -> T:
        if not isinstance(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: User is not of required type '{required_role.__name__}'",
            )
        return current_user

    return role_checker
