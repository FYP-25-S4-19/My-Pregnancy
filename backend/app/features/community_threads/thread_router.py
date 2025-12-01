from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_config import get_db
from app.features.community_threads.thread_service import ThreadService

thread_router = APIRouter(prefix="/threads", tags=["Community Threads"])


def get_threads_service(db: AsyncSession = Depends(get_db)) -> ThreadService:
    return ThreadService(db)


@thread_router.get("/")
async def get_thread_previews(service: ThreadService = Depends(get_threads_service)):
    return await service.get_thread_previews()
