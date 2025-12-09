from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from stream_chat import StreamChat

from app.core.security import require_role
from app.core.settings import settings
from app.core.users_manager import current_active_user
from app.db.db_config import get_db
from app.db.db_schema import PregnantWoman, User
from app.features.getstream.stream_models import ChannelCreationArgs, TokenResponse
from app.features.getstream.stream_service import StreamService

stream_router = APIRouter(prefix="/stream", tags=["GetStream"])


def get_server_client() -> StreamChat:
    if not settings.STREAM_API_KEY or not settings.STREAM_API_SECRET:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)


def get_stream_service(db: AsyncSession = Depends(get_db), client: StreamChat = Depends(get_server_client)):
    return StreamService(db, client)


@stream_router.get("/token", response_model=TokenResponse)
async def get_stream_token(
    user: User = Depends(current_active_user), stream_service: StreamService = Depends(get_stream_service)
) -> TokenResponse:
    try:
        return await stream_service.get_stream_token(user)
    except Exception as e:
        print("Error while fetching stream token:", e)
        raise


@stream_router.post("/chat/channel", status_code=status.HTTP_200_OK)
async def create_chat_channel(
    args: ChannelCreationArgs,
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
    stream_service: StreamService = Depends(get_stream_service),
) -> None:
    await stream_service.create_chat_channel(args, mother)


# @stream_router.post("/chat/channel/message")
# async def send_message(user: User = Depends(require_role(User))):
#     server_client: StreamChat = get_server_client()
# server_client.send_mes
