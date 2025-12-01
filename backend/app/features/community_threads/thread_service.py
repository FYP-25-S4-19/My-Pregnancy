from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_schema import CommunityThread
from app.features.community_threads.thread_models import ThreadPreview
from app.shared.utils import format_user_fullname


class ThreadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_thread_previews(self) -> list[ThreadPreview]:
        stmt = select(CommunityThread).limit(10).order_by(CommunityThread.posted_at.desc())
        query_results = (await self.db.execute(stmt)).scalars().all()
        return [
            ThreadPreview(
                id=thread.id,
                creator_name=format_user_fullname(thread.creator),
                title=thread.title,
                content=thread.content,
                posted_at=thread.posted_at.isoformat(),
            )
            for thread in query_results
        ]

    async def get_thread_by_id(self, thread_id: int):
        pass

    async def create_thread(self, thread_data):
        pass

    async def update_thread(self, thread_id, thread_data):
        pass

    async def delete_thread(self, thread_id):
        pass
