from sqlalchemy.orm import Session
from app.db_schema import (
    EduArticleCategory,
    EduArticle,
)
from faker import Faker
import random


class EduArticlesGenerator:
    @staticmethod
    def generate_edu_articles(
        db: Session, faker: Faker, edu_article_categories: list[EduArticleCategory], count: int
    ) -> list[EduArticle]:
        print("Generating educational articles.....")

        all_edu_articles: list[EduArticle] = []
        for _ in range(count):
            article = EduArticle(
                category=random.choice(edu_article_categories),
                title=faker.words(nb=random.randint(2, 10)),
                content_markdown=faker.paragraphs(nb=random.randint(2, 10)),
            )
            all_edu_articles.append(article)
            db.add(article)
        db.commit()
        return all_edu_articles
