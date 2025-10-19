from app.features.auth.auth_models import AuthLoginRequest, AuthLoginResponse
from fastapi import APIRouter, Depends, HTTPException, status, requests
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.core.settings import settings
from app.core.db_config import get_db
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from app.db_schema import User
from typing import Optional
import jwt

auth_router = APIRouter(prefix="/api/auth")


@auth_router.post("/login")
async def login_via_email(
    req: AuthLoginRequest, db: Session = Depends(get_db)
) -> AuthLoginResponse:
    user: Optional[User] = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    ph = PasswordHasher()
    is_password_correct: bool = ph.verify(user.password_hash, req.password)
    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    encoded_jwt: str = jwt.encode(
        {"sub": user.id}, settings.SECRET_KEY, algorithm="HS256"
    )
    return AuthLoginResponse(access_token=encoded_jwt, token_type="bearer")


# oauth = OAuth()
# oauth.register(
#     name="github",
#     client_id=settings.GITHUB_CLIENT_ID,
#     client_secret=settings.GITHUB_CLIENT_SECRET,
#     access_token_url="https://github.com/login/oauth/access_token",
#     access_token_params=None,
#     authorize_url="https://github.com/login/oauth/authorize",
#     authorize_params=None,
#     api_base_url="https://api.github.com/",
#     client_kwargs={"scope": "user:email"},
# )

# @auth_router.get("/google/login")
# async def login_via_google(req: Request):
#     redirect_uri = req.url_for("auth_via_google")
#     return ""
#
#
# @auth_router.get("/google/callback")
# async def auth_via_google(req: Request):
#     return ""
#
#
# @auth_router.get("/github/login")
# async def login_via_github(req: Request):
#     redirect_uri = req.url_for("auth_via_github")
#     github_client = oauth.create_client("github")
#     return await github_client.authorize_redirect(req, redirect_uri)
#
#
# @auth_router.get("/github/callback")
# async def auth_via_github(req: Request):
#     github = oauth.create_client("github")  # Get the github client
#     try:
#         token = await github.authorize_access_token(req)
#     except OAuthError as error:
#         return {"error": error.error}
#     resp = await github.get("user", token=token)
#     user_data = resp.json()
#     req.session["user"] = user_data
#     return user_data
