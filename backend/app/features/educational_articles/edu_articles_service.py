from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.db_schema import EduArticle, VolunteerDoctor
from app.features.educational_articles.edu_article_models import (
    ArticleDetailedResponse,
    ArticleOverviewResponse,
)


class EduArticlesService:
    def __init__(self, db: Session):
        self.db = db

    def get_article_overviews_by_category(self, category: str) -> list[ArticleOverviewResponse]:
        article_overviews = (
            self.db.execute(select(EduArticle.id, EduArticle.title).where(EduArticle.category == category))
            .mappings()
            .all()
        )
        return [ArticleOverviewResponse(id=ao.id, title=ao.title) for ao in article_overviews]

    def get_article_detailed(self, article_id: int) -> ArticleDetailedResponse:
        article = self.db.get(EduArticle, article_id)
        if article is None:
            raise
        return ArticleDetailedResponse.model_validate(article, from_attributes=True)

    def create_article(
        self, category: str, title: str, content_markdown: str, img_data: UploadFile, doctor: VolunteerDoctor
    ) -> EduArticle | None:
        article = EduArticle(
            author_id=doctor.id,
            category=category,
            img_key=None,
            title=title,
            content_markdown=content_markdown,
        )
        self.db.add(article)
        self.db.flush()
        # article_img_key: str = S3StorageInterface.put_article_img(article.id, img_data)
        # article.img_key = article_img_key
        return article

    def delete_article(self, article_id: int) -> None:
        article = self.db.get(EduArticle, article_id)
        self.db.delete(article)
