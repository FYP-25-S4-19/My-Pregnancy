from app.features.auth.auth_models import CreatePregAccountRequest, AuthLoginRequest, AuthLoginResponse
from app.db.db_schema import User, UserRole, PregnantWoman
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from app.core.security import TokenData
from app.core.settings import settings
from argon2 import PasswordHasher
from sqlalchemy import or_
import jwt


class AuthService:
    def __init__(self, db: Session, ph: PasswordHasher):
        self.db = db
        self.ph = ph

    def register_via_username_email(self, req: CreatePregAccountRequest) -> PregnantWoman:
        existing_user: User | None = (
            self.db.query(User).filter(or_(User.email == req.email, User.username == req.username)).first()
        )
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

    def login_via_username(self, req: AuthLoginRequest) -> AuthLoginResponse:
        user: User | None = self.db.query(User).filter(User.username == req.username).first()

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
            role=UserRole(user.role).value,
            exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
        )
        encoded_jwt: str = jwt.encode(jwt_data.model_dump(), settings.SECRET_KEY, algorithm="HS256")
        return AuthLoginResponse(access_token=encoded_jwt, token_type="bearer")
