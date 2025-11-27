from datetime import datetime, timedelta

from argon2 import PasswordHasher
from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenData
from app.core.settings import settings
from app.db.db_schema import PregnantWoman, User, UserRole
from app.features.auth.auth_models import AuthLoginRequest, AuthLoginResponse, CreatePregAccountRequest
from app.shared.utils import create_access_token


class AuthService:
    def __init__(self, db: AsyncSession, ph: PasswordHasher):
        self.db = db
        self.ph = ph

    async def register_via_username_email(self, req: CreatePregAccountRequest) -> PregnantWoman:
        query = select(User).where(or_(User.email == req.email, User.username == req.username))
        result = await self.db.execute(query)
        existing_user: User | None = result.scalars().first()

        if existing_user is not None:  # Already exists
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")

        new_preg_woman = PregnantWoman(
            username=req.username,
            role=UserRole.PREGNANT_WOMAN,
            email=req.email,
            password_hash=self.ph.hash(req.password),
            due_date=req.due_date,
            profile_img_key="",
        )
        self.db.add(new_preg_woman)
        return new_preg_woman

    async def login_via_username(self, req: AuthLoginRequest) -> AuthLoginResponse:
        query = select(User).where(User.username == req.username)
        result = await self.db.execute(query)
        user: User | None = result.scalars().first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or user not found"
            )

        try:
            self.ph.verify(str(user.password_hash), req.password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or user not found"
            )

        jwt_data = TokenData(
            sub=str(user.id),
            role=user.role.value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
        return AuthLoginResponse(access_token=create_access_token(jwt_data), token_type="bearer")
