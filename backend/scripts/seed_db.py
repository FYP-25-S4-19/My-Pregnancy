import os
# from app.db_config import SessionLocal
# from app.db_schema import EduArticleCategory, EduArticle


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    print("Script file:", __file__)
    # db = SessionLocal()
    # try:
    #     cat_baby = EduArticleCategory(label="Baby")
    #     cat_diet = EduArticleCategory(label="Diet")
    #     cat_pregnancy = EduArticleCategory(label="Pregnancy")

    #     db.add_all([cat_baby, cat_diet, cat_pregnancy])
    #     db.commit()

    #     for i in range(3):
    #         article = EduArticle(
    #             category=cat_baby,
    #             img_url="https://example.com/image.jpg",
    #             title=f"Article {i + 1}",
    #             content_markdown="Some content",
    #         )
    #         db.add(article)

    #     db.commit()
    #     print("Finished seeding the database!")
    # finally:
    #     db.close()
