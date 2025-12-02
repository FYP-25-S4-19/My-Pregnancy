from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users_manager import current_active_user
from app.db.db_config import get_db
from app.db.db_schema import User
from app.features.community_threads.thread_models import (
    CreateThreadData,
    ThreadData,
    ThreadPreviewData,
    ThreadUpdateData,
)
from app.features.community_threads.thread_service import ThreadService

community_threads_router = APIRouter(prefix="/threads", tags=["Community Threads"])


def get_threads_service(db: AsyncSession = Depends(get_db)) -> ThreadService:
    return ThreadService(db)


@community_threads_router.get("/", response_model=list[ThreadPreviewData])
async def get_thread_previews(service: ThreadService = Depends(get_threads_service)) -> list[ThreadPreviewData]:
    return await service.get_thread_previews()


@community_threads_router.get("/{thread_id}", response_model=ThreadData)
async def get_thread_by_id(thread_id: int, service: ThreadService = Depends(get_threads_service)) -> ThreadData:
    return await service.get_thread_by_id(thread_id)


@community_threads_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_thread(
    thread_data: CreateThreadData,
    service: ThreadService = Depends(get_threads_service),
    creator: User = Depends(current_active_user),
) -> None:
    await service.create_thread(thread_data, creator)


@community_threads_router.put("/{thread_id}", status_code=status.HTTP_200_OK)
async def update_thread(
    thread_id: int,
    thread_data: ThreadUpdateData,
    service: ThreadService = Depends(get_threads_service),
    current_user: User = Depends(current_active_user),
) -> None:
    await service.update_thread(thread_id, thread_data, current_user)


@community_threads_router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread(
    thread_id: int,
    service: ThreadService = Depends(get_threads_service),
    current_user: User = Depends(current_active_user),
) -> None:
    await service.delete_thread(thread_id, current_user)
