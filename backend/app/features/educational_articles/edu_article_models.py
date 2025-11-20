from fastapi import UploadFile

from app.core.custom_base_model import CustomBaseModel


class ArticleOverviewResponse(CustomBaseModel):
    id: int
    title: str


class ArticleDetailedResponse(CustomBaseModel):
    id: int
    author_id: int
    author: str
    category: str
    img_key: str | None
    title: str
    content_markdown: str
