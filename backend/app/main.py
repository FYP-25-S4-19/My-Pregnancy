from fastapi import FastAPI

from app.entities.items.items_router import items_router

app = FastAPI()
app.include_router(items_router)

@app.get("/")
def index():
    # TODO: Make a database connection
    return "Hello World"
