from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.db_config import get_db
from app.db.db_schema import VolunteerDoctor
from app.features.educational_articles.edu_article_models import (
    ArticleDetailedResponse,
    ArticleOverviewResponse,
)
from app.features.educational_articles.edu_article_service import EduArticleService

edu_articles_router = APIRouter(prefix="/articles")


def get_edu_articles_service(db: Session = Depends(get_db)) -> EduArticleService:
    return EduArticleService(db)


@edu_articles_router.get("/", response_model=list[ArticleOverviewResponse], status_code=status.HTTP_200_OK)
def get_article_overviews_by_category(category: str, service: EduArticleService = Depends(get_edu_articles_service)):
    return service.get_article_overviews_by_category(category)


@edu_articles_router.get("/{article_id}", response_model=ArticleDetailedResponse)
def get_article_detailed(
    article_id: int, service: EduArticleService = Depends(get_edu_articles_service)
) -> ArticleDetailedResponse:
    return service.get_article_detailed(article_id)


@edu_articles_router.post("/", status_code=status.HTTP_201_CREATED)
def create_article(
    category: str = Form(...),
    title: str = Form(...),
    content_markdown: str = Form(...),
    img_data: UploadFile = File(),
    db: Session = Depends(get_db),
    doctor: VolunteerDoctor = Depends(require_role(VolunteerDoctor)),
    service: EduArticleService = Depends(get_edu_articles_service),
):
    try:
        service.create_article(category, title, content_markdown, img_data, doctor)
        db.commit()
    except:
        db.rollback()
        raise


@edu_articles_router.delete("/{article_id}")
def delete_article(
    article_id: int,
    service: EduArticleService = Depends(get_edu_articles_service),
    db: Session = Depends(get_db),
    deleter: VolunteerDoctor = Depends(require_role(VolunteerDoctor)),
):
    try:
        service.delete_article(article_id, deleter)
        db.commit()
    except:
        db.rollback()
        raise
