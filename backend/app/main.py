from fastapi import FastAPI
from app.entities.educational_articles.edu_articles_router import edu_articles_router


app = FastAPI()
app.include_router(edu_articles_router)


@app.get("/")
def index():
    # TODO: Make a database connection
    return "Hello World"
