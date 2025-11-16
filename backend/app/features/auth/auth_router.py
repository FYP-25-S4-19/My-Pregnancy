from app.features.auth.auth_models import AuthLoginRequest, AuthLoginResponse, CreatePregAccountRequest
from app.core.password_hasher_config import get_password_hasher
from app.features.auth.auth_service import AuthService
from fastapi import APIRouter, Depends, status
from app.db.db_config import get_db
from sqlalchemy.orm import Session
from argon2 import PasswordHasher

auth_router = APIRouter(prefix="/auth")


def get_auth_service(db: Session = Depends(get_db), ph: PasswordHasher = Depends(get_password_hasher)):
    return AuthService(db, ph)


@auth_router.post("/register", response_model=None, status_code=status.HTTP_201_CREATED)
def register_via_username_email(
    req: CreatePregAccountRequest, auth_service: AuthService = Depends(get_auth_service), db: Session = Depends(get_db)
):
    try:
        auth_service.register_via_username_email(req)
        db.commit()
    except:
        db.rollback()
        raise


@auth_router.post("/login", response_model=AuthLoginResponse, status_code=status.HTTP_200_OK)
def login_via_username(
    req: AuthLoginRequest, auth_service: AuthService = Depends(get_auth_service)
) -> AuthLoginResponse:
    return auth_service.login_via_username(req)


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
