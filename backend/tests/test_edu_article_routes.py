import uuid

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.db_schema import EduArticle, EduArticleCategory, VolunteerDoctor


def test_get_articles_by_category_success(client: TestClient, db_session: Session) -> None:
    for article_category in EduArticleCategory:
        edu_article = EduArticle(
            author_id=1,
            category=article_category,
            img_key="",
            title=str(uuid.uuid4()),
            content_markdown="",
        )
        db_session.add(edu_article)
        db_session.commit()

    for category in EduArticleCategory:
        response = client.get(f"/articles?category={category.value}")
        assert response.status_code == status.HTTP_200_OK

        all_articles = response.json()
        assert isinstance(all_articles, list), f"Expected list, got {type(all_articles)}"

        article = all_articles[0]
        assert isinstance(article["id"], int), f"Article should have an 'id' attribute of type 'int'"
        assert isinstance(article["title"], str), f"Article should have a 'title' attribute of type 'str'"


def test_create_article_success(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    db_session: Session,
    img_file_fixture,
) -> None:
    client, doctor = authenticated_doctor_client

    response = client.post(
        "/articles",
        data={
            "title": "1st Trimester Guide",
            "category": EduArticleCategory.BABY.value,
            "content_markdown": "Le random content",
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_201_CREATED

    article = db_session.query(EduArticle).filter_by(title="1st Trimester Guide").one_or_none()
    assert article is not None, "Article should be created in database"
    assert article.category == EduArticleCategory.BABY
    assert article.content_markdown == "Le random content"


# def test_get_articles_by_category_failure(client: TestClient, db_session: Session) -> None:
