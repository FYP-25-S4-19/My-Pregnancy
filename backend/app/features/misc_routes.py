from fastapi import APIRouter

misc_router = APIRouter(tags=["Miscellaneous"])


@misc_router.get("/")
async def index():
    return "Ping!"
