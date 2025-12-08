from fastapi import APIRouter, Depends, HTTPException, status
from stream_chat import StreamChat
from stream_chat.channel import Channel

from app.core.security import require_role
from app.core.settings import settings
from app.core.users_manager import current_active_user
from app.db.db_schema import PregnantWoman, User
from app.features.getstream.stream_models import ChannelCreationArgs
from app.shared.utils import format_user_fullname

stream_router = APIRouter(prefix="/stream", tags=["GetStream"])


def get_server_client():
    if not settings.STREAM_API_KEY or not settings.STREAM_API_SECRET:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_API_SECRET)


@stream_router.get("/token")
async def get_stream_token(
    user: User = Depends(current_active_user), server_client: StreamChat = Depends(get_server_client)
):
    try:
        server_client.upsert_user({"id": str(user.id), "name": format_user_fullname(user)})
        token: str = server_client.create_token(str(user.id))
        return {"token": token}
    except Exception as e:
        print("Error while fetching stream token:", e)
        raise


@stream_router.post("/chat/channel", status_code=status.HTTP_200_OK)
async def create_chat_channel(
    args: ChannelCreationArgs,
    mother: PregnantWoman = Depends(require_role(PregnantWoman)),
    server_client: StreamChat = Depends(get_server_client),
):
    channel: Channel = server_client.channel("messaging", data=dict(members=[args.doctor_id]))
    channel.create(str(mother.id))


# @stream_router.post("/chat/channel/message")
# async def send_message(user: User = Depends(require_role(User))):
#     server_client: StreamChat = get_server_client()
# server_client.send_mes
