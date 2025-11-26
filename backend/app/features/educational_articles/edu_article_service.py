from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.db_schema import EduArticle, EduArticleCategory, VolunteerDoctor
from app.features.educational_articles.edu_article_models import (
    ArticleDetailedResponse,
    ArticleOverviewResponse,
)
from app.shared.s3_storage_interface import S3StorageInterface


class EduArticleService:
    def __init__(self, db: Session):
        self.db = db

    def get_article_overviews_by_category(self, category: str) -> list[ArticleOverviewResponse]:
        if category not in [cat.value for cat in list(EduArticleCategory)]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        article_overviews = (
            self.db.execute(select(EduArticle.id, EduArticle.title).where(EduArticle.category == category))
            .mappings()
            .all()
        )
        return [ArticleOverviewResponse(id=ao.id, title=ao.title) for ao in article_overviews]

    def get_article_detailed(self, article_id: int) -> ArticleDetailedResponse:
        article = self.db.get(EduArticle, article_id)

        if article is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        author: VolunteerDoctor = article.author
        full_name: str = " ".join(part for part in [author.first_name, author.middle_name, author.last_name] if part)

        return ArticleDetailedResponse(
            id=article.id,
            author_id=article.author_id,
            author=full_name,
            category=article.category.value,
            img_key=None,
            title=article.title,
            content_markdown=article.content_markdown,
        )

    def create_article(
        self, category: str, title: str, content_markdown: str, img_data: UploadFile, doctor: VolunteerDoctor
    ) -> EduArticle | None:
        existing_articles = self.db.query(EduArticle).where(EduArticle.title == title).all()
        if len(existing_articles) > 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        article = EduArticle(
            author_id=doctor.id,
            category=category,
            img_key=None,
            title=title,
            content_markdown=content_markdown,
        )
        self.db.add(article)
        self.db.flush()
        article_img_key: str = S3StorageInterface.put_article_img(article.id, img_data)
        article.img_key = article_img_key
        article.img_key = ""
        return article

    def delete_article(self, article_id: int, deleter: VolunteerDoctor) -> None:
        article = self.db.get(EduArticle, article_id)
        if article is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if article.author_id != deleter.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        self.db.delete(article)
