# from app.features.auth.auth_models import AuthLoginRequest, AuthLoginResponse, CreatePregAccountRequest
# from fastapi import APIRouter, Depends, HTTPException, status
# from app.db.db_schema import User, Role, PregnantWoman
# from app.core.security import get_password_hasher, TokenData
# from sqlalchemy.orm import Session, joinedload
# from datetime import datetime, timedelta
# from app.core.settings import settings
# from app.db.db_config import get_db
# from argon2 import PasswordHasher
# from sqlalchemy import or_
# import jwt
#
# auth_router = APIRouter(prefix="/auth")
#
# @auth_router.post("/register")
# async def register_via_username_email(
#     req: CreatePregAccountRequest,
#     db: Session = Depends(get_db),
#     ph: PasswordHasher = Depends(get_password_hasher)
# ):
#     existing_user: User | None = db.query(User).filter(
#         or_(User.email == req.email, User.username == req.username)
#     ).first()
#     if existing_user is not None:  # Already exists
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already in use")
#
#     preg_role: Role | None = db.query(Role).filter(Role.label == "PregnantWoman").first()
#     if preg_role is None:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Missing prerequisite role in DB")
#
#     new_preg_woman = PregnantWoman(
#         username=req.username,
#         role=preg_role,
#         email=req.email,
#         password_hash=ph.hash(req.password),
#         due_date=req.due_date
#     )
#     db.add(new_preg_woman)
#     db.commit()
#
#
# @auth_router.post("/login")
# async def login_via_username(
#     req: AuthLoginRequest,
#     db: Session = Depends(get_db),
#     ph: PasswordHasher = Depends(get_password_hasher)
# ) -> AuthLoginResponse:
#     user: User | None = db.query(User).options(joinedload(User.role)).filter(User.username == req.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#
#     try:
#         ph.verify(user.password_hash, req.password)
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
#
#     jwt_data = TokenData(
#         sub=str(user.id),
#         role=user.role.label,
#         exp=datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
#     )
#     encoded_jwt: str = jwt.encode(jwt_data.model_dump(), settings.SECRET_KEY, algorithm="HS256")
#     return AuthLoginResponse(access_token=encoded_jwt, token_type="bearer")
#

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
