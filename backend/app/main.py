from app.features.educational_articles.edu_articles_router import edu_articles_router
from starlette.middleware.sessions import SessionMiddleware
from app.features.users.users_router import users_router
from app.features.auth.auth_router import auth_router
from fastapi import FastAPI, Request, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.settings import settings
from app.db.db_config import get_db
from sqlalchemy.orm import Session

app: FastAPI

APP_TITLE = "MyPregnancy API"
if settings.APP_ENV != "dev":
    app = FastAPI(
        title=APP_TITLE,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
else:
    app = FastAPI(title=APP_TITLE)

app.include_router(auth_router)
app.include_router(edu_articles_router)
app.include_router(users_router)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(req: Request, e: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Integrity error: {e}"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(req: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An unexpected error has occurred, {e}"},
    )


@app.get("/")
def index(db: Session = Depends(get_db)):
    return "Hello World"
