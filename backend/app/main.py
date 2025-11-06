from app.features.educational_articles.edu_articles_router import edu_articles_router
from starlette.middleware.sessions import SessionMiddleware
from app.features.users.users_router import users_router
from app.features.auth.auth_router import auth_router
from fastapi import FastAPI, Request, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.settings import settings
from app.db.db_config import get_db, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

app = FastAPI(title="MyPregnancy API")
app.include_router(edu_articles_router)
app.include_router(auth_router)
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
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        return f"Failed to make db query: {settings.DATABASE_URL}"
    return "Hello World"
