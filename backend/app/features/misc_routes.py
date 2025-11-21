from fastapi import APIRouter

misc_router = APIRouter()


@misc_router.get("/")
def index():
    return "Ping!"
