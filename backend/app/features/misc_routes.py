from fastapi import APIRouter

misc_router = APIRouter(tags=["Miscellaneous"])


@misc_router.get("/")
def index():
    return "Ping!"
