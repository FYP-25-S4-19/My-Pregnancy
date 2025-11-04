from app.features.educational_articles.edu_article_models import GetEduArticleResponse
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.db_config import get_db
from app.db.db_schema import EduArticle
from sqlalchemy.orm import Session

edu_articles_router = APIRouter(prefix="/api/articles")


@edu_articles_router.get("/")
def get_all_articles(db: Session = Depends(get_db)):
    try:
        all_articles = db.query(EduArticle).all()
        return all_articles
    except Exception as e:
        print(f"Error during database: {e}")


@edu_articles_router.get("/{article_id}")
def get_article_by_id(article_id: int, db: Session = Depends(get_db)) -> GetEduArticleResponse:
    # edu_article = db.get(EduArticle, article_id)
    edu_article = db.query(EduArticle).filter(EduArticle.id == article_id).first()
    if edu_article is None:
        print("Edu Article Retrieved: ", edu_article)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    print("Edu Article Retrieved: ", edu_article)

    obj = GetEduArticleResponse(
        id=5
        # category=edu_article.category.label,
        # img_url=edu_article.img_url,
        # title=edu_article.title,
        # content_markdown=edu_article.content_markdown
    )
    return obj


@edu_articles_router.get("/{item_id}")
def get_item_by_id(item_id: int) -> str:
    return "Item of ID: " + str(item_id)
