import uuid

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.db_schema import Admin, EduArticle, EduArticleCategory, Nutritionist, PregnantWoman, VolunteerDoctor


# =========================================================================
# ========================== GET ARTICLES =================================
# =========================================================================
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
        assert isinstance(article["id"], int), "Article should have an 'id' attribute of type 'int'"
        assert isinstance(article["title"], str), "Article should have a 'title' attribute of type 'str'"


def test_get_articles_by_nonexistent_category_failure(client: TestClient) -> None:
    response = client.get("/articles?category=THERES_NO_WAY_THIS_CATEGORY_EXISTS_KEYBOARD_MASHING_ALFIJLEAIJFL")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_article_detailed_success(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor], db_session: Session
) -> None:
    client, doctor = authenticated_doctor_client

    article_title: str = "5 dishes that will blow your (pregnancy) socks off"
    article_content: str = "Fish, fish, a rice cake, fish and a rice cake, and fish"

    article = EduArticle(
        author_id=doctor.id,
        category=EduArticleCategory.NUTRITION.value,
        img_key="",
        title=article_title,
        content_markdown=article_content,
    )
    db_session.add(article)
    db_session.commit()

    response = client.get(f"/articles/{article.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == article.id
    assert data["author_id"] == doctor.id
    assert data["category"] == EduArticleCategory.NUTRITION.value
    assert data["title"] == article_title
    assert data["content_markdown"] == article_content


def test_get_article_detailed_invalid_id(client: TestClient) -> None:
    response = client.get("/articles/1337")
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ==========================================================================
# ========================== CREATE ARTICLES ===============================
# ==========================================================================
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
    assert article.author_id == doctor.id
    assert article.category == EduArticleCategory.BABY
    assert article.content_markdown == "Le random content"


def test_unregistered_create_article_fail(
    client: TestClient,
    img_file_fixture,
) -> None:
    response = client.post(
        "/articles",
        data={
            "title": "1st Trimester Guide",
            "category": EduArticleCategory.BABY.value,
            "content_markdown": "Le random content",
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN, (
        "Unauthenticated user should NOT have permissions to create article"
    )


def test_create_article_fail_due_to_duplicate(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor],
    db_session: Session,
    img_file_fixture,
) -> None:
    client, doctor = authenticated_doctor_client

    article_title: str = "1st Trimester Guide"
    article_content: str = "Le random content"

    article = EduArticle(
        author_id=doctor.id,
        category=EduArticleCategory.NUTRITION.value,
        img_key="",
        title=article_title,
        content_markdown=article_content,
    )
    db_session.add(article)
    db_session.commit()

    response = client.post(
        "/articles",
        data={
            "title": article_title,
            "category": EduArticleCategory.BABY.value,
            "content_markdown": article_content,
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, "Article already exists, there should be a conflict"


def test_admin_create_article_fail(
    authenticated_admin_client: tuple[TestClient, Admin],
    img_file_fixture,
) -> None:
    client, _ = authenticated_admin_client
    response = client.post(
        "/articles",
        data={
            "title": "1st Trimester Guide",
            "category": EduArticleCategory.BABY.value,
            "content_markdown": "Le random content",
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN, "Admin user should NOT have permissions to create article"


def test_pregnant_woman_create_article_fail(
    authenticated_pregnant_woman_client: tuple[TestClient, PregnantWoman],
    img_file_fixture,
) -> None:
    client, _ = authenticated_pregnant_woman_client
    response = client.post(
        "/articles",
        data={
            "title": "1st Trimester Guide",
            "category": EduArticleCategory.BABY.value,
            "content_markdown": "Le random content",
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN, (
        "Pregnant women should NOT have permissions to create article"
    )


def test_nutritionist_create_article_fail(
    authenticated_nutritionist_client: tuple[TestClient, Nutritionist],
    img_file_fixture,
) -> None:
    client, _ = authenticated_nutritionist_client
    response = client.post(
        "/articles",
        data={
            "title": "1st Trimester Guide",
            "category": EduArticleCategory.BABY.value,
            "content_markdown": "Le random content",
        },
        files=img_file_fixture,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN, (
        "Nutritionist should NOT have permissions to create article"
    )


# # ==========================================================================
# # ========================= DELETE ARTICLES ================================
# # ==========================================================================
def test_unregistered_delete_article_fail(client: TestClient, db_session: Session) -> None:
    article = EduArticle(
        author_id=1337,
        category=EduArticleCategory.BODY.value,
        img_key="",
        title="Exercises that will make you strong enough to lift a small car",
        content_markdown="Bodyweight push-ups, pilates",
    )
    db_session.add(article)
    db_session.commit()

    response = client.delete(f"/articles/{article.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    edu_article = db_session.get(EduArticle, article.id)
    assert edu_article is not None, "Article should be still exist"


def test_delete_article_success(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor], db_session: Session
) -> None:
    client, doctor = authenticated_doctor_client
    article = EduArticle(
        author_id=doctor.id,
        category=EduArticleCategory.BODY.value,
        img_key="",
        title="Exercises that will make you strong enough to lift a small car",
        content_markdown="Bodyweight push-ups, pilates",
    )
    db_session.add(article)
    db_session.commit()

    response = client.delete(f"/articles/{article.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, "Article should be deleted successfully"

    edu_article = db_session.get(EduArticle, article.id)
    assert edu_article is None, "Article should be 'None'"


def test_delete_article_not_authorized(
    authenticated_doctor_client: tuple[TestClient, VolunteerDoctor], db_session: Session
) -> None:
    client, doctor = authenticated_doctor_client
    article = EduArticle(
        author_id=doctor.id + 1,
        category=EduArticleCategory.BODY.value,
        img_key="",
        title="Exercises that will make you strong enough to lift a small car",
        content_markdown="Bodyweight push-ups, pilates",
    )
    db_session.add(article)
    db_session.commit()

    response = client.delete(f"/articles/{article.id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN, (
        "Trying to delete an article which was not authored by you"
    )

    edu_article = db_session.get(EduArticle, article.id)
    assert edu_article is not None, "Article should be still exist"


def test_delete_nonexistent_article(authenticated_doctor_client: tuple[TestClient, VolunteerDoctor]) -> None:
    client, _ = authenticated_doctor_client

    response = client.delete("/articles/3275")
    assert response.status_code == status.HTTP_404_NOT_FOUND, "Article should not exist"
