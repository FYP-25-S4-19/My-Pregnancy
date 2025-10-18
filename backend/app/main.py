from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.settings import settings

from app.feature.educational_articles.edu_articles_router import edu_articles_router
from app.feature.auth.auth_router import auth_router
from app.feature.users.users_router import users_router


app = FastAPI()
app.include_router(edu_articles_router)
app.include_router(auth_router)
app.include_router(users_router)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.get("/")
def index():
    return "Hello World"
