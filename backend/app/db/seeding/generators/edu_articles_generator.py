from sqlalchemy.orm import Session
from app.db.db_schema import (
    EduArticleCategory,
    SavedEduArticle,
    PregnantWoman,
    EduArticle,
)
from faker import Faker
from math import floor
import random


class EduArticlesGenerator:
    @staticmethod
    def generate_edu_articles(db: Session, faker: Faker, count: int) -> list[EduArticle]:
        print("Generating educational articles.....")

        all_edu_articles: list[EduArticle] = []
        for _ in range(count):
            article = EduArticle(
                category=random.choice(list(EduArticleCategory)),
                title=faker.words(nb=random.randint(2, 10)),
                content_markdown=faker.paragraphs(nb=random.randint(2, 10)),
            )
            all_edu_articles.append(article)
            db.add(article)
        db.commit()
        return all_edu_articles

    @staticmethod
    def generate_saved_edu_articles(
        db: Session, all_articles: list[EduArticle], all_mothers: list[PregnantWoman]
    ) -> None:
        print("Generating 'saved edu article' entries.....")

        mothers_sample_size: int = random.randint(0, len(all_mothers))
        mothers_sample: list[PregnantWoman] = random.sample(population=all_mothers, k=mothers_sample_size)
        for mother in mothers_sample:
            articles_sample_size: int = random.randint(0, floor(len(all_articles) * 0.3))
            articles_sample: list[EduArticle] = random.sample(population=all_articles, k=articles_sample_size)
            for article in articles_sample:
                saved_article = SavedEduArticle(saver=mother, article=article)
                db.add(saved_article)
        db.commit()
