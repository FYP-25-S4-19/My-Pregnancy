from fastapi import APIRouter
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.core.settings import settings

auth_router = APIRouter(prefix="/api/auth")

oauth = OAuth()
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


@auth_router.get("/google/login")
async def login_via_google(req: Request):
    redirect_uri = req.url_for("auth_via_google")
    return ""


@auth_router.get("/google/callback")
async def auth_via_google(req: Request):
    return ""


@auth_router.get("/github/login")
async def login_via_github(req: Request):
    redirect_uri = req.url_for("auth_via_github")
    github_client = oauth.create_client("github")
    return await github_client.authorize_redirect(req, redirect_uri)


@auth_router.get("/github/callback")
async def auth_via_github(req: Request):
    github = oauth.create_client("github")  # Get the github client
    try:
        token = await github.authorize_access_token(req)
    except OAuthError as error:
        return {"error": error.error}
    resp = await github.get("user", token=token)
    user_data = resp.json()
    req.session["user"] = user_data
    return user_data
